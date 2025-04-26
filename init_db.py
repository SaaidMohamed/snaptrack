import psycopg2
from psycopg2.extras import RealDictCursor

def db_execute(query, params=None):
    """
    Executes a SQL query and returns the result.
    
    :param query: SQL query string
    :param params: Tuple or dictionary of parameters for the query
    :return: Query result or None for non-SELECT queries

    :example: result = db_execute("SELECT * FROM users WHERE email = %s", ('example@test.com',))
    """
    conn = None
    try:
        conn = psycopg2.connect(
            dbname="TestDB",
            user="postgres",
            password="password",
            host="db",
            port="5432"
        )
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(query, params)
            if cursor.description:  # If the query returns data (e.g., SELECT)
                return cursor.fetchall()
            conn.commit()  # Commit if it's an INSERT/UPDATE/DELETE
    except Exception as e:
        return False
    finally:
        if conn:
            conn.close()
    return None

def insert_receipt_and_items_to_db(filtered_data, user_id):
    """
    Inserts receipt data into the database and associates it with a user.

    Parameters:
        filtered_data (dict): The filtered JSON data.
        user_id (int): The ID of the user.

    Returns:
        None
    """
    try:
        # Connect to PostgreSQL
        conn = psycopg2.connect(
            dbname="TestDB",
            user="postgres",
            password="password",
            host="db",
            port="5432"
        )
        cursor = conn.cursor()

        # Insert receipt data
        insert_receipt_query = """
        INSERT INTO receipts (merchant_name, merchant_address, date, time, total, currency, ocr_confidence, user_id)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s) RETURNING id;
        """
        receipt_values = (
            filtered_data.get("merchant_name"),
            filtered_data.get("merchant_address"),
            filtered_data.get("date"),
            filtered_data.get("time"),
            filtered_data.get("total"),
            filtered_data.get("currency"),
            filtered_data.get("ocr_confidence"),
            user_id
        )
        cursor.execute(insert_receipt_query, receipt_values)
        receipt_id = cursor.fetchone()[0]

        # Insert items
        insert_item_query = """
        INSERT INTO receipt_items (receipt_id, description, amount, qty, user_id)
        VALUES (%s, %s, %s, %s, %s);
        """
        for item in filtered_data.get("items", []):
            item_values = (
                receipt_id,
                item.get("description"),
                item.get("amount"),
                item.get("qty"),
                user_id
            )
            cursor.execute(insert_item_query, item_values)

        # Commit the transaction
        conn.commit()

    except Exception as e:
        print(f"Error inserting data: {e}")
        conn.rollback()
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def insert_receipt_and_items_json_to_db(validated_receipt, user_id):
    """
    Inserts receipt json data into the database and associates it with a user.

    Parameters:
        validated_receipt (dict): The filtered JSON data.
        user_id (int): The ID of the user.

    Returns:
        None
    """
    try:
        # Connect to PostgreSQL
        conn = psycopg2.connect(
            dbname="TestDB",
            user="postgres",
            password="password",
            host="db",
            port="5432"
        )
        cursor = conn.cursor()

        try:
        # Step 1: Insert receipt data into 'receipts' table
            insert_receipt_query = """
                INSERT INTO receipts (merchant_name, merchant_address, date, time, total, currency, ocr_confidence, user_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s) RETURNING id;
            """
            cursor.execute(insert_receipt_query, (
                validated_receipt['merchant_name'],
                validated_receipt['merchant_address'],
                validated_receipt['date'],
                validated_receipt['time'],
                validated_receipt['total'],
                validated_receipt['currency'],
                validated_receipt['ocr_confidence'],
                user_id
            ))

            # Get the inserted receipt id
            receipt_id = cursor.fetchone()[0]

            # Step 2: Insert items into 'receipt_items' table
            insert_item_query = """
                INSERT INTO receipt_items (receipt_id, description, amount, qty, user_id)
                VALUES (%s, %s, %s, %s, %s);
            """
            for item in validated_receipt['items']:
                cursor.execute(insert_item_query, (
                    receipt_id,
                    item['description'],
                    item['amount'],
                    item['qty'],
                    user_id
                ))

            # Commit the transaction
            conn.commit()

        except Exception as e:
            print("Error inserting data:", e)
            conn.rollback()
    finally:
        cursor.close()
        conn.close()

def fetch_receipt_and_items_json_from_db(user_id):
    """
    fetch receipt and items json data from the database for a specific user.

    Parameters:
        user_id (int): The ID of the user.

    Returns:
        json list
    """


    # Connect to PostgreSQL
    conn = psycopg2.connect(
        dbname="TestDB",
        user="postgres",
        password="password",
        host="db",
        port="5432"
    )
    cursor = conn.cursor()

    query = """
    SELECT 
        r.id AS receipt_id,
        r.merchant_name,
        r.merchant_address,
        r.date ,
        r.total,
        i.description AS item_name,
        i.qty,
        i.amount
    FROM 
        receipts r
    JOIN 
        receipt_items i
    ON 
        r.id = i.receipt_id
    WHERE r.user_id = %s
    ORDER BY r.id;
    """
    cursor.execute(query, (user_id,))
    rows = cursor.fetchall()

    

    # Extract column names
    column_names = [desc[0] for desc in cursor.description]

    # Close the connection
    cursor.close()
    conn.close()

    # Process the data into the desired format
    data = {}
    for row in rows:
        row_data = dict(zip(column_names, row))
        receipt_id = row_data["receipt_id"]
        
        if receipt_id not in data:
            data[receipt_id] = {
                "id": receipt_id,
                "merchant": row_data["merchant_name"],
                "address": row_data["merchant_address"],
                "datetime": row_data["date"],
                "total": f"${row_data['total']:.2f}",
                "items": []
            }
        data[receipt_id]["items"].append({
            "name": row_data["item_name"],
            "qty": row_data["qty"],
            "price": f"${row_data['amount']:.2f}"
        })
    print(data)
    # Convert data to a list
    return list(data.values())