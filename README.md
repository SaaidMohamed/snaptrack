
# [snaptrack][pypi-url]

[pypi-url]: https://github.com/SaaidMohamed/snaptrack/blob/main/README.md

Snaptrack is a simple Flask receipt manager application for managing and analyzing receipts. Users can take a picture or upload a picture of a receipt, convert receipt image to a digital receipt, submit receipt data, view summarized graphs. The app integrates a PostgreSQL database for secure data storage and retrieval.

---

## Features

- Convert receipt image to a digital receipt.
- Edit degital receipt data before saving it. 
- Submit and store degital receipt with all details.
- Visualize receipt data through graphs (totals, averages and predections).
- Store receipt images with their json data.
- prevent duplicate submissions during uploads for data consistency.
- Modern frontend design with responsive layouts.

---

## Technologies Used

- **Backend**: Flask (Python)
- **Database**: PostgreSQL
- **Frontend**: HTML, CSS, JavaScript (Fetch API)
- **Styling**: CSS (including custom gradients and transitions)

---

## Installation

### Prerequisites

- Python 3.x
- PostgreSQL
- Node.js (optional, if using advanced JS tooling)

### Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/SaaidMohamed/snaptrack.git
   cd snaptrack
   ```

2. Create a virtual environment and activate it:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up your PostgreSQL database and configure it:
   ```sql
   CREATE DATABASE snaptrack;
   ```
   Update `app.py` or `.env` with your database credentials.

5. Run the Flask app:
   ```bash
   flask run
   ```

6. Visit the app at `http://127.0.0.1:5000`.

---

## Usage

### Upload Receipts
- Navigate to `Home` and click on 'take a picture' to take a picture of the receipt, review receipt picture and submit.
- If camera option is not supported on your device, click on 'upload receipt' to upload a picture of the receipt, review receipt picture and submit.

### Editting Receipts
- After processing the uploaded picture, the digital receipt can be edited before saving it.
- Saving the receipt will redirect to receipts page.

### Viewing Graphs
- Go to `/Insights` to view visualizations of receipts' data.
- first 3 Graph are for total spending by year, month and week.
- Graph for top selling items.
- Graph for daily average spending by month.
- Graph for estimated spending for the upcoming month.

### Error Handling
- If you encounter an error (e.g., visiting a non-existent page), a friendly 404 error page will appear.

---

## File Structure

```
snaptrack/
├── app.py             # Main Flask application
├── helpers.py         # Python helper functions
├── init_db.py         # Python db init and functions
├── receipt_ocr.py     # Python OCR API 
├── valid_email.py     # Python email validation
├── requirements.txt   # Python dependencies
├── static/            # Static assets
│   ├── css/           # Stylesheets
│   └── js/            # JavaScript files
├── templates/         # HTML templates
│   ├── layouts.html   # Base template
|   ├── index.html     # home template
│   └── error.html     # 404 error page
└── README.md          # Project documentation
```

---

## Contributing

Contributions are welcome! Feel free to submit issues or pull requests.

---

## License

This project is licensed under the MIT License.
