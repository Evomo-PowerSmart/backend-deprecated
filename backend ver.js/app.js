const express = require("express");
const bodyParser = require("body-parser");
require("dotenv").config(); // Load environment variables

const realtimeRoutes = require("./routes/realtime");

const app = express();
app.use(bodyParser.json());

// Tambahkan route untuk API Realtime
app.use("/api/realtime", realtimeRoutes);

// Jalankan server
const PORT = process.env.PORT || 8080;
app.listen(PORT, () => {
    console.log(`Server berjalan di http://localhost:${PORT}`);
});


const iotRoutes = require("./routes/iot");
app.use("/api/devices", iotRoutes);

