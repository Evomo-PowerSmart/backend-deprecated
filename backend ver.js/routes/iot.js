const express = require("express");
const router = express.Router();
const axios = require("axios");

const devices = [
    {
        name: "MK10M-1e544",
        location: "Chiller witel Jakarta Selatan",
        applicationId: "APP64f7e28a5964d54552",
        deviceId: "DEV650bfd4fb68de46441",
    },
    {
        name: "MK10M-1f228",
        location: "Lift witel Jakarta Selatan",
        applicationId: "APP64f7e28a5964d54552",
        deviceId: "DEV650c04ed6097879912",
    },
    {
        name: "MK10M-1eed0",
        location: "Lift OPMC",
        applicationId: "APP64f7e28a5964d54552",
        deviceId: "DEV650bfd518fdbd25357",
    },
];

// Menampilkan semua perangkat
router.get("/", (req, res) => {
    res.status(200).json(devices);
});

// Mendapatkan data berdasarkan Device ID
router.get("/:deviceId", async (req, res) => {
    const { deviceId } = req.params;

    try {
        const response = await axios.get(
            `https://api-data.telkomiot.id/api/v2.0/APP64f7e28a5964d54552/${deviceId}/lasthistory`
        );
        res.status(200).json(response.data);
    } catch (err) {
        console.error("Error:", err.message);
        res.status(500).json({ error: "Failed to fetch data" });
    }
});

module.exports = router;
