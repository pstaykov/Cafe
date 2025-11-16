# Cafe Lumiére – Website with Sentiment Analysis and Reservation Backend

This project includes a front‑end cafe website, a backend API for
handling reservations, and a PyTorch-based sentiment analysis model.

## Repository Structure

    __pycache__/
    website/
    api.py
    cafe.db
    data.py
    database.db
    main.py
    model.py
    predict.py
    render.yaml
    requirements.txt
    schemas.py
    sentiment_model_full.pth
    test.csv
    texts.json
    train.py

Component Overview

### website/

Front-end files such as HTML, CSS, and JavaScript.

### api.py

Defines API endpoints for reservations and sentiment prediction.

### main.py

Entry point of the backend, starts server, loads model, configures
routing.

### model.py

PyTorch architecture for sentiment classification.

### train.py

Trains the sentiment model using texts.json and test.csv. Produces
sentiment_model_full.pth.

### predict.py

Loads the trained model and predicts sentiment for given text.

### schemas.py

Defines input and output schemas for API interactions.

### data.py

Data loading and preprocessing utilities.

### Database Files

database.db and cafe.db store reservation and application data using
SQLite.

### Dataset Files

texts.json and test.csv contain labeled text examples for training and
testing.

## Features

1. Cafe Website

-   Menu pages
-   About page
-   Contact section
-   Reservation form

2. Reservation Backend

-   Create reservations
-   Retrieve reservations
-   Validate input via schemas
-   Store entries in SQLite

3. Sentiment Analysis

-   PyTorch model for text sentiment classification
-   Training script included
-   Prediction script included

## Where to view it
view the website at https://cafe-skmi.onrender.com/

## API Overview

### Create a reservation

    POST /reservations

### Retrieve reservations

    GET /reservations

### Predict sentiment

    POST /predict

## Technologies Used

-   Python
-   PyTorch
-   FastAPI or Flask
-   SQLite
-   HTML, CSS, JavaScript


pstaykov
https://github.com/pstaykov
