import os
import datetime
from typing import List
from flask import Flask, render_template, request, redirect,session, jsonify, flash
from flask_bcrypt import Bcrypt
from pydantic import BaseModel, ValidationError
from flask_session import Session
from helpers import apology, login_required
from init_db import db_execute, insert_receipt_and_items_json_to_db
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
    description: str
    amount: float
    qty: int

class Receipt(BaseModel):
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

# Mock receipt data
receipts = [
    {
        "id": 1,
        "merchant": "The Great Store",
        "address": "123 Main Street, City, Country",
        "datetime": "2025-01-07 14:32",
        "total": "$39.00",
        "items": [
            {"name": "Item A", "qty": 1, "price": "$10.00"},
            {"name": "Item B", "qty": 2, "price": "$15.00"},
        ],
    },
    {
        "id": 2,
        "merchant": "Another Shop",
        "address": "456 Market Lane, City, Country",
        "datetime": "2025-01-06 10:15",
        "total": "$25.50",
        "items": [
            {"name": "Item X", "qty": 1, "price": "$12.00"},
            {"name": "Item Y", "qty": 1, "price": "$13.50"},
        ],
    },
]


@app.route("/")
def index():
    # Pass receipts data to the frontend
    return render_template("receipt.html", receipts=receipts)

@app.route("/api/receipt/<int:receipt_id>")
def get_receipt(receipt_id):
    # Fetch receipt details by ID
    receipt = next((r for r in receipts if r["id"] == receipt_id), None)
    if receipt:
        return jsonify(receipt)
    return jsonify({"error": "Receipt not found"}), 404

#@app.route('/')
#@login_required
#def index():
   # """Main index"""   
   # flash("testing flash!!")
    #return render_template('index.html')

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
        return jsonify({"message": "Receipt saved successfully!"}), 200


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

        data = request.form
        username = data.get("username").strip().lower()
        email = data.get("email").strip().lower()
        password = data.get("password")
        password_confirmation = data.get('confirmPassword')
        valid_email = is_valid_email(email)
        user_id = db_execute("SELECT user_id FROM users WHERE email = %s", (email,) )


        if not email or not password or not username :
            return apology("all entries are required", 400)
        if not valid_email:
            return apology("must provide valid email", 400)
        if password != password_confirmation:
            return apology("password mismatch.", 400)
        if user_id :
            return apology("Account already exists.", 400)

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        current_timestamp = datetime.datetime.now()
        query = "INSERT INTO Users (user_name, email, password_hash, created_at, updated_at, is_active, role) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        db_execute(query, (username, email, hashed_password,current_timestamp,current_timestamp,True,'admin'))

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
            return apology("must provide email", 403)
        elif not password:
            return apology("must provide password", 403)

        rows = db_execute("SELECT user_id, password_hash FROM users WHERE email = %s", (email,))
        
        if len(rows) != 1 or not bcrypt.check_password_hash(rows[0]['password_hash'], password):
            return apology("invalid username and/or password", 403)

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
    Data = db_execute("select merchant_name as store, (SELECT SUM(Amount) as total from receipt_items where user_id = %s AND receipt_id = receipts.id)  FROM receipts WHERE user_id = %s", (user_id,user_id))
    result = [{"label": item["store"], "value": item["total"]} for item in Data]
    return jsonify(result)  


@app.route('/history', methods=['GET'])
@login_required
def history():
    '''Populate graph'''
    return render_template("data.html")


@app.route("/logout")
def logout():
    """logs out user"""

    session.clear()
    return redirect("/login")




if __name__ == '__main__':
    app.run(host="0.0.0.0",debug=True)