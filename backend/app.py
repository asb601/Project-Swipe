from flask import Flask, request, jsonify
import google.generativeai as genai
import pandas as pd
import os
import json
from dotenv import load_dotenv
from flask_cors import CORS

load_dotenv()

app = Flask(__name__)
CORS(app) 
api_key = os.getenv("API_KEY")
if not api_key:
    raise ValueError("API_KEY not found in environment variables. Please check your .env file.")

# Configure GenAI
genai.configure(api_key=api_key)

def extract_invoice_details_from_excel(file_path):
    """
    Extract structured invoice details from an Excel file and separate totals or summary rows.

    Args:
        file_path (str): The path to the Excel file.

    Returns:
        dict: A dictionary containing the extracted invoice details and totals separately.
    """
    try:
        # Read the Excel file
        print("Reading Excel file...")
        df = pd.read_excel(file_path)

        # Fill missing values with empty strings
        df.fillna("", inplace=True)

        invoices = []
        products = []
        customers = []
        totals = []

        # Iterate over rows to extract and separate data
        for _, row in df.iterrows():
            # Skip rows where critical fields are empty
            if not row.get("Serial Number") or not row.get("Product Name"):
                # Check if it's a totals row
                if row.get("Serial Number") == "Totals":
                    totals.append({
                        "totalQuantity": row.get("Qty", ""),
                        "totalAmount": row.get("Item Total Amount", ""),
                        "cgst": row.get("CGST", ""),
                        "sgst": row.get("SGST", ""),
                        "igst": row.get("IGST", ""),
                        "netAmount": row.get("ITEM NET AMOUNT", ""),
                        "grandTotal": row.get("ITEM TOTAL AMOUNT", "")
                    })
                continue

            # Extract invoice data
            invoices.append({
                "serialNumber": row.get("Serial Number", ""),
                "customerName": row.get("Party Name", ""),
                "productName": row.get("Product Name", ""),
                "quantity": row.get("Qty", ""),
                "tax": row.get("Tax (%)", ""),
                "totalAmount": row.get("Item Total Amount", ""),
                "date": row.get("Invoice Date", "")
            })

            # Extract product data
            products.append({
                "productName": row.get("Product Name", ""),
                "quantity": row.get("Qty", ""),
                "unitPrice": "",  # Unit Price column not found in the file
                "tax": row.get("Tax (%)", ""),
                "priceWithTax": row.get("Price with Tax", "")
            })

            # Extract customer data
            customers.append({
                "customerName": row.get("Party Name", ""),
                "phoneNumber": row.get("Phone Number", ""),
                "totalPurchaseAmount": row.get("Item Total Amount", "")
            })

        # Consolidate extracted data
        consolidated_data = {
            "Invoices": invoices,
            "Products": products,
            "Customers": customers,
            "Totals": totals  # Add totals as a separate key
        }

        # Print the JSON-formatted data for debugging
        print("Extracted Data in JSON Format:")
        print(json.dumps(consolidated_data, indent=4))

        return consolidated_data

    except Exception as e:
        print(f"An error occurred while processing the Excel file: {e}")
        return None



def clean_extracted_data(raw_data):
    """
    Clean the raw extracted data by removing unwanted characters like Markdown formatting.
    """
    try:
        # Remove backticks and "```json" markers
        cleaned_data = raw_data.replace("```json", "").replace("```", "").strip()
        return cleaned_data
    except Exception as e:
        print(f"Error during cleaning extracted data: {e}")
        return raw_data  # Return raw data if cleaning fails

def convert_to_dataframe_and_dump(data):
    """
    Convert structured JSON data to pandas DataFrame and dump as a JSON string.
    """
    try:
        # Convert extracted data to DataFrames
        invoices_df = pd.DataFrame(data.get("Invoices", []))
        products_df = pd.DataFrame(data.get("Products", []))
        customers_df = pd.DataFrame(data.get("Customers", []))

        # Save DataFrames as JSON strings
        invoices_json = invoices_df.to_json(orient="records", indent=4)
        products_json = products_df.to_json(orient="records", indent=4)
        customers_json = customers_df.to_json(orient="records", indent=4)

        # Consolidate JSON output
        final_json = {
            "Invoices": json.loads(invoices_json),
            "Products": json.loads(products_json),
            "Customers": json.loads(customers_json),
        }

        # Dump final consolidated JSON for output
        dumped_json = json.dumps(final_json, indent=4)
        print("Final JSON Data Dumped:")
        print(dumped_json)
        return dumped_json

    except Exception as e:
        print(f"Error during DataFrame conversion or JSON dump: {e}")
        return {}

def extract_invoice_details(file_path):
    """
    Extract structured invoice details from a file using Google Generative AI.
    """
    try:
        print("Uploading file...")
        uploaded_file = genai.upload_file(file_path)
        print(f"File uploaded successfully: {uploaded_file.name}")

        # Prompt for generative AI
        prompt = """
        Extract all the structured information from this invoice in JSON format for the following fields:
        {
          "Invoices": [
            {
              "serialNumber": "1",
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
        """

        model = genai.GenerativeModel(model_name="gemini-1.5-pro")
        print("Generating content...")

        # Generate content using uploaded file and prompt
        response = model.generate_content([uploaded_file, "\n\n", prompt])
        raw_data = response.text

        # Clean raw extracted data
        print("Raw Extracted Data:")
        print(repr(raw_data))  # Print raw data to debug hidden characters

        cleaned_data = clean_extracted_data(raw_data)
        extracted_json = json.loads(cleaned_data)  # Parse cleaned JSON string

        # Consolidate and dump JSON
        final_json = convert_to_dataframe_and_dump(extracted_json)
        return json.loads(final_json)

    except Exception as e:
        print(f"An error occurred: {e}")
        return {
            "Invoices": [],
            "Products": [],
            "Customers": [],
            "Totals": []
        }
    
    


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
 
    
@app.route('/process-invoice', methods=['POST'])
def process_invoice():
    try:
        # Check if a file is provided
        if 'file' not in request.files:
            return jsonify({"error": "No file provided"}), 400

        file = request.files['file']

        # Save the uploaded file temporarily
        file_path = os.path.join("uploads", file.filename)
        os.makedirs("uploads", exist_ok=True)
        file.save(file_path)

        # Determine the file type
        _, file_extension = os.path.splitext(file.filename.lower())

        if file_extension in ['.xlsx', '.xls']:
            # Process Excel file
            data = extract_invoice_details_from_excel(file_path)
        elif file_extension in ['.pdf', '.png', '.jpg', '.jpeg']:
            # Process PDF or image file
            data = extract_invoice_details(file_path)
        else:
            return jsonify({"error": "Unsupported file type"}), 400

        # Clean up temporary file after processing
        os.remove(file_path)

        # Convert the processed data into JSON and return
        return jsonify(data)

    except Exception as e:
        print(f"An error occurred during processing: {e}")
        return jsonify({"error": str(e)}), 500
