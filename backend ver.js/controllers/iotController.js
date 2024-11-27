const axios = require("axios");

exports.getIoTData = async (req, res) => {
    try {
        const apiUrl = "https://api-data.telkomiot.id/api/v2.0/APP64f7e28a5964d54552/DEV650bfd505a3a394189/lasthistory";
        const response = await axios.get(apiUrl);

        const rawData = response.data;

        // Format data seperti tabel
        const formattedData = rawData.map((entry, index) => ({
            id: index + 1,
            reading_time: entry.timestamp || "Unknown",
            position: entry.position || "Unknown",
            meter_type: entry.meter_type || "Unknown",
            meter_serial_number: entry.meter_serial_number || "Unknown",
            active_energy_import: entry.active_energy_import || 0,
            active_energy_export: entry.active_energy_export || 0,
            reactive_energy_import: entry.reactive_energy_import || 0,
            reactive_energy_export: entry.reactive_energy_export || 0,
            apparent_energy_import: entry.apparent_energy_import || 0,
            apparent_energy_export: entry.apparent_energy_export || 0,
        }));
        res.status(200).json({ success: true, data: iotData });
    } catch (err) {
        console.error("Error fetching IoT data:", err.message);
        res.status(500).json({ success: false, error: err.message });
    }
};
