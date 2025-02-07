Chatbot AI

A full-stack chatbot application built with Flask (backend) and React (frontend). This project uses MySQL for database management and integrates a GPT-2 model for text summarization.

Features

Flask backend for handling user queries

MySQL database for storing products and suppliers

GPT-2 model for supplier summary generation

React frontend for user interaction

CORS support for frontend-backend communication

Tech Stack

Frontend: React.js

Backend: Flask, Flask-CORS

Database: MySQL

AI Model: GPT-2 (Hugging Face Transformers)

Installation & Setup

1️⃣ Clone the Repository

git clone (https://github.com/Mus-1kan/Chatbot-app/)

2️⃣ Set Up the Backend (Flask)

➤ Create a Virtual Environment (Optional)

python -m venv venv
venv\Scripts\activate

➤ Install Dependencies

pip install -r requirements.txt      


➤ Run Flask Server

python app.py

The backend should now be running at http://127.0.0.1:5000.

3️⃣ Set Up the Frontend (React)

cd chatbotai
npm install
npm start

The React app should now be running at http://localhost:3003.

API Endpoints

/query (POST)

Handles user queries and retrieves data from the database.

➤ Request Body:

{
  "query": "Find suppliers for electronics"
}

➤ Response:

{
  "suppliers": [
    {
      "name": "ABC Suppliers",
      "product_categories": "electronics, accessories",
      "summary": "ABC Suppliers offers electronics and accessories."
    }
  ]
}

Troubleshooting

If facing CORS issues, ensure Flask-CORS is properly configured:

from flask_cors import CORS
CORS(app, resources={r"/query": {"origins": "http://localhost:3003"}})

Ensure Flask and React servers are running simultaneously.

License

This project is licensed under the MIT License.

Contributing

Feel free to open issues or submit pull requests!

Contact

For any queries, @tripathimuskan.trm@gmail.com
