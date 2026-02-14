

<<<<<<< HEAD

# 🏗 Architecture
=======
# Architecture
>>>>>>> 09474cd7857564de61ff6a05905edee92301de52

React Frontend → Flask REST API → Service Layer → PostgreSQL

------------------------------------------------------------------------




# 🛠 Backend Setup

cd backend\

## Create Virtual Environment

python -m venv venv\

venv\Scripts\activate

## Install Dependencies

pip install -r requirements.txt



## Configure Environment Variables

FLASK_APP=run.py
FLASK_ENV=development
DATABASE_URL=postgresql://user:password@localhost/dbname

## Run Migrations

flask db upgrade

## Start Server

python run.py

# runs at:
http://127.0.0.1:5000

<<<<<<< HEAD

# Ingest the Given JSON File

Assume the provided file is:

attempt_events.json

You must POST it to the ingest endpoint:

1.Using PowerShell
    run flask in a terminal
    open another terminal and open cd backend, the
            Invoke-RestMethod -Method POST `
            -Uri "http://127.0.0.1:5000/api/ingest" `
            -ContentType "application/json" `
            -InFile "sample_attempt.json"

2.Using curl
                curl -X POST http://127.0.0.1:5000/api/ingest \
        -H "Content-Type: application/json" \
        -d @sample_attempt.json


You can verify: GET http://127.0.0.1:5000/api/attempts
------------------------------------------------------------------------

#  Frontend Setup
=======
------------------------------------------------------------------------

# Frontend Setup
>>>>>>> 09474cd7857564de61ff6a05905edee92301de52

cd frontend\
npm install\
npm start

------------------------------------------------------------------------

<<<<<<< HEAD
#  Important APIs
=======
# 📡 Important APIs
>>>>>>> 09474cd7857564de61ff6a05905edee92301de52

GET /api/attempts\
GET /api/attempts/`<id>`{=html}\
POST /api/attempts/`<id>`{=html}/recompute\
POST /api/attempts/`<id>`{=html}/flag

GET /api/analytics/leaderboard?test_id=`<id>`{=html}

------------------------------------------------------------------------

