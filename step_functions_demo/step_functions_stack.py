from aws_cdk import (
    Stack,
    Duration,
    aws_lambda as _lambda,
)
from constructs import Construct

class StepFunctionsStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        # נתחיל עם Lambda פשוט לבדיקה
        self.test_lambda = _lambda.Function(
            self, "TestFunction",
            runtime=_lambda.Runtime.PYTHON_3_9,
            code=_lambda.Code.from_inline("""
def lambda_handler(event, context):
    print(f"Received event: {event}")
    return {
        'statusCode': 200,
        'message': 'Hello from Step Functions Demo!',
        'input': event
    }
            """),
            handler="index.lambda_handler",
            timeout=Duration.seconds(30),
            description="Simple test lambda for Step Functions demo"
        )