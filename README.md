# CruzTenant — Autonomous Santa Cruz Tenant Rights & Lease Auditor

**Built for CruzHacks: Build with Gemma: Cruz Into The Gemmaverse!**  
**Track:** Track 1 — Autonomous Agent Track  
**Developer:** Lowell Monis  
**Project Repository:** [https://github.com/lowell-monis/CruzTenant](https://github.com/lowell-monis/CruzTenant)  
**Live Demo:** [https://lowell-monis.github.io/CruzTenant](https://lowell-monis.github.io/CruzTenant)  
**Kaggle Writeup:** [https://www.kaggle.com/competitions/cruz-into-the-gemmaverse/writeups](https://www.kaggle.com/competitions/cruz-into-the-gemmaverse/writeups)  

---

## 📌 Executive Summary & Mission
In Santa Cruz County, renters face one of the highest cost-of-living burdens in the United States alongside complex municipal tenant ordinances (Santa Cruz Municipal Code Chapters 21.03 and 21.04). Most tenants lack immediate access to affordable legal representation when served with illegal rent hikes, unlawful eviction notices, or retaliatory defect reporting bans.

**CruzTenant** is an autonomous AI legal defense agent powered by **Gemma 4 function calling**. It audits lease documents, rent increase notices, and eviction letters against Santa Cruz Municipal Code and California state housing statutes, automatically generating formal, ready-to-file legal dispute documents and matching tenants to verified local Santa Cruz legal aid resources.

---

## 🛠️ Key Agentic Features & Architecture

### 1. Gemma 4 Native Function-Calling Engine
CruzTenant uses 6 structured function tool declarations to execute deterministic legal audits against the Santa Cruz Municipal Code database:
- `calculate_max_allowed_rent_increase`: Enforces the 8.8% annual cap (5.0% base + 3.8% Santa Cruz Metro CPI) under SC Municipal Code Ch. 21.04 and California AB 1482.
- `verify_just_cause_eviction_notice`: Audits notices to vacate under SC Municipal Code Ch. 21.03 for mandatory just cause reasons and statutory relocation assistance ($3,000 / 2 months rent minimum).
- `check_security_deposit_limit`: Validates security deposits against California AB 12 (1.0x monthly rent limit effective July 2024).
- `verify_habitability_and_retaliation`: Audits lease terms for void retaliatory defect reporting bans (CA Civil Code § 1953) and severe habitability breaches (CA Civil Code § 1941.1).
- `check_legal_aid_intake`: Retrieves verified local Santa Cruz County legal aid organization contacts and intake eligibility requirements.
- `generate_custom_dispute_document`: Dynamically drafts tailored formal dispute letters citing governing municipal codes.

### 2. Verified Santa Cruz Legal Aid Intake Matching
When an audit is performed, CruzTenant matches the tenant's specific situation to verified local Santa Cruz County legal assistance providers:
- **Senior Citizens Legal Services — Santa Cruz** (Seniors & low-income rent dispute assistance)
- **California Rural Legal Assistance (CRLA) — Watsonville/Santa Cruz** (Tenant rights & substandard housing litigation)
- **Conflict Resolution Center of Santa Cruz County** (Landlord-tenant mediation & dispute resolution)
- **Santa Cruz County Law Library Tenant Self-Help** (Public legal form filing & municipal code research)

---

## 🚀 Environment Setup & Local Execution

### Running with `uv` (Synced & Lockfile Ready)
1. Clone the repository:
   ```bash
   git clone https://github.com/lowell-monis/CruzTenant.git
   cd CruzTenant
   ```
2. Sync virtual environment using `uv`:
   ```bash
   uv sync
   ```
3. Run the application:
   ```bash
   uv run python server.py
   ```
4. Open **[http://localhost:8000](http://localhost:8000)** in your browser.

### Standard Python Setup (Local Fallback)
1. Install Python 3.9+:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
2. Create a `.env` file in the project root:
   ```env
   GEMINI_API_KEY=your_google_ai_studio_api_key_here
   ```
3. Start the server:
   ```bash
   python server.py
   ```
4. Open **[http://localhost:8000](http://localhost:8000)**.

---

## 🌐 GitHub Deployment Instructions

### 1. Push to GitHub
Initialize and push your local repository to your GitHub account:
```bash
git remote add origin https://github.com/lowell-monis/CruzTenant.git
git branch -M main
git push -u origin main
```

### 2. Enable GitHub Pages Deployment
1. Go to your repository settings on GitHub: **Settings > Pages**.
2. Under **Build and deployment > Source**, select **GitHub Actions**.
3. The included GitHub Actions workflow (`.github/workflows/deploy.yml`) will automatically deploy the static frontend to **`https://lowell-monis.github.io/CruzTenant`** on every push to `main`!

---

## ⚖️ Legal Disclaimer & Trademark Attribution
> **LEGAL DISCLAIMER:** CruzTenant is an automated AI educational tool built by Lowell Monis for CruzHacks and powered by Gemma 4. It is not a substitute for formal legal representation or advice. For official legal counsel or litigation defense, please consult a licensed attorney or a verified Santa Cruz legal aid organization listed in the application.

*Gemma is a trademark of Google LLC.*
