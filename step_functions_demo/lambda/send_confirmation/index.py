# step_functions_demo/lambda/send_confirmation/index.py
import json
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    """
    שליחת אישור ללקוח
    """
    logger.info(f"Sending confirmation: {event}")
    
    order_id = event.get('order_id')
    customer_id = event.get('customer_id')
    transaction_id = event.get('transaction_id')
    
    # סימולציה של שליחת אימייל/SMS
    confirmation_id = f"conf_{order_id}"
    
    return {
        'statusCode': 200,
        'confirmation_sent': True,
        'confirmation_id': confirmation_id,
        'order_id': order_id,
        'customer_id': customer_id,
        'transaction_id': transaction_id,
        'notification_method': 'email'
    }
