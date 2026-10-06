from fastapi import FastAPI
from routes import pharmacies, medicines, batches, sales, reports

app = FastAPI(title="Pharmacy API")
app.include_router(pharmacies.router, prefix="/pharmacies", tags=["pharmacies"])
app.include_router(medicines.router, prefix="/medicines", tags=["medicines"])
app.include_router(batches.router, prefix="/batches", tags=["batches"])
app.include_router(sales.router, prefix="/sales", tags=["sales"])
app.include_router(reports.router, prefix="/reports", tags=["reports"])

@app.get("/health")
def health(): return {"status": "ok"}
