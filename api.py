# api.py
import sqlite3
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel

from predict import load_model, predict_text

#debugging
import os
print("DIR CONTENT:", os.listdir())
print("WEBSITE CONTENT:", os.listdir("website") if os.path.exists("website") else "website folder missing!")


# ------------------------------------------------------------
# CONFIG
# ------------------------------------------------------------
MODEL_PATH = "sentiment_model_full.pth"
DB_PATH = "database.db"

model, vocab, max_len = load_model(MODEL_PATH)

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve all frontend files under /website/*
app.mount("/website", StaticFiles(directory="website"), name="website")

# Serve homepage at "/"
@app.get("/")
def serve_home():
    return FileResponse("website/index.html")



# ------------------------------------------------------------
# Pydantic Models
# ------------------------------------------------------------
class PredictRequest(BaseModel):
    text: str


class FeedbackRequest(BaseModel):
    text: str
    model_prediction: int
    actual_label: int


class Reservation(BaseModel):
    full_name: str
    email: str
    phone: str
    guests: int
    date: str
    time: str


# ------------------------------------------------------------
# Database
# ------------------------------------------------------------
def get_db():
    return sqlite3.connect(DB_PATH)


def init_db():
    conn = get_db()
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT,
            model_prediction INTEGER,
            actual_label INTEGER
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS reservations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT,
            email TEXT,
            phone TEXT,
            date TEXT,
            time TEXT,
            guests TEXT
        )
    """)

    conn.commit()
    conn.close()


init_db()


# ------------------------------------------------------------
# PUBLIC ENDPOINTS
# ------------------------------------------------------------
@app.post("/predict")
def predict(req: PredictRequest):
    sentiment, pred_label = predict_text(req.text, model, vocab, max_len)
    return {"sentiment": sentiment, "label": pred_label}


@app.post("/feedback")
def save_feedback(req: FeedbackRequest):
    conn = get_db()
    c = conn.cursor()

    c.execute(
        "INSERT INTO reviews (text, model_prediction, actual_label) VALUES (?, ?, ?)",
        (req.text, req.model_prediction, req.actual_label)
    )

    conn.commit()
    conn.close()
    return {"status": "saved"}


@app.post("/reservations")
def create_reservation(req: Reservation):
    conn = get_db()
    c = conn.cursor()

    c.execute("""
        INSERT INTO reservations (full_name, email, phone, date, time, guests)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (req.full_name, req.email, req.phone, req.date, req.time, req.guests))

    conn.commit()
    conn.close()
    return {"status": "reservation_saved"}


# ------------------------------------------------------------
# ADMIN ENDPOINTS (No Auth)
# ------------------------------------------------------------
@app.get("/admin/reservations")
def admin_get_reservations():
    conn = get_db()
    c = conn.cursor()

    rows = c.execute("SELECT * FROM reservations ORDER BY id DESC").fetchall()
    conn.close()

    return [
        {
            "id": r[0],
            "full_name": r[1],
            "email": r[2],
            "phone": r[3],
            "date": r[4],
            "time": r[5],
            "guests": r[6],
        }
        for r in rows
    ]


@app.delete("/admin/reservations/{item_id}")
def admin_delete_reservation(item_id: int):
    conn = get_db()
    c = conn.cursor()

    c.execute("DELETE FROM reservations WHERE id = ?", (item_id,))
    conn.commit()
    conn.close()

    return {"status": "deleted"}


@app.get("/admin/reviews")
def admin_get_reviews():
    conn = get_db()
    c = conn.cursor()

    rows = c.execute("SELECT * FROM reviews ORDER BY id DESC").fetchall()
    conn.close()

    return [
        {
            "id": r[0],
            "text": r[1],
            "model_prediction": r[2],
            "actual_label": r[3],
        }
        for r in rows
    ]


@app.delete("/admin/reviews/{item_id}")
def admin_delete_review(item_id: int):
    conn = get_db()
    c = conn.cursor()

    c.execute("DELETE FROM reviews WHERE id = ?", (item_id,))
    conn.commit()
    conn.close()

    return {"status": "deleted"}


@app.post("/admin/retrain")
def admin_retrain():
    # Placeholder for future real retraining logic
    return {"status": "retrained"}
