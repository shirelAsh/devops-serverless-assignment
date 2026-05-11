from aws_cdk import (
    Stack,
    Duration,
    CfnOutput,
    aws_s3 as s3,
    aws_s3_deployment as s3deploy,
    aws_sns as sns,
    aws_sns_subscriptions as subs,
    aws_lambda as _lambda,
)
from constructs import Construct


class InfraStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, email: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        bucket = s3.Bucket(self, "AssignmentBucket")

        topic = sns.Topic(self, "AssignmentTopic")
        topic.add_subscription(subs.EmailSubscription(email))

        fn = _lambda.Function(
            self,
            "AssignmentLambda",
            runtime=_lambda.Runtime.PYTHON_3_11,
            handler="app.lambda_handler",
            code=_lambda.Code.from_asset("../lambda"),
            timeout=Duration.seconds(30),
            environment={
                "BUCKET_NAME": bucket.bucket_name,
                "TOPIC_ARN": topic.topic_arn,
            },
        )

        bucket.grant_read(fn)
        topic.grant_publish(fn)

        s3deploy.BucketDeployment(
            self,
            "UploadSampleFiles",
            destination_bucket=bucket,
            sources=[s3deploy.Source.asset("../sample_files")],
        )

        CfnOutput(self, "BucketName", value=bucket.bucket_name)
        CfnOutput(self, "LambdaName", value=fn.function_name)
        CfnOutput(self, "TopicArn", value=topic.topic_arn)