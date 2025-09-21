import json
import logging
import random
import time

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    """
    עיבוד תשלום - סימולציה
    """
    logger.info(f"Processing payment: {json.dumps(event)}")
    
    order_id = event.get('order_id')
    amount = event.get('amount', 0)
    customer_id = event.get('customer_id')
    
    # סימולציה של זמן עיבוד תשלום
    time.sleep(1)
    
    # סימולציה של הצלחה/כישלון (85% הצלחה)
    success = random.random() < 0.85
    
    if success:
        transaction_id = f"txn_{order_id}_{int(time.time())}"
        logger.info(f"Payment successful for order {order_id}, transaction: {transaction_id}")
        
        return {
            'statusCode': 200,
            'payment_successful': True,
            'transaction_id': transaction_id,
            'order_id': order_id,
            'customer_id': customer_id,
            'amount_charged': amount,
            'payment_method': 'credit_card',
            'timestamp': int(time.time())
        }
    else:
        logger.error(f"Payment failed for order {order_id}")
        return {
            'statusCode': 400,
            'payment_successful': False,
            'order_id': order_id,
            'customer_id': customer_id,
            'error': 'Payment declined by bank',
            'error_code': 'PAYMENT_DECLINED'
        }