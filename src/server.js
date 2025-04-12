const express = require("express");
const fs = require("fs");
const app = express();

// Root route
app.get("/", (req, res) => {
  res.send("Umm Al-Qura API is live!");
});

// /jazantimes route
app.get("/jazantimes", (req, res) => {
  fs.readFile("jazan.json", "utf8", (err, data) => {
    if (err) {
      console.error("Failed to read jazan.json", err);
      return res.status(500).json({ error: "Internal server error" });
    }
    res.header("Content-Type", "application/json");
    res.send(data);
  });
});

// Start server
app.listen(process.env.PORT || 3000, () => {
  console.log("Server is running...");
});
