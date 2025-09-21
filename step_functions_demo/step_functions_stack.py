from aws_cdk import (
    Stack,
    Duration,
    aws_lambda as _lambda,
)
from constructs import Construct

class StepFunctionsStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        # Validate Order Lambda
        self.validate_order_lambda = _lambda.Function(
            self, "ValidateOrderFunction",
            runtime=_lambda.Runtime.PYTHON_3_9,
            code=_lambda.Code.from_asset("step_functions_demo/lambda/validate_order"),
            handler="index.lambda_handler",
            timeout=Duration.seconds(30),
            description="Validates incoming orders"
        )