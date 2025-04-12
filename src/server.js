const express = require("express");
const { exec } = require("child_process");
const app = express();
const fs = require("fs");
const prayerTimes = require("./jazan.json");

app.get("/", (req, res) => {
  res.send("Athan Clock Server is running!");
});

app.get("/jazantimes", (req, res) => {
  res.json(prayerTimes);
});

app.get("/sync", (req, res) => {
  exec("python3 sync.py", (error, stdout, stderr) => {
    if (error) {
      console.error(`Error: ${stderr}`);
      res.status(500).send(`Sync failed:\n${stderr}`);
    } else {
      console.log(`Output: ${stdout}`);
      res.send(`Sync complete:\n${stdout}`);
    }
  });
});

const port = process.env.PORT || 3000;
app.listen(port, () => {
  console.log("Server is running on port", port);
});
