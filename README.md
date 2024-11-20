Invoice Processing System
=========================

This project provides an **end-to-end Invoice Processing System** that leverages Google Generative AI to extract, process, and structure data from invoices. It supports multiple file types such as Excel and PDF, offering detailed insights into **Invoices, Products, and Customers**.

* * * * *

Project Overview
----------------

### Features

-   **Process Excel Invoices**: Extract structured data (e.g., invoice details, product information, and customer data) from Excel files.
-   **Process PDF Invoices**: Utilize Google Generative AI to extract structured data from PDFs with high accuracy.
-   **API Integration**: REST API with an endpoint `/process-invoice` to handle file uploads and data processing.
-   **Data Output**: Outputs data in JSON format, including structured invoice, product, and customer details.

* * * * *

Requirements
------------

Ensure you have the following installed:

-   Python 3.x
-   Flask
-   Flask-CORS
-   Python-dotenv
-   Pandas
-   Google Generative AI Library (`google-generativeai`)

Install dependencies via:

bash

Copy code

`pip install -r requirements.txt`

* * * * *

Data Preparation
----------------

1.  Ensure your **invoices are available** in either Excel (`.xlsx`/`.xls`) or PDF format.
2.  For Excel files:
    -   Ensure critical columns such as **Serial Number**, **Product Name**, **Customer Name**, etc., are present.
3.  For PDF files:
    -   Upload your PDF invoices, and let the system use Generative AI for extraction.

* * * * *

File Descriptions
-----------------

-   **API Backend (`app.py`)**: Handles file uploads and processes invoices using Google Generative AI or Pandas for structured extraction.
-   **Environment Config (`.env`)**: Securely stores sensitive data like the API key for Generative AI.
-   **Requirements File (`requirements.txt`)**: Lists all necessary Python dependencies for the project.

* * * * *

Getting Started
---------------

### 1\. Running the Backend

Deploy or run the backend locally using Flask to process invoices.

Example usage:

bash

Copy code

`python app.py`

### 2\. API Endpoint

To upload and process an invoice, send a `POST` request to the `/process-invoice` endpoint with the invoice file.

Example request (using `curl`):

bash

Copy code

`curl -X POST -F "file=@path_to_invoice.pdf" http://localhost:5000/process-invoice`

### 3\. Deployment

-   **Backend Deployment**: The backend is deployed on Render. The API endpoint is available at:

    arduino

    Copy code

    `https://project-swipe.onrender.com/process-invoice`

-   **Frontend Deployment**: The frontend is deployed on Vercel and interacts seamlessly with the backend API.

* * * * *


## Example Outputs
---

### Processed Invoices (JSON Example):

```json
{
  "Invoices": [
    {
      "invoiceNumber": "1",
      "customerName": "John Doe",
      "productName": "Product 1",
      "quantity": "10",
      "tax": "5%",
      "totalAmount": "$100",
      "date": "12 Nov 2024"
    }
  ],
  "Products": [
    {
      "productName": "Product 1",
      "quantity": "10",
      "unitPrice": "$10",
      "tax": "5%",
      "priceWithTax": "$10.50"
    }
  ],
  "Customers": [
    {
      "customerName": "John Doe",
      "phoneNumber": "9999999999",
      "totalPurchaseAmount": "$100"
    }
  ]
}
```

### Example Workflow

1.  Upload an invoice (Excel or PDF) via the frontend.
2.  Backend processes the file and extracts structured data.
3.  Frontend displays the structured data in a user-friendly format.

* * * * *

Additional Notes
----------------

### Deployment Links

-   **Backend**: [Render Deployment]
-   **Frontend**: Vercel Deployment
-   **Link**:(https://project-swipe.vercel.app)
### Video Demonstration

Upload your demonstration video to platforms like YouTube or Vimeo. Then, add the link here: [Demo Video](#)
