import os

from aws_cdk import aws_ec2 as ec2
from aws_cdk import aws_ecs as ecs
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

        task_definition = ecs.FargateTaskDefinition(
            self, f"fargate-task-definition-{identifier}", cpu=256, memory_limit_mib=512
        )

        container = ecs.ContainerImage.from_asset("docker")

        task_definition.add_container(
            f"container-definition-{identifier}",
            image=container,
            environment={"SSH_PUBLIC_KEY": os.environ["SSH_PUBLIC_KEY"]},
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
