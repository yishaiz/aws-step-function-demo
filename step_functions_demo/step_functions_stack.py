# step_functions_demo/step_functions_stack.py
from aws_cdk import (
    Stack,
    Duration,
    aws_lambda as _lambda,
    aws_stepfunctions as sfn,
    aws_stepfunctions_tasks as tasks,
    aws_iam as iam,
    aws_logs as logs,
)
from constructs import Construct

class StepFunctionsStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # יצירת Lambda Functions
        self.create_lambda_functions()
        
        # יצירת Step Function
        self.create_state_machine()

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

    def create_state_machine(self):
        """יצירת State Machine - הלב של Step Function"""
        
        # הגדרת Tasks (כל Task קורא ל-Lambda)
        validate_task = tasks.LambdaInvoke(
            self, "ValidateOrder",
            lambda_function=self.validate_order_lambda,
            output_path="$.Payload"  # לוקח רק את התוצאה מה-Lambda
        )

        process_payment_task = tasks.LambdaInvoke(
            self, "ProcessPayment", 
            lambda_function=self.process_payment_lambda,
            output_path="$.Payload"
        )

        send_confirmation_task = tasks.LambdaInvoke(
            self, "SendConfirmation",
            lambda_function=self.send_confirmation_lambda,
            output_path="$.Payload"
        )

        update_inventory_task = tasks.LambdaInvoke(
            self, "UpdateInventory",
            lambda_function=self.update_inventory_lambda,
            output_path="$.Payload"
        )

        # הגדרת States לטיפול בשגיאות
        validation_failed = sfn.Fail(
            self, "ValidationFailed",
            cause="Order validation failed",
            error="ValidationError"
        )

        payment_failed = sfn.Fail(
            self, "PaymentFailed", 
            cause="Payment processing failed",
            error="PaymentError"
        )

        order_completed = sfn.Succeed(
            self, "OrderCompleted",
            comment="Order processed successfully"
        )

        # יצירת Workflow עם Conditional Logic
        definition = validate_task.add_choice(
            sfn.Choice(self, "IsOrderValid")
            .when(
                sfn.Condition.boolean_equals("$.valid", False),
                validation_failed
            )
            .otherwise(
                process_payment_task.add_choice(
                    sfn.Choice(self, "IsPaymentSuccessful")
                    .when(
                        sfn.Condition.boolean_equals("$.payment_successful", False),
                        payment_failed
                    )
                    .otherwise(
                        sfn.Parallel(self, "NotifyAndUpdateInventory")
                        .branch(send_confirmation_task)
                        .branch(update_inventory_task)
                        .next(order_completed)
                    )
                )
            )
        )

        # יצירת Log Group ל-Step Function
        log_group = logs.LogGroup(
            self, "StepFunctionLogGroup",
            log_group_name="/aws/stepfunction/OrderProcessing",
            retention=logs.RetentionDays.ONE_WEEK
        )

        # יצירת State Machine
        self.state_machine = sfn.StateMachine(
            self, "OrderProcessingStateMachine",
            definition=definition,
            timeout=Duration.minutes(5),
            logs=sfn.LogOptions(
                destination=log_group,
                level=sfn.LogLevel.ALL
            )
        )