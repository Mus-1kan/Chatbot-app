import React, { useState } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [query, setQuery] = useState("");
  const [responses, setResponses] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!query.trim()) return;

    setError("");
    setLoading(true);

    try {
      // Sending POST request to Flask API
      const res = await axios.post("http://127.0.0.1:5000/query", { query });

      // Check if suppliers data is available in the response
      if (res.data.suppliers) {
        const supplierData = res.data.suppliers.map((supplier) => (
          <div key={supplier.id}>
            <p><strong>Supplier Name:</strong> {supplier.name}</p>
            <p><strong>Contact:</strong> {supplier.contact_info}</p>
            <p><strong>Product Categories:</strong> {supplier.product_categories}</p>
            <p><strong>Summary:</strong> {supplier.summary}</p>
          </div>
        ));
        setResponses([...responses, { user: query, bot: supplierData }]);
      } else {
        // In case there is no supplier data, use a fallback message
        const botResponse = res.data.message || "Sorry, I couldn't find any relevant suppliers.";
        setResponses([...responses, { user: query, bot: botResponse }]);
      }

    } catch (err) {
      console.error("API error:", err);
      setError("Error: Could not connect to the backend API.");
      setResponses([...responses, { user: query, bot: "Error: Could not connect to the backend API." }]);
    }

    setQuery("");
    setLoading(false);
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>AI-Powered Chatbot</h1>
        <div className="chatbox">
          {responses.map((resp, index) => (
            <div key={index} className="message-pair">
              <p className="user-message"><strong>User:</strong> {resp.user}</p>
              <div className="bot-message"><strong>Bot:</strong> {resp.bot}</div>
            </div>
          ))}
        </div>
        {loading && <p>Loading...</p>}
        {error && <p style={{ color: "red" }}>{error}</p>}
        <form onSubmit={handleSubmit} className="chat-form">
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Ask me anything..."
            className="chat-input"
          />
          <button type="submit" className="chat-button">Send</button>
        </form>
      </header>
    </div>
  );
}

export default App;
