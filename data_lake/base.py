from enum import Enum
from aws_cdk import (
    aws_s3 as s3,
    core 
)

class DataLakeLayer(Enum):
    RAW="raw"
    PROCESSED="processed"
    CURATED="curated"


class BaseDataLakeBucket(s3.Bucket):
    def __init__(self, scope: core.Construct, layer: DataLakeLayer, **kwargs):
        self.layer = layer
        self.deploy_env = scope.deploy_env
        self.obj_name = f"s3-leoouzabh-{self.deploy_env}-datalake-{self.layer.value}"
        super().__init__(
            scope=scope,
            id=self.obj_name,
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
            encryption=s3.BucketEncryption.S3_MANAGED,
            versioned=True,
            **kwargs
        )
        self.set_default_lifecycle_rule()

    def set_default_lifecycle_rule(self):
        """
        Set lifecycle rules by default
        """
        self.add_lifecycle_rule(
            abort_incomplete_multipart_upload_after=core.Duration.days(7), 
            enabled=True
        )

        self.add_lifecycle_rule(
            noncurrent_version_transitions=[
                s3.NoncurrentVersionTransition(
                    storage_class=s3.StorageClass.INFREQUENT_ACCESS,
                    transition_after=core.Duration.days(30)
                ),
                s3.NoncurrentVersionTransition(
                    storage_class=s3.StorageClass.GLACIER,
                    transition_after=core.Duration.days(60)
                ),
            ]
        )
