/label>
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