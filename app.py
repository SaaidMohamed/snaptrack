import os
import datetime
from typing import List
from flask import Flask, render_template, request, redirect,session, jsonify
from flask_bcrypt import Bcrypt
from pydantic import BaseModel, ValidationError
from flask_session import Session
from helpers import apology, login_required
from init_db import db_execute, insert_receipt_and_items_json_to_db, fetch_receipt_and_items_json_from_db
from valid_email import is_valid_email
from receipt_ocr import ReceiptOCR
#from models import db
#from models.user import User
#from models.receipt import Receipt
#from models.receipt_item import ReceiptItem


app = Flask(__name__)
bcrypt = Bcrypt(app)


# PostgreSQL Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
#db.init_app(app)

# Create Tables
#@app.before_first_request
#def create_tables():
    #db.create_all()

# Define Pydantic model for validation
class Item(BaseModel):
    """ docs """
    description: str
    amount: float
    qty: int

class Receipt(BaseModel):
    """ docs """
    merchant_name: str
    merchant_address: str
    date: str
    time: str
    total: float
    currency: str
    ocr_confidence: float
    items: List[Item]


Date = datetime.datetime.now()

JSON_FOLDER = "uploads/json"
IMG_FOLDER = "uploads/img"
app.config['JSON_FOLDER'] = JSON_FOLDER
app.config['IMG_FOLDER'] = IMG_FOLDER
os.makedirs(JSON_FOLDER, exist_ok=True)
os.makedirs(IMG_FOLDER, exist_ok=True)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route('/')
@login_required
def index():
    """Main index"""   
    
    return render_template('index.html')

@app.route('/fetch_receipts')
@login_required
def fetch_receipts():
    """ docs """

    user_id = session['user_id']
    receipts = fetch_receipt_and_items_json_from_db(user_id)

    return render_template("receipt.html", receipts=receipts)



@app.route("/api/receipt", methods=['POST'])
@login_required
def get_receipt():
    """ docs """ 
    if request.method == 'POST':
        req_data = request.json
        if not req_data or 'id' not in req_data:
            return jsonify({'error': 'ID not provided'}), 400

        # Extract the ID
        receipt_id = req_data['id']

        # Fetch receipt details by ID
        user_id = session['user_id']
        receipts = fetch_receipt_and_items_json_from_db(user_id)
        receipt = next((r for r in receipts if r["id"] == receipt_id), None)

        if receipt:
            return jsonify(receipt)
        return jsonify({"error": "Receipt not found"}), 404
    return jsonify({"error": "page not found"}), 404



@app.route('/save-receipt', methods=['POST'])
@login_required
async def save_receipt():
    """ save receipt  """
    if request.method == 'POST':
        try:
            # Get the JSON data from the request body
            json_data = request.get_json()

            # Validate the data with Pydantic (assuming Receipt is a Pydantic model)
            validated_receipt = Receipt(**json_data)  # Directly create a Receipt object

        except ValidationError as e:
            return jsonify({"error": e.errors()}), 400

        # Insert data into PostgreSQL
        user_id = session['user_id']
        insert_receipt_and_items_json_to_db(validated_receipt.model_dump(), user_id)
        receipts = fetch_receipt_and_items_json_from_db(user_id)

        return render_template("receipt.html", receipts=receipts)



@app.route('/upload', methods=['POST'])
@login_required
def upload():
    """uploads image and process"""

    if 'image' not in request.files:
        return apology('No image uploaded', 400)
    
    if request.method == 'POST':

        fs = request.files.get('image')

        if fs.filename == '':
            return apology('No image selected', 400)
        if fs:
            #save uploaded image to /uploads
            img_path = os.path.join(app.config['IMG_FOLDER'], fs.filename)
            json_path = os.path.join(app.config['JSON_FOLDER'], fs.filename)
            fs.save(img_path)

            #make a request to ocr api passing image name.
            ocr = ReceiptOCR()
            ocr_api_data = ocr.ocr_api(img_path,json_path)

            return render_template('ocrtext.html', data = ocr_api_data)
        else:
            return apology('No image uploaded', 400)




