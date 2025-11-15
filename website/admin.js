const API_URL = "http://localhost:8000";

// -----------------------------
// Page Load
// -----------------------------
window.onload = () => {
    loadReservations();
    loadReviews();
};

// -----------------------------
// Reservations
// -----------------------------
async function loadReservations() {
    const r = await fetch(`${API_URL}/admin/reservations`);
    const data = await r.json();

    const table = document.querySelector("#reservationsTable tbody");
    table.innerHTML = "";

    data.forEach(row => {
        table.innerHTML += `
            <tr>
                <td>${row.id}</td>
                <td>${row.full_name}</td>
                <td>${row.email}</td>
                <td>${row.phone}</td>
                <td>${row.date}</td>
                <td>${row.time}</td>
                <td>${row.guests}</td>
                <td><button onclick="deleteReservation(${row.id})">X</button></td>
            </tr>
        `;
    });
}

async function deleteReservation(id) {
    await fetch(`${API_URL}/admin/reservations/${id}`, { method: "DELETE" });
    loadReservations();
}

// -----------------------------
// Reviews
// -----------------------------
async function loadReviews() {
    const r = await fetch(`${API_URL}/admin/reviews`);
    const data = await r.json();

    const table = document.querySelector("#reviewsTable tbody");
    table.innerHTML = "";

    data.forEach(row => {
        table.innerHTML += `
            <tr>
                <td>${row.id}</td>
                <td>${row.text}</td>
                <td>${row.model_prediction}</td>
                <td>${row.actual_label}</td>
                <td><button onclick="deleteReview(${row.id})">X</button></td>
            </tr>
        `;
    });
}

async function deleteReview(id) {
    await fetch(`${API_URL}/admin/reviews/${id}`, { method: "DELETE" });
    loadReviews();
}

// -----------------------------
// Retrain Model
// -----------------------------
async function retrainModel() {
    alert("Retraining model...");
    const r = await fetch(`${API_URL}/admin/retrain`, { method: "POST" });
    alert("Model retrained!");
}
