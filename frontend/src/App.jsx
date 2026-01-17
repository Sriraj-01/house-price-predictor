import { useState } from "react";
import axios from "axios";

function App() {
  const [form, setForm] = useState({
    location: "",
    BHK: 2,
    "Carpet Area": "",
    Floor: "",
    Bathroom: 2,
    Balcony: 1,
    Status: "Ready to Move",
    Transaction: "Resale",
    Furnishing: "Semi-Furnished",
    facing: "East",
    overlooking: "Road",
    Society: "Other",
    Ownership: "Freehold"
  });

  const [price, setPrice] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const predictPrice = async () => {
    setLoading(true);
    setError(null);
    setPrice(null);

    try {
      const res = await axios.post(
        "https://house-price-api-7f6w.onrender.com/predict",
        form
      );
      setPrice(res.data.predicted_price);
    } catch (err) {
      setError("Prediction failed. Please check inputs.");
    }

    setLoading(false);
  };

  return (
    <div style={styles.container}>
      <h2>🏠 House Price Predictor</h2>

      <div style={styles.field}>
        <label>Location</label>
        <input
          name="location"
          placeholder="e.g. Bangalore"
          onChange={handleChange}
          required
        />
      </div>

      <div style={styles.field}>
        <label>BHK</label>
        <select name="BHK" onChange={handleChange} value={form.BHK}>
          <option value={1}>1 BHK</option>
          <option value={2}>2 BHK</option>
          <option value={3}>3 BHK</option>
          <option value={4}>4+ BHK</option>
        </select>
      </div>

      <div style={styles.field}>
        <label>Carpet Area (sq ft)</label>
        <input
          name="Carpet Area"
          placeholder="e.g. 900"
          onChange={handleChange}
          required
        />
        <small style={styles.help}>
          Usable area inside the house (excluding walls & common areas)
        </small>
      </div>

      <div style={styles.field}>
        <label>Bathrooms</label>
        <input
          name="Bathroom"
          type="number"
          min="1"
          onChange={handleChange}
          value={form.Bathroom}
        />
      </div>

      <div style={styles.field}>
        <label>Floor</label>
        <input
          name="Floor"
          placeholder="e.g. 3"
          onChange={handleChange}
        />
      </div>

      <button onClick={predictPrice} disabled={loading} style={styles.button}>
        {loading ? "Predicting..." : "Predict Price"}
      </button>

      {price && (
        <h3 style={styles.result}>
          Estimated Price: ₹ {price.toLocaleString()}
        </h3>
      )}

      {error && <p style={styles.error}>{error}</p>}
    </div>
  );
}

const styles = {
  container: {
    maxWidth: 420,
    margin: "40px auto",
    padding: 20,
    fontFamily: "Arial",
    border: "1px solid #ddd",
    borderRadius: 8
  },
  field: {
    marginBottom: 12,
    display: "flex",
    flexDirection: "column"
  },
  help: {
    fontSize: 12,
    color: "#555"
  },
  button: {
    width: "100%",
    padding: 10,
    marginTop: 10,
    cursor: "pointer"
  },
  result: {
    marginTop: 20,
    color: "green"
  },
  error: {
    marginTop: 10,
    color: "red"
  }
};

export default App;