@app.route("/register", methods=["GET", "POST"])
def register():
    """registers user"""

    session.clear()
    method = request.method

    if method == "POST":

        form_data = request.form
        username = form_data.get("username").strip().lower()
        email = form_data.get("email").strip().lower()
        password = form_data.get("password")
        password_confirmation = form_data.get('confirmPassword')
        valid_email = is_valid_email(email)
        user_id = db_execute("SELECT user_id FROM users WHERE email = %s", (email,) )

        if not email or not password or not username :
            error_message = {"message":"all entries are required", "class":"error_message"}
            return render_template("/register.html", error_message = error_message)
        
        if not valid_email:
            error_message = {"message":"must provide valid email", "class":"error_message"}
            return render_template("/register.html", error_message = error_message)
                
        if password != password_confirmation:
            error_message = {"message":"password mismatch.", "class":"error_message"}
            return render_template("/register.html", error_message = error_message)
        
        if user_id :
            error_message = {"message":"Account already exists.", "class":"error_message"}
            return render_template("/register.html", error_message = error_message)
        
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        current_timestamp = datetime.datetime.now()
        query = """INSERT INTO Users (user_name, email, password_hash, created_at,
        updated_at, is_active, role) VALUES (%s, %s, %s, %s, %s, %s, %s)"""

        db_execute(query, (username, email, hashed_password,current_timestamp,current_timestamp,True,'admin'))
        rows = db_execute("SELECT user_id, password_hash FROM users WHERE email = %s", (email,))
        session["user_id"] = rows[0]["user_id"]

        return render_template('index.html' )
    
    else:
        return render_template("/register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """logs in user"""

    session.clear()

    if request.method == "POST":

        email = request.form.get("email").strip().lower()
        password = request.form.get("password")

        if not email:
            error_message = {"message":"must provide email", "class":"error_message"}
            return render_template("login.html", error_message = error_message)
        
        elif not password:
            error_message = {"message":"must provide password", "class":"error_message"}
            return render_template("login.html", error_message = error_message)

        rows = db_execute("SELECT user_id, password_hash FROM users WHERE email = %s", (email,))
        
        if len(rows) != 1 or not bcrypt.check_password_hash(rows[0]['password_hash'], password):
            error_message = {"message":"invalid username and/or password", "class":"error_message"}
            return render_template("login.html", error_message = error_message)

        session["user_id"] = rows[0]["user_id"]

        return redirect("/")
    
    else:
        return render_template("login.html")


@app.route('/data', methods=['GET'])
@login_required
def data():
    '''Populate graph'''
    # Fetch data from the database
    user_id = session['user_id']

    db_data_ys = db_execute("""SELECT 
                                DATE_PART('year', date) AS year,
                                SUM(total) AS total
                        FROM receipts
                        WHERE user_id = %s
                        GROUP BY DATE_PART('year', date)
                        ORDER BY year
                        LIMIT 5;""", (user_id,))
    year_spending = [{"label": item["year"], "value": item["total"]} for item in db_data_ys]

    db_data_ms = db_execute("""SELECT
                                TO_CHAR(DATE_TRUNC('month', date), 'Month YYYY') AS month, 
                                SUM(total) AS total
                            FROM receipts
                            WHERE user_id = %s
                            GROUP BY month
                            ORDER BY month
                            LIMIT 12; """, (user_id,))
    month_spending = [{"label": item["month"], "value": item["total"]} for item in db_data_ms]

    db_data_ws = db_execute(""" SELECT
                                TO_CHAR(DATE_TRUNC('week', date), 'YYYY-MM-DD') AS week, 
                                SUM(total) AS total
                            FROM receipts
                            WHERE user_id = %s
                            GROUP BY week
                            ORDER BY week 
                            LIMIT 12; """, (user_id,))
    week_spending = [{"label": item["week"], "value": item["total"]} for item in db_data_ws]

    db_data_tsi = db_execute("""SELECT
                                description, 
                                SUM(qty) AS total
                            FROM receipt_items
                            WHERE user_id = %s
                            GROUP BY description
                            ORDER BY total DESC
                            LIMIT 10;""", (user_id,))
    top_selling_items = [{"label": item["description"], "value": item["total"]} for item in db_data_tsi]

    db_data_dsbm = db_execute(""" SELECT 
                                    TO_CHAR(DATE_TRUNC('month', date), 'Month YYYY') AS month,
                                    SUM(total) / DATE_PART('days', DATE_TRUNC('month', date) + INTERVAL '1 month' - INTERVAL '1 day') AS daily_average
                                FROM receipts
                                WHERE  user_id = %s
                                GROUP BY DATE_TRUNC('month', date)
                                ORDER BY DATE_TRUNC('month', date)
                                LIMIT 12;""", (user_id,))
    daily_spending_by_month = [{"label": item["month"], "value": item["daily_average"]} for item in db_data_dsbm]

    db_data_pnms = db_execute("""WITH user_monthly AS (
                                    SELECT 
                                        DATE_TRUNC('month', date) AS month,
                                        SUM(total) AS total_spending
                                    FROM receipts
                                    WHERE user_id = %s 
                                    GROUP BY  month
                                    ORDER BY month
                                )
                                SELECT TO_CHAR((DATE_TRUNC('month', CURRENT_DATE) + INTERVAL '1 month')::date, 'Month YYYY') AS next_month_start,
                                    AVG(total_spending) AS predicted_next_month_spending
                                FROM user_monthly
                                WHERE month >= NOW() - INTERVAL '6 months' """, (user_id,))
    predicted_next_month_spending = [{"label": item["next_month_start"], "value": item["predicted_next_month_spending"]} for item in db_data_pnms]

    # Combine results into a single response
    graphs_data = {
        "year_spending": year_spending,
        "month_spending": month_spending,
        "week_spending":week_spending,
        "top_selling_items":top_selling_items,
        "daily_spending_by_month":daily_spending_by_month,
        "predicted_next_month_spending":predicted_next_month_spending
    }
    return jsonify(graphs_data)


@app.route('/insights', methods=['GET'])
@login_required
def insights():
    '''Populate graph'''
    return render_template("data.html")


@app.route("/logout")
def logout():
    """logs out user"""

    session.clear()
    return redirect("/login")




if __name__ == '__main__':
    app.run(host="0.0.0.0",debug=True)