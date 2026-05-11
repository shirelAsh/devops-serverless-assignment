#!/usr/bin/env python3
import aws_cdk as cdk
from infra.infra_stack import InfraStack

app = cdk.App()

email = app.node.try_get_context("email")
if not email:
    raise ValueError('Deploy with: cdk deploy -c email="you@example.com"')

InfraStack(app, "InfraStack", email=email)

app.synth()