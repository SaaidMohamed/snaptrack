
# [snaptrack][pypi-url]

[pypi-url]: https://github.com/SaaidMohamed/snaptrack/blob/main/README.md

Snaptrack is a receipt manager App, a simple Flask application for managing and analyzing receipts. 
Users can take a picture or upload a picture of a receipt, convert receipt image to a digital receipt,
submit receipt data, view summarized graphs, and access user-friendly pages. The app integrates a PostgreSQL database
for secure data storage and retrieval.

---

Video Demo: <https://youtu.be/Tz3JNFO_JwI>


## Features

- Convert receipt image to a digital receipt.
- Submit and store receipt details.
- Visualize receipt data through graphs (totals or summaries).
- User-friendly success/error feedback pages.
- Store images with their json data.
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
   cd receipt-manager
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

### Submitting Receipts
- Navigate to `/add-receipt` and fill out the form to submit a receipt.
- The app will return a unique receipt ID.

### Viewing Graphs
- Go to `/graphs` to view visualizations of receipt data.

### Error Handling
- If you encounter an error (e.g., visiting a non-existent page), a friendly 404 error page will appear.

---

## File Structure

```
receipt-manager/
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
