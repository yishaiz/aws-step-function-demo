# app.py
#!/usr/bin/env python3
import aws_cdk as cdk
from step_functions_demo.step_functions_stack import StepFunctionsStack

app = cdk.App()
StepFunctionsStack(app, "StepFunctionsDemo")

app.synth()