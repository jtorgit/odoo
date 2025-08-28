# POSPY

POSPY is a simplified example of a Point of Sale project written entirely in Python. It showcases a basic MVC architecture that interacts with the existing Odoo backend via XML-RPC. The user interface is built with Tkinter and mimics the standard POS flows: selecting products, creating orders and synchronising with the server.

The project stores metadata in a local SQLite database while product images are stored in the `images/` directory. This mirrors the approach in Odoo where the file metadata resides in the DB and the files themselves are kept on disk.

## Requirements

- Python 3.9+
- `requests` (for XML-RPC calls via `xmlrpc.client`)
- `Pillow` (optional, for image handling in the GUI)

Install dependencies with:

```bash
pip install -r requirements.txt
```

## Running the Demo

1. Ensure your Odoo backend is reachable and fill in the connection details in `pospy/config.py`.
2. Create the SQLite database by running the initialisation script:

```bash
python -m pospy.backend.database
```

3. Start the graphical interface:

```bash
python -m pospy.frontend.main
```

This will open a simple POS window where you can load products from Odoo and create basic orders. The implementation is intentionally minimal but serves as a starting point for a full featured POS in Python.

## Project Structure

```
POSPY/
  README.md          # This file
  requirements.txt   # Python dependencies
  pospy/
    __init__.py
    config.py        # Connection settings
    backend/
      __init__.py
      bus.py         # Lightweight bus communication
      database.py    # SQLite helpers
      models.py      # Abstractions for products and orders
    frontend/
      __init__.py
      main.py        # Tkinter based GUI
      assets/        # Where product images are stored
  images/            # Example location for attachments
  tests/             # Basic unittests
```

## Disclaimer

This project is an illustrative prototype and does not implement all Point of Sale features. It aims to demonstrate how one might start building a Python-only interface that reuses Odoo's backend models.

