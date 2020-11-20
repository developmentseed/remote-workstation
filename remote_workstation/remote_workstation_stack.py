import os

from aws_cdk import aws_ec2 as ec2
from aws_cdk import aws_ecr as ecr
from aws_cdk import aws_ecs as ecs
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

        self.public_key = self.get_ssh_public_key(os.environ["SSH_PUBLIC_KEY"])

        task_definition = ecs.FargateTaskDefinition(
            self,
            f"fargate-task-definition-{identifier}",
            cpu=int(os.environ.get("INSTANCE_CPU", 256)),
            memory_limit_mib=int(os.environ.get("INSTANCE_MEMORY", 512)),
        )

        log_driver = ecs.AwsLogDriver(
            stream_prefix=f"remote-workstation/{identifier}",
            log_retention=logs.RetentionDays.ONE_WEEK,
        )

        task_definition.add_container(
            f"container-definition-{identifier}",
            image=self.get_docker_image(identifier),
            logging=log_driver,
            environment={"SSH_PUBLIC_KEY": self.public_key},
        )

        fargate_service = ecs.FargateService(
            self,
            f"fargate-service-{identifier}",
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

    def get_ssh_public_key(self, public_keyfile: str):
        with open(public_keyfile, "r") as reader: 
            return reader.readline()

    def get_docker_image(self, identifier: str) -> ecs.AssetImage:
        if ecr_repo := os.environ.get("CONTAINER_ECR_REPOSITORY", None):
            return ecs.ContainerImage.from_ecr_repository(
                ecr.Repository.from_repository_name(
                    self, id=f"ecr-repository-{identifier}", repository_name=ecr_repo
                )
            )
        elif docker_repo := os.environ.get("CONTAINER_DOCKER_REPOSITORY", None):
            return ecs.ContainerImage.from_registry(docker_repo)
        elif local_docker := os.environ.get("CONTAINER_LOCAL_PATH", None):
            return ecs.ContainerImage.from_asset(local_docker)
        else:
            return ecs.ContainerImage.from_asset("docker")
