const express = require("express");
const fs = require("fs");
const app = express();

app.get("/", (req, res) => {
  res.send("Umm Al-Qura API is live!");
});

app.get("/jazantimes", (req, res) => {
  fs.readFile("jazan.json", "utf8", (err, data) => {
    if (err) return res.status(500).json({ error: "Failed to read JSON" });
    res.header("Content-Type", "application/json");
    res.send(data);
  });
});

app.listen(process.env.PORT || 3000, () => {
  console.log("Server running...");
});
