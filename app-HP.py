from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
from transformers import pipeline
import string  # For stripping punctuation

app = Flask(__name__)

# Enable CORS for your React frontend
CORS(app, resources={r"/query": {"origins": "http://localhost:3000"}})

# MySQL configuration
db_config = {
    "host": "127.0.0.1",         # or "localhost"
    "user": "root",              # Your MySQL username
    "password": "",              # Your MySQL password
    "database": "chatbot_db"     # Replace with your database name
}

def get_db_connection():
    try:
        conn = mysql.connector.connect(**db_config)
        return conn
    except mysql.connector.Error as e:
        print(f"Database connection error: {e}")
        return None

# Load the GPT-2 model
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
            category = user_query.split()[-1].strip(string.punctuation)
            sql = "SELECT * FROM suppliers WHERE LOWER(product_categories) LIKE %s"
            param = "%" + category.lower() + "%"
            cursor.execute(sql, (param,))
            suppliers = cursor.fetchall()

            if suppliers:
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
    app.run(debug=True, host="127.0.0.1", port=5000)
