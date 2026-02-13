


# 🏗 Architecture

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

------------------------------------------------------------------------

#  Frontend Setup

cd frontend\
npm install\
npm start

------------------------------------------------------------------------

#  Important APIs

GET /api/attempts\
GET /api/attempts/`<id>`{=html}\
POST /api/attempts/`<id>`{=html}/recompute\
POST /api/attempts/`<id>`{=html}/flag

GET /api/analytics/leaderboard?test_id=`<id>`{=html}

------------------------------------------------------------------------

