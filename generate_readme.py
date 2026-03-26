from datetime import datetime

content = f"""Inventory Management API - Auto Generated README
Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

FastAPI Documentation:
http://localhost:8000/docs

API Endpoints:

1. /getSingleProduct
   Method: GET
   Parameters:
   - id (integer, required)
   Example:
   /getSingleProduct?id=1001

2. /getAll
   Method: GET
   Parameters:
   - None
   Example:
   /getAll

3. /addNew
   Method: POST
   Body (JSON):
   {{
       "ProductID": 999,
       "Name": "Test Item",
       "UnitPrice": 10.5,
       "StockQuantity": 20,
       "Description": "Test product"
   }}

4. /deleteOne
   Method: DELETE
   Parameters:
   - id (integer, required)
   Example:
   /deleteOne?id=999

5. /startsWith
   Method: GET
   Parameters:
   - letter (string, required, single character)
   Example:
   /startsWith?letter=s

6. /paginate
   Method: GET
   Parameters:
   - start_id (integer, required)
   - end_id (integer, required)
   Example:
   /paginate?start_id=1001&end_id=1025

7. /convert
   Method: GET
   Parameters:
   - id (integer, required)
   Example:
   /convert?id=1007

Tech Stack:
- FastAPI
- MongoDB
- Docker
- Jenkins
- Newman
- Pytest
"""

with open("README.txt", "w", encoding="utf-8") as f:
    f.write(content)

print("README.txt generated successfully")