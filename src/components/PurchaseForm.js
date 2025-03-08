import { useState } from "react";
import axios from "axios";

const PurchaseForm = () => {
  const [item, setItem] = useState("");
  const [cost, setCost] = useState("");
  const [roastLevel, setRoastLevel] = useState(2);
  const [responseMessage, setResponseMessage] = useState("");
  const [customerId, setCustomerId] = useState(""); 

  const handleAnalyzePurchase = async () => {
    try {
      const response = await axios.post("http://127.0.0.1:5000/api/analyze", {
        item,
        cost: Number(cost),
        roastLevel: Number(roastLevel),
      });

      setResponseMessage(response.data.message);
    } catch (error) {
      setResponseMessage("Error: Could not connect to the AI. Try again later.");
      console.error("API Error:", error);
    }
  };

  return (
    <div style={styles.container}>
      <h2>Too Broke for This?</h2>

      <label>Enter Item:</label>
      <input 
        type="text" 
        value={item} 
        onChange={(e) => setItem(e.target.value)} 
        style={styles.input} 
      />

      <label>Enter Cost ($):</label>
      <input 
        type="number" 
        value={cost} 
        onChange={(e) => setCost(e.target.value)} 
        style={styles.input} 
      />

      <label>Choose Your Roast Level ({roastLevel})</label>
      <input
        type="range"
        min="1"
        max="4"
        value={roastLevel}
        onChange={(e) => setRoastLevel(e.target.value)}
        style={styles.slider}
      />

      <button onClick={handleAnalyzePurchase} style={styles.button}>
        Analyze Purchase
      </button>

      <h3>AI Response:</h3>
      <p>{responseMessage}</p>
    </div>
  );
};

const styles = {
  container: {
    maxWidth: "400px",
    margin: "0 auto",
    padding: "20px",
    textAlign: "center",
    background: "#fff",
    borderRadius: "10px",
    boxShadow: "0px 4px 10px rgba(0, 0, 0, 0.1)",
  },
  input: {
    width: "100%",
    padding: "8px",
    marginBottom: "10px",
  },
  slider: {
    width: "100%",
    marginBottom: "10px",
  },
  button: {
    background: "#007bff",
    color: "#fff",
    padding: "10px",
    border: "none",
    borderRadius: "5px",
    cursor: "pointer",
  },
};

export default PurchaseForm;
