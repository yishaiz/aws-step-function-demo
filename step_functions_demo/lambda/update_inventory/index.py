import json
import logging
import random
import time

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    """
    עדכון מלאי
    """
    logger.info(f"Updating inventory: {json.dumps(event)}")
    
    order_id = event.get('order_id')
    items = event.get('items', [])
    
    # סימולציה של עדכון מלאי
    inventory_updates = []
    
    for item in items:
        item_id = item.get('id')
        quantity = item.get('quantity', 0)
        item_name = item.get('name', 'Unknown Item')
        
        # סימולציה של בדיקת מלאי נוכחי ועדכון
        current_stock = random.randint(100, 500)  # מלאי נוכחי
        remaining_stock = max(0, current_stock - quantity)
        
        inventory_updates.append({
            'item_id': item_id,
            'item_name': item_name,
            'quantity_ordered': quantity,
            'previous_stock': current_stock,
            'remaining_stock': remaining_stock,
            'low_stock_warning': remaining_stock < 50
        })
        
        logger.info(f"Updated inventory for item {item_id}: {current_stock} -> {remaining_stock}")
    
    # סימולציה של זמן עדכון מלאי
    time.sleep(0.3)
    
    return {
        'statusCode': 200,
        'inventory_updated': True,
        'order_id': order_id,
        'updates': inventory_updates,
        'update_timestamp': int(time.time()),
        'total_items_updated': len(inventory_updates)
    }