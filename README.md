# ContribGuide AI

RAG pipeline helping first-time contributors understand open-source docs.

## Run backend
cd backend
pip install -r requirements.txt
cp .env.example .env  # set GOOGLE_API_KEY
uvicorn app.main:app --reload --port 8000

## Run frontend
cd frontend
npm install
npm run dev

## Tests
cd backend && pytest
