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
        
        print("Reading Excel file...")
        df = pd.read_excel(file_path)

      
        df.fillna("", inplace=True)

        invoices = []
        products = []
        customers = []
        totals = []

        
        for _, row in df.iterrows():
           
            if not row.get("Serial Number") or not row.get("Product Name"):
            
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

           
            invoices.append({
                "serialNumber": row.get("Serial Number", ""),
                "customerName": row.get("Party Name", ""),
                "productName": row.get("Product Name", ""),
                "quantity": row.get("Qty", ""),
                "tax": row.get("Tax (%)", ""),
                "totalAmount": row.get("Item Total Amount", ""),
                "date": row.get("Invoice Date", "")
            })

           
            products.append({
                "productName": row.get("Product Name", ""),
                "quantity": row.get("Qty", ""),
                "unitPrice": "",  
                "tax": row.get("Tax (%)", ""),
                "priceWithTax": row.get("Price with Tax", "")
            })

            
            customers.append({
                "customerName": row.get("Party Name", ""),
                "phoneNumber": row.get("Phone Number", ""),
                "totalPurchaseAmount": row.get("Item Total Amount", "")
            })

     
        consolidated_data = {
            "Invoices": invoices,
            "Products": products,
            "Customers": customers,
            "Totals": totals  
        }

        
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
      
        cleaned_data = raw_data.replace("```json", "").replace("```", "").strip()
        return cleaned_data
    except Exception as e:
        print(f"Error during cleaning extracted data: {e}")
        return raw_data  

def convert_to_dataframe_and_dump(data):
    """
    Convert structured JSON data to pandas DataFrame and dump as a JSON string.
    """
    try:
        
        invoices_df = pd.DataFrame(data.get("Invoices", []))
        products_df = pd.DataFrame(data.get("Products", []))
        customers_df = pd.DataFrame(data.get("Customers", []))

   
        invoices_json = invoices_df.to_json(orient="records", indent=4)
        products_json = products_df.to_json(orient="records", indent=4)
        customers_json = customers_df.to_json(orient="records", indent=4)

       
        final_json = {
            "Invoices": json.loads(invoices_json),
            "Products": json.loads(products_json),
            "Customers": json.loads(customers_json),
        }

   
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

       
        response = model.generate_content([uploaded_file, "\n\n", prompt])
        raw_data = response.text

        print("Raw Extracted Data:")
        print(repr(raw_data))  

        cleaned_data = clean_extracted_data(raw_data)
        extracted_json = json.loads(cleaned_data)  

       
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
     
        if 'file' not in request.files:
            return jsonify({"error": "No file provided"}), 400

        file = request.files['file']

      
        file_path = os.path.join("uploads", file.filename)
        os.makedirs("uploads", exist_ok=True)
        file.save(file_path)

      
        _, file_extension = os.path.splitext(file.filename.lower())

        if file_extension in ['.xlsx', '.xls']:
     
            data = extract_invoice_details_from_excel(file_path)
        elif file_extension in ['.pdf', '.png', '.jpg', '.jpeg']:
    
            data = extract_invoice_details(file_path)
        else:
            return jsonify({"error": "Unsupported file type"}), 400

      
        os.remove(file_path)

     
        return jsonify(data)

    except Exception as e:
        print(f"An error occurred during processing: {e}")
        return jsonify({"error": str(e)}), 500
