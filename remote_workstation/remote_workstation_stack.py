import os

from aws_cdk import aws_ec2 as ec2
from aws_cdk import aws_ecs as ecs
from aws_cdk import aws_efs as efs
from aws_cdk import aws_logs as logs
from aws_cdk import core


class RemoteWorkstationStack(core.Stack):
    def __init__(
        self,
        scope: core.Construct,
        construct_id: str,
        identifier: str,
        public_ip: str,
        **kwargs,
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        vpc = ec2.Vpc(self, f"vpc-{identifier}", max_azs=1)

        self.cluster = ecs.Cluster(
            self,
            f"cluster-{identifier}",
            vpc=vpc,
            cluster_name=f"remote-cluster-{identifier}",
        )

        file_system = efs.FileSystem(self, f"efs-file-system-{identifier}", vpc=vpc)

        file_system_security_groups = file_system.connections.security_groups

        task_definition = ecs.FargateTaskDefinition(
            self,
            f"fargate-task-definition-{identifier}",
            cpu=256,
            memory_limit_mib=512,
        )

        task_definition.add_volume(
            name=file_system.file_system_id,
            efs_volume_configuration=ecs.EfsVolumeConfiguration(
                file_system_id=file_system.file_system_id
            ),
        )

        container = ecs.ContainerImage.from_asset("docker")

        log_driver = ecs.AwsLogDriver(
            stream_prefix=f"remote-workstation/{identifier}",
            log_retention=logs.RetentionDays.ONE_WEEK,
        )

        container_definition = task_definition.add_container(
            f"container-definition-{identifier}",
            image=container,
            logging=log_driver,
            environment={"SSH_PUBLIC_KEY": os.environ["SSH_PUBLIC_KEY"]},
        )

        container_definition.add_mount_points(
            ecs.MountPoint(
                container_path="/workspace",
                source_volume=file_system.file_system_id,
                read_only=False,
            )
        )

        fargate_service = ecs.FargateService(
            self,
            f"fargate-service-{identifier}",
            platform_version=ecs.FargatePlatformVersion.VERSION1_4,
            assign_public_ip=True,
            cluster=self.cluster,
            desired_count=1,
            task_definition=task_definition,
        )

        for security_group in fargate_service.connections.security_groups:
            security_group.add_ingress_rule(
                peer=ec2.Peer.ipv4(f"{public_ip}/32"),
                connection=ec2.Port.tcp(22),
                description=f"SSH Access from {identifier}s Public IP",
            )
            for fs_security_group in file_system_security_groups:
                fs_security_group.add_ingress_rule(
                    peer=security_group,
                    connection=ec2.Port.all_traffic(),
                    description="Access from the remote workstation fargate service"
                )
