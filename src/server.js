const express = require("express");
const { exec } = require("child_process");
const fs = require("fs");
const app = express();

const prayerTimes = require("./jazan.json");

app.get("/", (req, res) => {
  res.send("Athan Clock Server is running");
});

app.get("/jazantimes", (req, res) => {
  res.json(prayerTimes);
});

app.get("/sync", (req, res) => {
  exec("pip install -r requirements.txt && python3 src/sync.py", (err, stdout, stderr) => {
    if (err) {
      console.error("Sync failed:", stderr);
      res.status(500).send("Sync failed:\n" + stderr);
    } else {
      console.log("Sync success:", stdout);
      res.send("Sync complete:\n" + stdout);
    }
  });
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log("Server is running...");
});
