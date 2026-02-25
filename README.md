# In-Force Annuity Review Platform with AI Copilot

**IRI Hackathon 2026** - Proof of Concept

An intelligent platform for in-force annuity policy review, featuring AI-powered insights and compliance-aware replacement analysis.

---

## 🆕 **NEW: IARTS Standard**

**We've created a brand new industry standard for annuity replacement transactions!**

📋 **IARTS** (IRI Annuity Replacement Transaction Standard) is a modern, JSON-based payload format that replaces legacy ACORD XML for replacement transactions.

| Feature | ACORD XML | **IARTS** |
|---------|-----------|-----------|
| Format | XML | **JSON** |
| Size | 130+ lines | **65 lines (50% smaller)** |
| Transport | Batch EDI | **REST API** |
| Compliance | External | **Built-in** |
| AI-Ready | No | **Yes** ✨ |

**📚 Full Documentation:**
- [**IARTS Overview**](IARTS_STANDARD_OVERVIEW.md) - Executive summary with badges
- [**Full Specification**](REPLACEMENT_TRANSACTION_STANDARD.md) - Complete technical spec
- [**Quick Start Guide**](REPLACEMENT_TRANSACTION_QUICK_START.md) - Get started in 5 minutes
- [**ACORD Comparison**](ACORD_VS_IARTS_COMPARISON.md) - Side-by-side format comparison

**🚀 Try It:**
```bash
cd API
python example_replacement_transactions.py
```

---

## 🎯 Project Overview

This application helps financial advisors review in-force annuity policies with:
- **Automated Alert Detection** - Flags policies requiring review (Replacement Opportunities, Income Activation, Missing Info, Suitability Drift)
- **AI Copilot** - Contextual AI assistance for policy analysis and recommendations
- **Compliance Tools** - Built-in compliance workflows for suitability verification and replacement reviews
- **Product Comparison** - Smart product matching with side-by-side comparisons

## 🏗️ Architecture

### Frontend (Angular 19)
- **Framework**: Angular 19 with standalone components
- **UI Library**: Angular Material Design
- **State Management**: Angular Signals
- **Features**: Server-side rendering (SSR), Hot Module Replacement (HMR)

### Backend (FastAPI)
- **Framework**: FastAPI (Python)
- **Data Storage**: JSON files (for PoC - easily upgradeable to SQL/NoSQL)
- **AI Integration**: Pluggable AI providers (OpenAI, Claude, Mock)
- **API Docs**: Auto-generated Swagger/OpenAPI documentation

## 📁 Project Structure

```
IRIHackathon2026/
├── API/                            # FastAPI Backend
│   ├── app/
│   │   ├── api/                   # API endpoints (policies, clients, products, AI, replacement-transactions)
│   │   ├── models/                # Pydantic data models
│   │   │   └── replacement_transaction.py  # 🆕 IARTS Standard Models
│   │   └── services/              # Business logic (data store, product matching, AI)
│   ├── data/                      # Mock data (JSON files)
│   ├── main.py                    # FastAPI application entry point
│   ├── example_replacement_transactions.py  # 🆕 IARTS Examples
│   └── requirements.txt           # Python dependencies
│
├── UI/                            # Angular Frontend
│   ├── src/
│   │   ├── app/
│   │   │   ├── components/       # Policy Dashboard, Policy Detail Modal
│   │   │   ├── models/           # TypeScript interfaces
│   │   │   └── services/         # API service
│   │   └── styles.scss           # Global styles
│   ├── angular.json
│   └── package.json              # Node dependencies
│
├── wireframes/                    # UI mockups and designs
├── diagrams/                      # PlantUML diagrams
│
├── 🆕 IARTS_STANDARD_OVERVIEW.md         # IARTS executive summary
├── 🆕 REPLACEMENT_TRANSACTION_STANDARD.md # Full IARTS specification
├── 🆕 REPLACEMENT_TRANSACTION_QUICK_START.md # IARTS quick start
├── 🆕 ACORD_VS_IARTS_COMPARISON.md       # Format comparison
│
├── DEMO_SCRIPT.md                # Demo walkthrough script
├── Functional_and_Technical_Doc_Angular19_FastAPI.md
├── UI_Specs_Annuity_Review_AI_Copilot.md
└── README.md                     # This file
```

## 🚀 Quick Start

### Prerequisites

- **Node.js** 18.x or higher
- **Python** 3.10 or higher
- **Git**

### 1. Clone the Repository

```bash
git clone <repository-url>
cd IRIHackathon2026
```

### 2. Setup Backend (API)

```bash
# Navigate to API directory
cd API

# Create virtual environment (recommended)
python -m venv .venv

# Activate virtual environment
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the API server
python -c "import uvicorn; uvicorn.run('main:app', host='0.0.0.0', port=8000, reload=True)"
```

API will be available at:
- **API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

### 3. Setup Frontend (UI)

