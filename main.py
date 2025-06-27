from fastapi import FastAPI, HTTPException
from typing import List, Optional
import pandas as pd
from rapidfuzz import fuzz, process
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can restrict to your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)




# Load and clean CSV
df = pd.read_csv(r"./Data/Retail Price Information.csv")

# Clean column names
df.columns = [col.strip().replace(" ", "_").replace(".", "") for col in df.columns]


# Fill NaN with empty strings and ensure all fields are strings
df = df.fillna("").astype(str)


# Convert DataFrame to list of dicts
medicines_data = df.to_dict(orient="records")

@app.get("/")
def read_root():
    return {"message": "Welcome to the Medicines API"}

@app.get("/api/medicines", response_model=List[dict])
def get_all_medicines():
    return medicines_data

@app.get("/api/medicine/{serial_no}")
def get_medicine_by_serial(serial_no: int):
    for item in medicines_data:
        if item["SNo"] == serial_no:
            return item
    raise HTTPException(status_code=404, detail="Medicine not found")

@app.get("/api/search")
def search_medicine(name: Optional[str] = None,
                    manufacturer: Optional[str] = None,
                    marketing_company: Optional[str] = None,
                    threshold: int = 70):
    results = []

    for med in medicines_data:
        match_score = 0
        matched = True

        if name:
            if fuzz.partial_ratio(name.lower(), med["Medicines"].lower()) >= threshold:
                match_score += 1
            else:
                matched = False

        if manufacturer:
            if fuzz.partial_ratio(manufacturer.lower(), med["Manufacturer_Name"].lower()) >= threshold:
                match_score += 1
            else:
                matched = False

        if marketing_company:
            if fuzz.partial_ratio(marketing_company.lower(), med["Marketing_Company"].lower()) >= threshold:
                match_score += 1
            else:
                matched = False

        if matched:
            med_copy = med.copy()
            med_copy["match_score"] = match_score
            results.append(med_copy)

    if not results:
        raise HTTPException(status_code=404, detail="No matching medicines found")

    # Sort results by highest match_score
    return sorted(results, key=lambda x: x["match_score"], reverse=True)


@app.get("/api/fuzzy-search")
def fuzzy_search(name: Optional[str] = None, threshold: int = 70):
    if not name:
        raise HTTPException(status_code=400, detail="Name query is required")

    results = []
    for med in medicines_data:
        score = fuzz.partial_ratio(name.lower(), med["Medicines"].lower())
        if score >= threshold:
            med_copy = med.copy()
            med_copy["match_score"] = score
            results.append(med_copy)

    if not results:
        raise HTTPException(status_code=404, detail="No similar medicine names found")

    return sorted(results, key=lambda x: x["match_score"], reverse=True)