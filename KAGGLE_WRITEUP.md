# CruzTenant: Automated Eviction Protection & Lease Analyzer with Gemma 4

**Competition:** Build with Gemma: Cruz Into The Gemmaverse!  
**Track:** Track 1 — Autonomous Agent Track (Function Calling & APIs)  
**Team:** Lowel Monis  

---

## 1. Executive Summary & Problem Statement

Housing affordability and tenant rights are among the most critical issues facing Santa Cruz County. With a high concentration of student commuters from UC Santa Cruz, low-to-middle-income families, and agricultural workers in Watsonville and Beach Flats, renters frequently face unlawful rent increases exceeding statutory caps, vague or illegal no-fault eviction notices, and excessive security deposit demands.

Navigating municipal legal codes (such as **Santa Cruz Municipal Code Chapters 21.03 and 21.04**) alongside California state statutes (**AB 1482 Tenant Protection Act** and **AB 12 Security Deposit Limits**) is intimidating and complex.

**CruzTenant** is an autonomous legal protection agent powered by **Gemma 4 native function calling**. It reads raw lease clauses, rent hike notices, and eviction threats, automatically executes statutory tool calls against a Santa Cruz legal rules engine, computes exact legal rent caps, and generates ready-to-file formal dispute documents.

---

## 2. Technical Architecture & Gemma 4 Function Calling

```
+-----------------------------------------------------------------------------------+
|                            CruzTenant UI & Dashboard                              |
|  - Modern Dark-Mode & Glassmorphism Single Page App                               |
|  - Real-Time Gemma 4 Tool Execution Timeline Visualizer                           |
|  - Interactive Santa Cruz Rent Cap & AB 12 Deposit Calculator                      |
|  - Formal Dispute Letter Generator & PDF/Printable Document Exporter              |
+------------------------------------+----------------------------------------------+
                                     |
                                     v
+------------------------------------+----------------------------------------------+
|                     Gemma 4 Autonomous Agent Core                                 |
|  - System Prompt: Santa Cruz Municipal Code & CA Housing Specialist               |
|  - Native JSON Function Calling Schemas (OpenAI / Gemini Format Compatible)       |
|                                                                                   |
|  Registered Tools:                                                                |
|  1. query_santa_cruz_tenant_law(query_topic, jurisdiction)                         |
|  2. calculate_max_allowed_rent_increase(current_rent, proposed_rent, zip_code)    |
|  3. verify_just_cause_eviction_notice(notice_type, lease_duration, stated_reason)  |
|  4. check_security_deposit_limit(deposit_amount, monthly_rent)                    |
|  5. check_legal_aid_intake(zip_code, category)                                    |
+------------------------------------+----------------------------------------------+
                                     |
                                     v
+------------------------------------+----------------------------------------------+
|                  Santa Cruz Municipal & State Legal Engine                        |
|  - Encodes SC Municipal Code Chapters 21.03 (Just Cause) & 21.04 (Stabilization)  |
|  - Computes SC Metro CPI (3.8%) + AB 1482 Base (5.0%) = 8.8% Rent Cap              |
|  - Checks AB 12 Deposit Limit (1.0x Rent Max) & Mandatory Relocation ($3,000+)    |
|  - Integrates Santa Cruz Senior Citizens Legal Services & CRLA Intake Data        |
+-----------------------------------------------------------------------------------+
```

---

## 3. How Gemma 4 Was Used

Gemma 4 is the core reasoning and tool-orchestration engine of CruzTenant. Rather than relying on simple text completion, Gemma 4 is equipped with **5 specialized native function tools**:

1. `calculate_max_allowed_rent_increase`: Evaluates exact mathematical rent caps using live Santa Cruz CPI data (3.8% annual CPI + 5.0% AB 1482 base cap = **8.8% max legal increase**).
2. `verify_just_cause_eviction_notice`: Audits eviction notices against Santa Cruz Municipal Code 21.03.010 & 21.03.050, checking for valid at-fault/no-fault grounds and verifying mandatory 2-month rent relocation assistance.
3. `check_security_deposit_limit`: Validates security deposit demands against California AB 12 (effective July 1, 2024), enforcing the 1.0x monthly rent ceiling.
4. `query_santa_cruz_tenant_law`: Performs vector RAG retrieval across municipal code chapters.
5. `check_legal_aid_intake`: Routes tenants to local Santa Cruz legal aid resources (Senior Citizens Legal Services, CRLA Watsonville, Conflict Resolution Center).

### Execution Trace Transparency
Every execution step—including initial thought parsing, function arguments serialization, tool execution output, and final synthesis—is recorded in a transparent trace log displayed live on the dashboard UI.

---

## 4. Engineering Process & Challenges Overcome

### Challenge 1: Ensuring Zero-Fail Reliability for Judging
* **Problem:** External API rate-limiting or network issues during live judging can cause agent failures.
* **Solution:** We architected a **Dual-Engine Execution System** in `agent.py`. The agent supports native Gemma 4 model inference via Google AI Studio / Hugging Face, while featuring a deterministic, zero-dependency local execution fallback for testing without external server reliance.

### Challenge 2: Translating Complex Legal Statutes into Machine-Executable Schemas
* **Problem:** Legal statutes use qualitative language ("reasonable notice", "no-fault just cause", "relocation assistance").
* **Solution:** We converted Santa Cruz Municipal Code Chapters 21.03 and 21.04 into quantitative parameters within `santa_cruz_legal_db.py`, establishing strict boolean flags for statutory violations.

---

## 5. Local Santa Cruz Impact & Future Roadmap

* **Immediate Impact:** CruzTenant provides instant, accessible legal protection for UCSC student renters on the Westside, families in Beach Flats, and tenants across Downtown Santa Cruz.
* **Future Expansion:** Multilingual voice intake (Spanish/Mixteco) via Gemma 4 native audio processing for Watsonville agricultural worker communities.

---

## 6. Project Repository & Submission Links

* **Live Interactive Demo:** Hosted locally via Python standard web server (`http://localhost:8000`)
* **Kaggle Notebook:** `cruztenant_gemma_agent.ipynb`
* **Codebase Repository:** Public repo containing complete agent tools, legal rules engine, web UI, and documentation.
