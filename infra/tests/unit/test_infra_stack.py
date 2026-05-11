import aws_cdk as core
import aws_cdk.assertions as assertions

from infra.infra_stack import InfraStack


def _synth_stack() -> assertions.Template:
    app = core.App()
    stack = InfraStack(app, "TestInfraStack", email="test@example.com")
    return assertions.Template.from_stack(stack)


def test_lambda_function_configured():
    template = _synth_stack()
    template.has_resource_properties(
        "AWS::Lambda::Function",
        {
            "Handler": "app.lambda_handler",
            "Runtime": "python3.11",
            "Environment": {
                "Variables": {
                    "BUCKET_NAME": assertions.Match.object_like({}),
                    "TOPIC_ARN": assertions.Match.object_like({}),
                }
            },
        },
    )


def test_sns_topic_exists():
    template = _synth_stack()
    topics = template.find_resources("AWS::SNS::Topic")
    assert len(topics) >= 1


def test_s3_bucket_exists():
    template = _synth_stack()
    buckets = template.find_resources("AWS::S3::Bucket")
    assert len(buckets) >= 1
