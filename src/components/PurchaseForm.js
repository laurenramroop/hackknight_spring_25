import "./PurchaseForm.css";
import React, { useState } from "react";
import axios from "axios"; // Import Axios for API calls
import "./PurchaseForm.css"; // Import CSS for styling

function PurchaseForm() {
    const [item, setItem] = useState(""); // Store item name
    const [cost, setCost] = useState(""); // Store cost
    const [response, setResponse] = useState(""); // Store AI response
    const [loading, setLoading] = useState(false); // Show loading state

    // Function to handle form submission
    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true); // Show loading while waiting for API response

        try {
            const res = await axios.post("http://localhost:5000/analyze", { item, cost });
            setResponse(res.data.message); // Store AI's response
        } catch (error) {
            console.error("Error sending request:", error);
            setResponse("⚠️ Error: Could not connect to the AI. Try again later.");
        }
        
        setLoading(false); // Hide loading
    };

    return (
        <div className="purchase-container">
            <h2>Enter Your Purchase</h2>
            <form onSubmit={handleSubmit} className="purchase-form">
                <input
                    type="text"
                    placeholder="Item name (e.g., Sneakers)"
                    value={item}
                    onChange={(e) => setItem(e.target.value)}
                    required
                />
                <input
                    type="number"
                    placeholder="Cost ($)"
                    value={cost}
                    onChange={(e) => setCost(e.target.value)}
                    required
                />
                <button type="submit" disabled={loading}>
                    {loading ? "Analyzing..." : "Analyze Purchase"}
                </button>
            </form>

            {response && (
                <div className="response-box">
                    <h3>AI Response:</h3>
                    <p>{response}</p>
                </div>
            )}
        </div>
    );
}

export default PurchaseForm;
