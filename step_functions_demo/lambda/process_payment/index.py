# step_functions_demo/lambda/process_payment/index.py
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
    logger.info(f"Processing payment: {event}")
    
    order_id = event.get('order_id')
    amount = event.get('amount', 0)
    
    # סימולציה של זמן עיבוד
    time.sleep(1)
    
    # סימולציה של הצלחה/כישלון (90% הצלחה)
    success = random.random() < 0.9
    
    if success:
        transaction_id = f"txn_{order_id}_{int(time.time())}"
        return {
            'statusCode': 200,
            'payment_successful': True,
            'transaction_id': transaction_id,
            'order_id': order_id,
            'amount_charged': amount,
            'payment_method': 'credit_card'
        }
    else:
        return {
            'statusCode': 400,
            'payment_successful': False,
            'order_id': order_id,
            'error': 'Payment declined by bank'
        }
