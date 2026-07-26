# CruzTenant — 2-Minute Hackathon Demo & Pitch Script

**Event:** Build with Gemma: Cruz Into The Gemmaverse!  
**Track:** Track 1 — Autonomous Agent Track (Function Calling & APIs)  
**Project:** CruzTenant — Automated Eviction Protection & Lease Analyzer  

---

## 🎬 Video Script & Screen Recording Guide (2 Minutes)

### [0:00 - 0:25] The Problem & Santa Cruz Housing Context
* **Visual:** Show Santa Cruz map / UCSC campus / Downtown Pacific Ave.
* **Speaker Script:**
  > "Hi everyone, I'm presenting **CruzTenant**, an autonomous AI agent built with **Gemma 4** for the Cruz Into The Gemmaverse hackathon.
  >
  > In Santa Cruz, housing insecurity is an urgent crisis. UCSC students, working families, and renters constantly deal with sky-high rents, sudden eviction notices, and excessive deposit demands. Most tenants don't know that Santa Cruz Municipal Code Chapter 21.04 caps rent hikes at 5% plus local CPI, or that California AB 12 caps security deposits at one month's rent.
  >
  > That's why we built CruzTenant."

---

### [0:25 - 1:15] Live Demo: Gemma 4 Tool Calling Execution
* **Visual:** Open CruzTenant Web Dashboard (`http://localhost:8000`). Click on **Sample Case 1: Downtown SC Excessive 18% Rent Hike**. Click **Analyze with Gemma 4 Agent**.
* **Speaker Script:**
  > "Let's see CruzTenant in action. Here we have a realistic scenario from Downtown Santa Cruz: a tenant whose rent was raised by 18% from $2,800 to $3,304 per month.
  >
  > When I click 'Analyze', Gemma 4 doesn't just output generic text. It autonomously invokes specialized function tools:
  > 1. `calculate_max_allowed_rent_increase` checks Santa Cruz Metro CPI (3.8%) + AB 1482 base (5.0%) = 8.8% max cap.
  > 2. It calculates that the maximum legal rent is $3,046.40, revealing an illegal monthly overcharge of $253.60.
  > 3. `check_legal_aid_intake` fetches local Santa Cruz Senior Citizens Legal Services and CRLA contacts."

---

### [1:15 - 1:45] Instant Formal Dispute Document Exporter
* **Visual:** Scroll down to show the generated **Formal Dispute Document** and click **Print / Export Letter**. Show another sample case (Beach Flats Unlawful Eviction with $0 relocation).
* **Speaker Script:**
  > "Crucially, CruzTenant goes beyond diagnosis. It immediately generates a legally grounded, ready-to-file Formal Dispute Notice citing Santa Cruz Municipal Code Chapters 21.03 and 21.04 that the tenant can print or email to their landlord within seconds.
  >
  > It also detects unlawful eviction notices that fail to provide Santa Cruz's mandatory 2-month relocation assistance."

---

### [1:45 - 2:00] Summary & Submission Wrap-Up
* **Visual:** Show Kaggle Notebook `cruztenant_gemma_agent.ipynb` and architecture diagram.
* **Speaker Script:**
  > "CruzTenant combines deep local municipal impact with Gemma 4's powerful native tool-calling capabilities. Our complete submission includes this live web dashboard, a fully functional Kaggle Notebook, and well-documented public code.
  >
  > Thank you!"
