# Step Functions Demo Project

פרויקט דמו ללמידת AWS Step Functions עם CDK ו-Python.

## מבנה הפרויקט

המערכת מעבדת הזמנות בתהליך של 4 שלבים:

1. **Validation** - בדיקת תקינות הזמנה
2. **Payment** - עיבוד תשלום
3. **Confirmation** - שליחת אישור (במקביל לעדכון מלאי)
4. **Inventory Update** - עדכון מלאי (במקביל לאישור)

## התקנה והרצה

### צעד 1: הגדרת הסביבה

```bash
# יצירת ספרייה חדשה
mkdir step_functions_demo
cd step_functions_demo

# יצירת סביבה וירטואלית
python -m venv venv
source venv/bin/activate  # Linux/Mac
# או
venv\Scripts\activate  # Windows

# התקנת dependencies
pip install aws-cdk-lib constructs
```

### צעד 2: יצירת מבנה הקבצים

צור את המבנה בהתאם לקבצים למעלה.

### צעד 3: Deploy

```bash
# אתחול CDK (פעם אחת בחשבון)
cdk bootstrap

# Deploy
cdk deploy
```

## בדיקת התוצאות

### דוגמת Input מוצלחת:

```json
{
  "order_id": "order-12345",
  "customer_id": "customer-789",
  "amount": 99.99,
  "items": [
    {
      "id": "item-001",
      "name": "Product A",
      "quantity": 2,
      "price": 49.99
    }
  ]
}
```

### דוגמת Input כושלת (חסר order_id):

```json
{
  "customer_id": "customer-789",
  "amount": 99.99,
  "items": []
}
```

## מה קורה בזרימה?

### 1. קלט נכנס ל-Step Function

```
Input → Step Function → Lambda 1 (Validate)
```

### 2. בדיקת תקינות

```
Lambda Validate → אם תקין: המשך
                → אם לא: FAIL
```

### 3. עיבוד תשלום

```
Lambda Payment → אם הצליח: המשך למקביל
               → אם נכשל: FAIL
```

### 4. עיבוד מקבילי (Parallel)

```
├── Lambda Confirmation
└── Lambda Inventory Update
```

### 5. סיום מוצלח

```
SUCCESS
```

## טיפים לתרגול

### 1. בדיקה בקונסול

- לך ל-AWS Console → Step Functions
- בחר את ה-State Machine שנוצר
- לחץ "Start execution"
- הכנס JSON input
- עקוב אחרי הביצוע הגרפי

### 2. צפייה בלוגים

- לך ל-CloudWatch → Log groups
- חפש את הלוגים של כל Lambda
- ראה איך הנתונים עוברים בין השלבים

### 3. שינויים לתרגול

נסה לשנות:

- הוסף Lambda נוסף (כמו שליחת SMS)
- שנה את לוגיקת ההחלטות
- הוסף Retry ו-Catch לטיפול בשגיאות
- הוסף Wait state עם Timeout

## שגיאות נפוצות ופתרונות

### שגיאה: "Lambda function not found"

- בדוק שהקבצים נמצאים בנתיב הנכון
- ודא ש-`cdk deploy` עבר בהצלחה

### שגיאה: "Permissions denied"

- Step Function מקבל הרשאות אוטומטיות לקרוא ל-Lambda
- אם יש בעיות, בדוק ב-IAM Console

### שגיאה: "Execution failed"

- בדוק CloudWatch Logs
- ודא שה-JSON Input תקין

## קישורים מועילים

- [AWS Step Functions Developer Guide](https://docs.aws.amazon.com/step-functions/)
- [CDK Step Functions Module](https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_stepfunctions/README.html)
