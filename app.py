from flask import Flask, request, jsonify
import mysql.connector
from transformers import pipeline
import string  # For stripping punctuation

app = Flask(__name__)

# Configure your MySQL connection details
db_config = {
    "host": "127.0.0.1",         # or "localhost"
    "user": "root",              # Replace with your MySQL username if different
    "password": "",              # Replace with your MySQL password
    "database": "chatbot_db"     # The database name you created
}

# Function to create a connection to the MySQL database
def get_db_connection():
    try:
        conn = mysql.connector.connect(**db_config)
        return conn
    except mysql.connector.Error as e:
        print(f"Database connection error: {e}")
        return None

# Load the GPT-2 model for summarizing supplier details.
summarizer = pipeline("text-generation", model="gpt2", pad_token_id=50256)

def summarize_text(text):
    try:
        summary = summarizer(text, max_length=50, num_return_sequences=1, do_sample=True)
        return summary[0]["generated_text"].strip()
    except Exception as e:
        print(f"Error generating summary: {e}")
        return "Error generating summary"

@app.route("/query", methods=["POST"])
def chatbot_query():
    data = request.json
    user_query = data.get("query", "").lower()
    print(f"Received query: {user_query}")  # Debug output

    # Establish database connection
    connection = get_db_connection()
    if not connection:
        return jsonify({"error": "Failed to connect to the database."}), 500

    cursor = connection.cursor(dictionary=True)
    result = {}

    try:
        if "product" in user_query:
            brand = user_query.split()[-1].strip(string.punctuation)
            sql = "SELECT * FROM products WHERE brand LIKE %s"
            cursor.execute(sql, ("%" + brand + "%",))
            products = cursor.fetchall()
            if products:
                result["products"] = products
            else:
                result["message"] = "No products found for this brand."

        elif "supplier" in user_query:
            # Extract the last word from the query and remove punctuation
            last_word = user_query.split()[-1]
            category = last_word.strip(string.punctuation)
            print(f"Category extracted: '{category}'")  # Debug output

            # Use LOWER() with LIKE to perform a case-insensitive match
            sql = "SELECT * FROM suppliers WHERE LOWER(product_categories) LIKE %s"
            # Build a parameter that searches for the category within the comma-separated list
            param = "%" + category.lower() + "%"
            cursor.execute(sql, (param,))
            suppliers = cursor.fetchall()
            print(f"Suppliers found: {suppliers}")  # Debug output

            if suppliers:
                # Generate a summary for each supplier using GPT-2
                for supplier in suppliers:
                    text_to_summarize = f"Supplier {supplier['name']} offers {supplier['product_categories']}."
                    supplier["summary"] = summarize_text(text_to_summarize)
                result["suppliers"] = suppliers
            else:
                result["message"] = "No suppliers found for this category."

        else:
            result["message"] = "Sorry, I could not understand your query."

    except mysql.connector.Error as e:
        result["error"] = f"Database error: {e}"
    finally:
        cursor.close()
        connection.close()

    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)
