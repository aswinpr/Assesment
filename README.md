

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
Database Tables-

attempts
<img width="1620" height="881" alt="attempts" src="https://github.com/user-attachments/assets/ebb8bab8-ed40-4831-93b4-a5a4ca3768a2" />

attempt_scores
<img width="1452" height="886" alt="attempt_scores" src="https://github.com/user-attachments/assets/44e1d9d6-0483-40f2-bbea-54805f3c69d2" />


students
<img width="1128" height="807" alt="students" src="https://github.com/user-attachments/assets/bb448130-0b17-4fa6-ae7e-6c078cb5ac38" />

flags
<img width="1211" height="598" alt="flags" src="https://github.com/user-attachments/assets/ca81ff31-0962-4cc1-9f1d-2c8064b6d161" />

tests
<img width="1353" height="548" alt="tests" src="https://github.com/user-attachments/assets/b44e18d8-1be8-4c02-ace2-2c3c52787f12" />
