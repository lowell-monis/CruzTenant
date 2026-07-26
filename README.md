# CruzTenant 🏠⚖️
### Automated Eviction Protection & Lease Analyzer with Gemma 4
**Build with Gemma: Cruz Into The Gemmaverse! Kaggle Hackathon** | *Track 1: Autonomous Agent Track (Function Calling & APIs)*

---

## Overview

**CruzTenant** is an autonomous AI legal assistant powered by **Gemma 4 native function calling**. It empowers Santa Cruz renters, student commuters, and community advocates by automatically analyzing lease agreements, rent increase notices, and eviction threats against:
* **Santa Cruz Municipal Code Chapter 21.03** (Just Cause Eviction Protections & Mandatory Relocation Assistance)
* **Santa Cruz Municipal Code Chapter 21.04** (Rent Stabilization & Excessive Rent Increases)
* **California AB 1482** (Tenant Protection Act of 2019 - 5% + CPI Rent Increase Cap)
* **California AB 12** (Security Deposit Limits - Effective July 1, 2024)

---

## Key Features

1. **Native Gemma 4 Tool Execution Engine**: Registered schemas for 5 specialized tools (`calculate_max_allowed_rent_increase`, `verify_just_cause_eviction_notice`, `check_security_deposit_limit`, `query_santa_cruz_tenant_law`, `check_legal_aid_intake`).
2. **Transparent Tool Call Execution Trace**: Visualizes step-by-step agent thoughts, function arguments, tool outputs, and synthesis on a live timeline.
3. **Santa Cruz Rent Cap & Deposit Calculator**: Computes exact legal limits using Santa Cruz Metro CPI data (3.8% CPI + 5.0% base cap = **8.8% max allowed rent increase**).
4. **Formal Dispute Letter Exporter**: Generates ready-to-file, printable tenant dispute notices and connects users to Santa Cruz County Legal Aid intake.
5. **Kaggle Notebook Ready**: Includes a fully self-contained Kaggle notebook (`cruztenant_gemma_agent.ipynb`).

---

## Quick Start (Run Locally in < 1 Minute)

No complex package installation required! Built using Python standard libraries.

### 1. Launch Backend & Web Server
```bash
python server.py
```

### 2. Open Web Dashboard
Navigate to `http://localhost:8000` in your web browser.

---

## Repository Structure

```
C:\Users\lowel\cruzhacks\
├── server.py                   # Python web server & REST API handler
├── agent.py                    # Gemma 4 Autonomous Agent Core & Tool Execution Engine
├── santa_cruz_legal_db.py      # Santa Cruz Municipal Code & CA Law Rules Engine
├── cruztenant_gemma_agent.ipynb# Kaggle Competition Notebook
├── KAGGLE_WRITEUP.md           # Competition Writeup (Kaggle Template Formatted)
├── PITCH_AND_DEMO_SCRIPT.md    # 2-Minute Pitch Deck & Video Recording Script
├── README.md                   # Public Repository Documentation
└── public/                     # Web App Frontend Assets
    ├── index.html              # Single Page UI Structure
    ├── styles.css              # Glassmorphism Dark Theme Styling
    └── app.js                  # Frontend REST API Integration & Trace Visualizer
```

---

## License & Credits

Built for the **Build with Gemma: Cruz Into The Gemmaverse!** Kaggle Hackathon.  
Grounded in public Santa Cruz Municipal Code and California Civil Code.
