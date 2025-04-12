const express = require("express");
const { exec } = require("child_process");
const app = express();

app.get("/", (req, res) => {
  res.send("Athan Clock Server is running");
});

app.get("/sync", (req, res) => {
  exec(`
    python3 -m venv venv && \
    . venv/bin/activate && \
    pip install --upgrade pip && \
    pip install -r ../requirements.txt && \
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
  });
});

app.listen(process.env.PORT || 3000, () => {
  console.log("Server is running");
});
