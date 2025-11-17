import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Any, Dict
from datetime import datetime, timezone

from database import db, create_document, get_documents
from schemas import Inquiry, Appointment

app = FastAPI(title="Solace Counselling API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Solace Counselling Backend is running"}

@app.get("/api/hello")
def hello():
    return {"message": "Hello from Solace Counselling API"}

@app.get("/test")
def test_database():
    """Test endpoint to check if database is available and accessible"""
    response: Dict[str, Any] = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }

    try:
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Configured"
            response["database_name"] = db.name if hasattr(db, 'name') else "✅ Connected"
            response["connection_status"] = "Connected"
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️  Available but not initialized"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"

    import os as _os
    response["database_url"] = "✅ Set" if _os.getenv("DATABASE_URL") else "❌ Not Set"
    response["database_name"] = "✅ Set" if _os.getenv("DATABASE_NAME") else "❌ Not Set"

    return response

# Public endpoints for website forms
@app.post("/api/inquiries")
def create_inquiry(payload: Inquiry):
    try:
        data = payload.model_dump()
        data["submitted_at"] = datetime.now(timezone.utc)
        inserted_id = create_document("inquiry", data)
        return {"status": "ok", "id": inserted_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/appointments")
def create_appointment(payload: Appointment):
    try:
        data = payload.model_dump()
        data["submitted_at"] = datetime.now(timezone.utc)
        inserted_id = create_document("appointment", data)
        return {"status": "ok", "id": inserted_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Simple list endpoints (limited) for admin/testing
@app.get("/api/inquiries")
def list_inquiries(limit: int = 20):
    try:
        docs = get_documents("inquiry", limit=limit)
        for d in docs:
            d["_id"] = str(d.get("_id"))
        return docs
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/appointments")
def list_appointments(limit: int = 20):
    try:
        docs = get_documents("appointment", limit=limit)
        for d in docs:
            d["_id"] = str(d.get("_id"))
        return docs
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Schema exposure for tooling
class _SchemaResponse(BaseModel):
    schemas: Dict[str, Any]

@app.get("/schema")
def get_schema():
    return {
        "schemas": {
            "Inquiry": Inquiry.model_json_schema(),
            "Appointment": Appointment.model_json_schema(),
        }
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
