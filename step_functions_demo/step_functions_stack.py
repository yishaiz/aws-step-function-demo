from aws_cdk import (
    Stack,
    Duration,
    aws_lambda as _lambda,
)
from constructs import Construct

class StepFunctionsStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        # יצירת כל ה-Lambda Functions
        self.create_lambda_functions()

    def create_lambda_functions(self):
        """יצירת כל ה-Lambda functions"""
        
        # Validate Order Lambda
        self.validate_order_lambda = _lambda.Function(
            self, "ValidateOrderFunction",
            runtime=_lambda.Runtime.PYTHON_3_9,
            code=_lambda.Code.from_asset("step_functions_demo/lambda/validate_order"),
            handler="index.lambda_handler",
            timeout=Duration.seconds(30),
            description="Validates incoming orders"
        )

        # Process Payment Lambda
        self.process_payment_lambda = _lambda.Function(
            self, "ProcessPaymentFunction",
            runtime=_lambda.Runtime.PYTHON_3_9,
            code=_lambda.Code.from_asset("step_functions_demo/lambda/process_payment"),
            handler="index.lambda_handler",
            timeout=Duration.seconds(60),
            description="Processes payment for orders"
        )

        # Send Confirmation Lambda
        self.send_confirmation_lambda = _lambda.Function(
            self, "SendConfirmationFunction",
            runtime=_lambda.Runtime.PYTHON_3_9,
            code=_lambda.Code.from_asset("step_functions_demo/lambda/send_confirmation"),
            handler="index.lambda_handler",
            timeout=Duration.seconds(30),
            description="Sends order confirmation to customer"
        )

        # Update Inventory Lambda
        self.update_inventory_lambda = _lambda.Function(
            self, "UpdateInventoryFunction",
            runtime=_lambda.Runtime.PYTHON_3_9,
            code=_lambda.Code.from_asset("step_functions_demo/lambda/update_inventory"),
            handler="index.lambda_handler",
            timeout=Duration.seconds(30),
            description="Updates inventory after successful order"
        )