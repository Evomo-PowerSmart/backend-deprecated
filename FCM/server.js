const admin = require("firebase-admin");
const express = require("express");
const bodyParser = require("body-parser");

// Inisialisasi Firebase Admin SDK
const serviceAccount = require("./firebase-key.json");

admin.initializeApp({
    credential: admin.credential.cert(serviceAccount),
});

const app = express();
app.use(bodyParser.json());

// Endpoint untuk mengirim notifikasi
app.post("/send-notification", (req, res) => {
    const { token, title, body } = req.body;

    const message = {
        notification: {
            title: title,
            body: body,
        },
        token: token,
    };

    admin.messaging().send(message)
        .then((response) => {
            res.status(200).send(`Notifikasi berhasil dikirim: ${response}`);
        })
        .catch((error) => {
            res.status(500).send(`Gagal mengirim notifikasi: ${error}`);
        });
});

const PORT = process.env.PORT || 8080;
app.listen(PORT, () => {
    console.log(`Server berjalan di http://localhost:${PORT}`);
});
