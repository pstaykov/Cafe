const API_URL = "https://cafe-skmi.onrender.com";

// Disable past dates
const dateInput = document.getElementById("date");
if (dateInput) {
    const today = new Date().toISOString().split("T")[0];
    dateInput.min = today;
}


// --------------------------------------------------
// ANALYZE SENTIMENT
// --------------------------------------------------

document.getElementById("analyzeBtn")?.addEventListener("click", analyze);
const feedbackButtons = document.querySelectorAll(".feedbackBtn");

async function analyze() {
    const text = document.getElementById("textInput").value;
    const resultBox = document.getElementById("result");
    const feedbackBox = document.getElementById("feedback");

    resultBox.classList.add("hidden");
    feedbackBox.classList.add("hidden");

    const res = await fetch(`${API_URL}/predict`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text })
    });

    const data = await res.json();
    window.lastPrediction = data.label;

    resultBox.innerHTML = `<strong>Prediction:</strong> ${data.sentiment}`;
    resultBox.classList.remove("hidden");
    feedbackBox.classList.remove("hidden");
}


// --------------------------------------------------
// FEEDBACK (positive / negative buttons)
// --------------------------------------------------

feedbackButtons.forEach(btn => {
    btn.addEventListener("click", async () => {
        const actual_label = Number(btn.dataset.label);
        const text = document.getElementById("textInput").value;
        const model_prediction = window.lastPrediction;

        if (model_prediction === undefined) {
            alert("Please analyze text first.");
            return;
        }

        await fetch(`${API_URL}/feedback`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                text,
                model_prediction,
                actual_label
            })
        });

        alert("Thanks! Feedback saved.");
    });
});


// --------------------------------------------------
// RESERVATION FORM 
// --------------------------------------------------

document.getElementById("reservationForm")?.addEventListener("submit", async (e) => {
    e.preventDefault();

    const payload = {
        full_name: document.getElementById("fullName").value.trim(),
        email: document.getElementById("email").value.trim(),
        phone: document.getElementById("phone").value.trim(),
        guests: Number(document.getElementById("guests").value.trim()),
        date: document.getElementById("date").value.trim(),
        time: document.getElementById("time").value.trim()
    };

    console.log("Sending reservation:", payload);

    const res = await fetch(`${API_URL}/reservations`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
    });

    if (res.ok) {
        document.querySelector('.reservation-form').style.display = 'none';
        document.querySelector('.reservation-info').style.display = 'none';
        document.getElementById('reservationSuccess').classList.remove('hidden');
    } else {
        alert("Error saving reservation. Check server logs.");
    }
});
