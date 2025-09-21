import json
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    """
    בדיקת תקינות הזמנה
    """
    logger.info(f"Validating order: {json.dumps(event)}")
    
    # בדיקות בסיסיות
    order_id = event.get('order_id')
    customer_id = event.get('customer_id')
    amount = event.get('amount', 0)
    items = event.get('items', [])
    
    errors = []
    
    if not order_id:
        errors.append("Missing order_id")
    
    if not customer_id:
        errors.append("Missing customer_id")
    
    if amount <= 0:
        errors.append("Invalid amount - must be greater than 0")
    
    if not items:
        errors.append("No items in order")
    
    if errors:
        logger.error(f"Validation failed for order {order_id}: {errors}")
        return {
            'statusCode': 400,
            'valid': False,
            'errors': errors,
            'order_id': order_id
        }
    
    logger.info(f"Order {order_id} validation successful")
    return {
        'statusCode': 200,
        'valid': True,
        'order_id': order_id,
        'customer_id': customer_id,
        'amount': amount,
        'items': items,
        'validation_timestamp': context.aws_request_id
    }