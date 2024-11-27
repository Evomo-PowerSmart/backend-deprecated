const axios = require("axios");

exports.fetchRealtimeData = async (req, res) => {
    try {
        const apiUrl = "https://api-data.telkomiot.id/api/v2.0/APP64f7e28a5964d54552/DEV650bfd505a3a394189/lasthistory";
    ;

        const realtimeData = response.data; // Data dari API IoT
        console.log("Realtime Data Received:", realtimeData);

        // Kirim data ke client sebagai response
        res.status(200).json({ success: true, data: realtimeData });
    } catch (err) {
        console.error("Error fetching realtime data:", err.message);
        res.status(500).json({ success: false, error: err.message });
    }
};
