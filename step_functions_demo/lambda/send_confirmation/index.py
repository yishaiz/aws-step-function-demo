import json
import logging
import time

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    """
    שליחת אישור ללקוח
    """
    logger.info(f"Sending confirmation: {json.dumps(event)}")
    
    order_id = event.get('order_id')
    customer_id = event.get('customer_id')
    transaction_id = event.get('transaction_id')
    amount_charged = event.get('amount_charged', 0)
    
    # סימולציה של שליחת אימייל/SMS
    confirmation_id = f"conf_{order_id}_{int(time.time())}"
    
    # סימולציה של זמן שליחה
    time.sleep(0.5)
    
    logger.info(f"Confirmation sent for order {order_id}, confirmation ID: {confirmation_id}")
    
    return {
        'statusCode': 200,
        'confirmation_sent': True,
        'confirmation_id': confirmation_id,
        'order_id': order_id,
        'customer_id': customer_id,
        'transaction_id': transaction_id,
        'amount_charged': amount_charged,
        'notification_method': 'email',
        'sent_timestamp': int(time.time()),
        'message': f"Order {order_id} confirmed! Amount charged: ${amount_charged}"
    }