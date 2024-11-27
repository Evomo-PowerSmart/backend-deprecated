const express = require("express");
const router = express.Router();
const { fetchRealtimeData } = require("../controllers/realtimeController");

// Endpoint untuk mendapatkan data IoT
router.get("/", fetchRealtimeData);

module.exports = router;
