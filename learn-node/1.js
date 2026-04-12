const express = require("express");
const app = express();
const port = 3000;

// Middleware to parse JSON
app.use(express.json());

// Basic route
app.get("/", (req, res) => {res.send("Hello, World!");});

app.get("/data", (req, res) => {
  const data = {
    message: "This is some sample data",
    timestamp: new Date(),
  };
  res.json(data);
});

// Start the server
app.listen(port, () => {
  console.log(`Server is running on http://localhost:${port}`);
});
