
# step_functions_demo/lambda/update_inventory/index.py
import json
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    """
    עדכון מלאי
    """
    logger.info(f"Updating inventory: {event}")
    
    order_id = event.get('order_id')
    items = event.get('items', [])
    
    # סימולציה של עדכון מלאי
    inventory_updates = []
    
    for item in items:
        item_id = item.get('id')
        quantity = item.get('quantity', 0)
        
        inventory_updates.append({
            'item_id': item_id,
            'quantity_reduced': quantity,
            'remaining_stock': random.randint(50, 200)  # סימולציה
        })
    
    return {
        'statusCode': 200,
        'inventory_updated': True,
        'order_id': order_id,
        'updates': inventory_updates
    }