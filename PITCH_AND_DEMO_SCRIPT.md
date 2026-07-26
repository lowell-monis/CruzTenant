# CruzTenant — Pitch and Presentation Script

**Project:** CruzTenant — Autonomous Santa Cruz Tenant Rights & Lease Auditor  
**Hackathon:** CruzHacks Build with Gemma: Cruz Into The Gemmaverse!  
**Track:** Track 1 — Autonomous Agent Track  
**Presenter:** Lowell Monis  

---

## 🎙️ 3-Minute Demo Script

### 1. Introduction & The Santa Cruz Housing Problem (0:00 - 0:45)
"Hi everyone, I'm **Lowell Monis**, and I'm excited to present **CruzTenant** — an autonomous AI legal defense agent built for Santa Cruz renters for CruzHacks Track 1.

Santa Cruz renters face some of the highest housing costs in California, governed by strict local tenant protection ordinances under Santa Cruz Municipal Code Chapters 21.03 and 21.04. However, when tenants receive unlawful rent hike notices, illegal eviction demands, or lease terms banning them from reporting black mold to city inspectors, they rarely have immediate access to legal advice.

CruzTenant solves this by giving every Santa Cruz tenant an autonomous legal defense agent powered by **Gemma 4 function calling**."

---

### 2. Live Demo & Gemma 4 Tool Engine (0:45 - 2:00)
"Let's look at a live demonstration:

1. **Scenario 1 — Rent Hike Violation**:
   - We select a tenant in Downtown Santa Cruz paying $2,800/month who receives an 18% rent hike to $3,304/month.
   - CruzTenant executes `calculate_max_allowed_rent_increase`.
   - The agent calculates the 8.8% legal cap (5.0% base + 3.8% Santa Cruz CPI = $3,046.40 max legal rent) and identifies a statutory monthly overcharge of $257.60.

2. **Scenario 2 — Unlawful Eviction & Relocation**:
   - A Beach Flats tenant of 3 years receives a 60-day notice to vacate for owner renovations with $0 relocation assistance.
   - CruzTenant executes `verify_just_cause_eviction_notice`, flagging violations of SC Municipal Code 21.03.050 for missing mandatory relocation assistance ($3,000 minimum).

3. **Scenario 3 — Security Deposit Ceiling**:
   - A UCSC student near Seabright is asked for a 2-month security deposit ($5,600).
   - CruzTenant executes `check_security_deposit_limit`, asserting California AB 12's 1-month ceiling.

4. **Scenario 4 — Retaliatory Lease Clause & Black Mold**:
   - A Westside lease clause threatens immediate eviction if the tenant reports plumbing leaks or black mold to City Code Enforcement.
   - CruzTenant executes `verify_habitability_and_retaliation`, declaring the reporting ban void under CA Civil Code § 1953 and citing habitability breaches under § 1941.1."

---

### 3. Output & Legal Aid Intake (2:00 - 2:45)
"In every case, CruzTenant:
- Renders an inspection trace showing Gemma 4's tool execution.
- Generates a formal, ready-to-file legal dispute document citing Santa Cruz Municipal Code.
- Matches the tenant directly to verified local Santa Cruz legal aid resources like **Senior Citizens Legal Services**, **CRLA**, **Conflict Resolution Center**, and the **Santa Cruz Law Library**."

---

### 4. Conclusion & Legal Disclaimer (2:45 - 3:00)
"CruzTenant empowers Santa Cruz renters with immediate, grounded statutory protection. 

*Legal Disclaimer: CruzTenant is an automated educational AI tool powered by Gemma 4 and is not a replacement for formal legal counsel. Licensed attorneys and verified Santa Cruz legal aid contacts are linked directly in the platform.*

Thank you!"
