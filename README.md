
# 💊 Medicines Price API

A simple FastAPI server that reads medicine price and formulation data from a CSV file and exposes RESTful endpoints with fuzzy search capabilities.

---

## 🛠️ Features

- Load and serve medicine pricing data from CSV
- Get all medicines
- Retrieve medicine by serial number
- Search medicines by name, manufacturer, or marketing company (with fuzzy matching)
- Dedicated fuzzy name search
- FastAPI Swagger UI for interactive documentation

---

## 📁 Project Structure

```
medicine-api/
├── Data/
│   └── Retail Price Information.csv
├── main.py
├── venv/ (your virtual environment)
└── README.md
```

---

## ⚙️ Setup Instructions

### 1. Clone the repo

```bash
git clone https://github.com/yourusername/medicine-api.git
cd medicine-api
```

### 2. Create & activate a virtual environment

```bash
# Create virtualenv
python3 -m venv venv

# Activate virtualenv (Linux/macOS)
source venv/bin/activate

# On Windows:
# venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install fastapi uvicorn pandas rapidfuzz
```

---

## ▶️ Run the API Server

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Now visit:  
**[http://localhost:8000/docs](http://localhost:8000/docs)** for interactive Swagger documentation.

---

## 📌 API Endpoints

### ✅ Root

**GET /**  
**Description**: Welcome message  
**Response**:
```json
{ "message": "Welcome to the Medicines API" }
```

---

### ✅ Get All Medicines

**GET /api/medicines**  
**Response**: List of all medicine records (as JSON array)

---

### ✅ Get Medicine by Serial Number

**GET /api/medicine/{serial_no}**

**Example**:
```http
GET /api/medicine/2
```

**Response**:
```json
{
  "SNo": "2",
  "Medicines": "Cetrizine HCl+ Ambroxol HCl",
  ...
}
```

---

### ✅ Search with Fuzzy Matching

**GET /api/search**

**Query Params**:
- `name`: (optional) medicine name
- `manufacturer`: (optional) manufacturer name
- `marketing_company`: (optional) marketing company name
- `threshold`: (optional, default `70`) match confidence threshold

**Example**:
```http
GET /api/search?name=ometrazol&manufacturer=gujrat
```

**Response**:
Sorted list of matching medicines with `match_score`.

---

### ✅ Fuzzy Search by Name

**GET /api/fuzzy-search**

**Query Params**:
- `name`: (required) fuzzy match against `Medicines` field
- `threshold`: (optional, default `70`)

**Example**:
```http
GET /api/fuzzy-search?name=glibenclamaid
```

**Response**:
List of best fuzzy matches with match scores.

---

## 🧪 Testing

Use Swagger at:

```
http://localhost:8000/docs
```

Or test with cURL/Postman using the endpoints above.

---

## 📄 Requirements

Create a `requirements.txt` using:

```bash
pip freeze > requirements.txt
```

Or manually:

```
fastapi
uvicorn
pandas
rapidfuzz
```

---

## 🛰️ Deployment (Optional)

You can deploy using:

- [Render](https://render.com/)
- [Railway](https://railway.app/)
- [Deta](https://deta.space/)
- Docker (add a Dockerfile if needed)

---

## 📌 License

MIT License (or your preferred license)

---

## ✨ Author

**Susovan Das**  
Email: suvo.codes15@gmail.com 

LinkedIn: [linkedin.com/in/susovan-das-66503a298/](https://www.linkedin.com/in/susovan-das-66503a298/)
---
