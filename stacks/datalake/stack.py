import os
from aws_cdk import (
    aws_s3 as s3,
    core 
)
from stacks.datalake.base import BaseDataLakeBucket, DataLakeLayer

class DataLakeStack(core.Stack):
    def __init__(self, scope: core.Construct, deploy_env, **kwargs):
        self.deploy_env = deploy_env
        super().__init__(scope, id=f"{self.deploy_env}-datalake-stack", **kwargs)

        self.datalake_raw_bucket = BaseDataLakeBucket(self, layer=DataLakeLayer.RAW)
        self.datalake_raw_bucket.add_lifecycle_rule(
            transitions=[
                s3.Transition(
                    storage_class=s3.StorageClass.INTELLIGENT_TIERING,
                    transition_after=core.Duration.days(90)
                ),
                s3.Transition(
                    storage_class=s3.StorageClass.GLACIER,
                    transition_after=core.Duration.days(360)
                )
            ],
            enabled=True
        )
        self.datalake_raw_bucket.add_lifecycle_rule(
            expiration=core.Duration.days(360),
            enabled=True
        )

        self.datalake_processed_bucket = BaseDataLakeBucket(self, layer=DataLakeLayer.PROCESSED)
        self.datalake_curated_bucket = BaseDataLakeBucket(self, layer=DataLakeLayer.CURATED)
