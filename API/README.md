# Annuity Review API - FastAPI Backend

## Hackathon PoC - February 2026

Backend API for the In-Force Annuity Review Platform with AI Copilot.

## Features Implemented

✅ **Policy Listing API** - Returns policies grouped by client account with alert summaries
✅ **Policy Detail API** - Returns complete policy information for modal view
✅ **Client API** - Returns client information and suitability profile
✅ **Suitability Update API** - Updates client suitability fields
✅ **Mock Data** - Sample policies with multiple alert types (Replacement, Income Activation, Suitability Drift)

## Quick Start

### 1. Install Dependencies

```bash
# Create virtual environment (recommended)
python -m venv .venv

# Activate virtual environment
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Run the Server

```bash
# From the API directory
uvicorn main:app --reload --port 8000
```

The API will be available at: `http://localhost:8000`

Interactive API docs (Swagger UI): `http://localhost:8000/docs`

Alternative docs (ReDoc): `http://localhost:8000/redoc`

## API Endpoints

### Policies

- **GET `/api/policies`** - Get all policies grouped by client account
  - Returns: List of `ClientPoliciesGroup` with alert counts
  - Use this for the Policy Listing Dashboard

- **GET `/api/policies/{policy_id}`** - Get policy detail
  - Returns: Complete `Policy` object with all alerts
  - Use this when opening Policy Detail Modal

- **GET `/api/clients/{client_account_number}/policies`** - Get all policies for a client
  - Returns: List of `PolicySummary` objects

### Clients

- **GET `/api/clients/{client_account_number}`** - Get client with suitability profile
  - Returns: `ClientWithSuitability` object
  - Use this for suitability verification in Replacement module

- **PATCH `/api/clients/{client_account_number}/suitability`** - Update client suitability
  - Body: `SuitabilityUpdateRequest`
  - Returns: Updated `ClientWithSuitability`

### Health Check

- **GET `/`** - Basic health check
- **GET `/health`** - Detailed health check

## Data Structure

### Sample Policy Listing Response (GET /api/policies)

```json
[
  {
    "clientAccountNumber": "101-123456-001",
    "clientName": "Milovich Pichirallo",
    "policies": [
      {
        "policyId": "POL-90002",
        "policyLabel": "Lincoln FIA (2016)",
        "carrier": "Lincoln",
        "productType": "FIA",
        "accountValue": 472350.93,
        "renewalDays": 15,
        "currentCapRate": 3.9,
        "renewalCapRate": 3.4,
        "alerts": [
          {
            "alertId": "ALT-POL-90002-REPL",
            "type": "REPLACEMENT",
            "severity": "HIGH",
            "title": "Replacement Opportunity",
            "reasonShort": "Renewal in 15 days; cap drops from 3.9% to 3.4%"
          }
        ]
      }
    ],
    "totalAlerts": 2,
    "highSeverityCount": 1,
    "mediumSeverityCount": 1,
    "lowSeverityCount": 0
  }
]
```

## Mock Data

The API uses JSON files for data:
- `data/clients_profile.json` - Client information and suitability profiles
- `data/policies.json` - Policy details with alerts

### Alert Types in Mock Data

- **REPLACEMENT** (HIGH) - Renewal opportunities, cap rate drops
- **INCOME_ACTIVATION** (MEDIUM) - Income rider available but not activated
- **SUITABILITY_DRIFT** (LOW/MEDIUM) - Life stage or objective changes

## Development

### Project Structure

```
API/
├── main.py                 # FastAPI app entry point
├── app/
│   ├── __init__.py
│   ├── config.py          # Settings and configuration
│   ├── api/               # API route handlers
│   │   ├── policies.py
│   │   └── clients.py
│   ├── models/            # Pydantic models
│   │   ├── alert.py
│   │   ├── client.py
│   │   └── policy.py
│   └── services/          # Business logic services
│       └── data_store.py
├── data/                  # Mock JSON data
│   ├── clients_profile.json
│   └── policies.json
├── requirements.txt
└── README.md
```

### Running Tests

```bash
# Test the main policy listing endpoint
curl http://localhost:8000/api/policies

# Test specific policy detail
curl http://localhost:8000/api/policies/POL-90002

# Test client endpoint
curl http://localhost:8000/api/clients/101-123456-001
```

## Next Steps for Hackathon

- [ ] Add AI chat endpoint (`POST /api/ai/chat`)
- [ ] Implement market alternatives endpoint (`GET /api/policies/{policy_id}/alternatives`)
- [ ] Add audit logging (optional)
- [ ] Implement alert engine service for dynamic alert generation

## CORS Configuration

The API is configured to allow requests from:
- `http://localhost:4200` (Angular dev server)
- `http://localhost:3000`

Update `app/config.py` to add more origins if needed.

## License

Hackathon PoC - Internal Use Only
