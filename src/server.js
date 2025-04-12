const { exec } = require("child_process");
const express = require("express");
const app = express(); // <== THIS LINE is missing in your code
app.get("/sync", (req, res) => {
  exec(
    `
    python3 -m venv venv && \
    . venv/bin/activate && \
    pip install --upgrade pip && \
    pip install -r requirements.txt && \
    python3 sync.py
    `,
    (error, stdout, stderr) => {
      if (error) {
        console.error(`Sync failed: ${error.message}`);
        res.send(`Sync failed: ${error.message}`);
        return;
      }
      if (stderr) {
        console.error(`stderr: ${stderr}`);
      }
      console.log(`stdout: ${stdout}`);
      res.send("Sync complete.");
    }
  );
});
