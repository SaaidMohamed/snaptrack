
# Receipt Manager App

Receipt Manager App is a simple Flask application for managing and analyzing receipts. Users can submit receipt data, view summarized graphs, and access user-friendly pages for success and errors. The app integrates a PostgreSQL database for secure data storage and retrieval.

---

## Features

- Submit and store receipt details with a unique ID for each entry.
- Visualize receipt data through graphs (totals or summaries).
- User-friendly success/error feedback pages.
- Disable duplicate submissions during uploads for data consistency.
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
   git clone https://github.com/your-username/receipt-manager.git
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
   CREATE DATABASE receipt_manager;
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
├── requirements.txt   # Python dependencies
├── static/            # Static assets
│   ├── css/           # Stylesheets
│   └── js/            # JavaScript files
├── templates/         # HTML templates
│   ├── base.html      # Base template
│   └── error.html     # 404 error page
└── README.md          # Project documentation
```

---

## Contributing

Contributions are welcome! Feel free to submit issues or pull requests.

---

## License

This project is licensed under the MIT License.