Open a new terminal:

```bash
# Navigate to UI directory
cd UI

# Install dependencies
npm install

# Run development server
ng serve
```

UI will be available at: **http://localhost:4200**

## 🎬 Using the Application

### Dashboard View
1. Navigate to http://localhost:4200
2. View policies grouped by client account
3. See alert badges (Replacement, Income Activation, Missing Info, Suitability Drift)
4. Click **Review** button to open Policy Detail Modal

### Policy Detail Modal
1. **Policy Overview** - View policy details, performance metrics, fees
2. **Alert Review Modules**:
   - **Replacement Opportunity**: 3-step workflow (Why Flagged → Verify Suitability → Review Alternatives)
   - **Income Activation**: Scenario comparison for income activation
   - **Missing Info**: DTCC Administrative API integration for non-financial updates
   - **Suitability Drift**: Change detection and re-verification

### AI Copilot
- Click **AI Copilot** button to get contextual insights
- Ask questions about policies, alternatives, or compliance requirements
- AI provides personalized recommendations based on client suitability

## 📚 API Endpoints

### Policies
- `GET /api/policies` - List all policies grouped by client
- `GET /api/policies/{policy_id}` - Get policy details

### Clients
- `GET /api/clients/{account_number}` - Get client with suitability profile
- `PATCH /api/clients/{account_number}/suitability` - Update suitability

### Products
- `GET /api/policies/{policy_id}/alternatives` - Get alternative products with comparison

### AI
- `POST /api/ai/chat` - Chat with AI Copilot (context-aware)

Full API documentation: http://localhost:8000/docs

## 🔧 Configuration

### Backend Configuration

Create `.env` file in `API/` directory (optional - defaults work for PoC):

```env
# AI Provider Configuration
AI_MOCK_MODE=True          # Use mock AI responses (set to False for real AI)
OPENAI_API_KEY=your-key    # If using OpenAI
CLAUDE_API_KEY=your-key    # If using Claude

# CORS Configuration
ALLOWED_ORIGINS=http://localhost:4200,http://localhost:59923
```

### Frontend Configuration

No configuration needed for local development. API URL is set to `http://localhost:8000/api` in `api.service.ts`.

## 🧪 Testing

### Test Backend
```bash
cd API
python test_api.py
```

### Test Frontend
```bash
cd UI
ng test
```

### Manual Testing
1. Start both servers (API + UI)
2. Navigate to http://localhost:4200
3. Click "Review" on any policy
4. Test each alert review workflow

## 📊 Sample Data

The application includes mock data for demonstration:

- **3 Client Accounts** with 9 policies total
- **Multiple Alert Types** across different policies
- **Client Suitability Profiles** with varied objectives and risk tolerances
- **Product Catalog** with 5+ alternative products

Data files located in `API/data/`:
- `clients_profile.json` - Client suitability profiles
- `policies.json` - In-force policies with alerts
- `products.json` - Product catalog
- `alerts_generated.json` - Pre-generated alerts

## 🎯 Key Features Demonstrated

✅ **Policy Dashboard** - Grouped view with alert summaries  
✅ **Policy Detail Modal** - Comprehensive policy review interface  
✅ **3-Step Replacement Workflow** - Why Flagged → Verify Suitability → Review Alternatives  
✅ **Product Comparison Table** - Side-by-side comparison of 3 alternatives  
✅ **Suitability Management** - View and edit client suitability profiles  
✅ **AI Copilot Integration** - Context-aware AI assistance (mock mode)  
✅ **Compliance Awareness** - Built-in disclaimers and regulatory guidance  
✅ **Responsive Design** - Material Design components with custom styling  

## 🔜 Future Enhancements

- Real AI integration (OpenAI/Claude)
- Database integration (PostgreSQL/MongoDB)
- User authentication and authorization
- Audit trail and compliance logging
- PDF report generation
- Email notifications
- Advanced filtering and search
- Mobile app (React Native/Flutter)

## 📖 Documentation

- **Demo Script**: [DEMO_SCRIPT.md](DEMO_SCRIPT.md)
- **Functional Specs**: [Functional_and_Technical_Doc_Angular19_FastAPI.md](Functional_and_Technical_Doc_Angular19_FastAPI.md)
- **UI Specs**: [UI_Specs_Annuity_Review_AI_Copilot.md](UI_Specs_Annuity_Review_AI_Copilot.md)

## 🤝 Contributing

This is a hackathon proof-of-concept. For production use:
1. Implement proper authentication/authorization
2. Add database with proper schemas
3. Add comprehensive error handling
4. Implement unit and integration tests
5. Add logging and monitoring
6. Security audit and penetration testing

## 📝 License

Proprietary - IRI Hackathon 2026

## 👥 Team

Built for IRI Hackathon 2026

---

**Note**: This is a proof-of-concept demonstration application. Not intended for production use without significant security, compliance, and architectural enhancements.
