"""
santa cruz municipal code and California tenant law rules engine.
"""

from typing import Dict, Any, List, Optional
import datetime

CURRENT_SANTA_CRUZ_CPI = 3.8
AB1482_BASE_CAP = 5.0
MAX_ALLOWED_RENT_INCREASE_PERCENT = AB1482_BASE_CAP + CURRENT_SANTA_CRUZ_CPI

SANTA_CRUZ_MUNICIPAL_CODES = {
    "21.03.010": {
        "title": "Santa Cruz just cause eviction protections",
        "description": "landlords must provide a valid at-fault or no-fault just cause reason to terminate tenancy for tenants occupying a property for 12+ months.",
        "jurisdiction": "City of Santa Cruz",
        "at_fault_reasons": [
            "nonpayment of rent",
            "material breach of lease terms after written notice to cure",
            "nuisance or illegal activity on premises",
            "refusal to execute written extension of lease with similar terms"
        ],
        "no_fault_reasons": [
            "owner or owner's immediate family intent to occupy",
            "substantial rehabilitation or demolition of property",
            "withdrawal of residential rental unit from rental market (Ellis Act)",
            "compliance with government or court order to vacate"
        ]
    },
    "21.03.050": {
        "title": "mandatory relocation assistance for no-fault eviction",
        "description": "no-fault eviction terminations in Santa Cruz require relocation assistance equal to 2 months rent or $3,000, whichever is greater.",
        "jurisdiction": "City of Santa Cruz",
        "relocation_multiplier_months": 2,
        "minimum_relocation_usd": 3000
    },
    "21.04.020": {
        "title": "rent stabilization and excessive rent increase notice",
        "description": "rent increases exceeding 5% + CPI (8.8% total) within any 12-month period trigger 90-day written notice and tenant mediation rights.",
        "max_allowable_annual_increase_pct": MAX_ALLOWED_RENT_INCREASE_PERCENT,
        "required_notice_days_large_increase": 90,
        "required_notice_days_standard": 30
    },
    "CA_AB_12": {
        "title": "California AB 12 security deposit limits",
        "description": "security deposits are restricted to a maximum of 1 month rent for residential leases starting July 1, 2024.",
        "effective_date": "2024-07-01",
        "max_deposit_months": 1.0,
        "small_landlord_exception": "landlords owning <= 2 properties with <= 4 total units may collect up to 2 months rent."
    },
    "CA_AB_1482": {
        "title": "California Tenant Protection Act of 2019 (AB 1482)",
        "description": "statewide rent cap (5% + local CPI) and just cause eviction protections.",
        "base_cap_pct": 5.0,
        "max_overall_cap_pct": 10.0
    }
}

SANTA_CRUZ_LEGAL_AID_RESOURCES = [
    {
        "name": "Senior Citizens Legal Services - Santa Cruz",
        "address": "501 Soquel Ave, Suite F, Santa Cruz, CA 95062",
        "phone": "(831) 426-8824",
        "services": ["eviction defense", "rent increase disputes", "housing discrimination"],
        "eligibility": "Santa Cruz County residents aged 60+ or low-income households"
    },
    {
        "name": "California Rural Legal Assistance (CRLA) - Watsonville/Santa Cruz",
        "address": "21 Carr St, Watsonville, CA 95076",
        "phone": "(831) 724-2253",
        "services": ["tenant rights", "substandard housing litigation", "unlawful detainer defense"],
        "eligibility": "low-income tenants and agricultural workers in Santa Cruz County"
    },
    {
        "name": "Conflict Resolution Center of Santa Cruz County",
        "address": "147 S River St, Suite 206, Santa Cruz, CA 95060",
        "phone": "(831) 475-6117",
        "services": ["landlord-tenant mediation", "rent dispute settlement"],
        "eligibility": "Santa Cruz County landlords and tenants"
    },
    {
        "name": "Santa Cruz County Law Library Tenant Self-Help",
        "address": "701 Ocean Street, Room 080, Santa Cruz, CA 95060",
        "phone": "(831) 457-2525",
        "services": ["legal form filing", "tenant answer assistance", "municipal code research"],
        "eligibility": "public access"
    }
]

def query_tenant_law(query_topic: str, jurisdiction: str = "Santa Cruz") -> Dict[str, Any]:
    """queries Santa Cruz and California tenant protection laws for a topic."""
    query_lower = query_topic.lower()
    matches = []
    
    for code, details in SANTA_CRUZ_MUNICIPAL_CODES.items():
        searchable_text = f"{code} {details['title']} {details['description']}".lower()
        if any(term in searchable_text for term in query_lower.split()):
            matches.append({"code": code, **details})
            
    if not matches:
        matches = [
            {"code": "21.04.020", **SANTA_CRUZ_MUNICIPAL_CODES["21.04.020"]},
            {"code": "21.03.010", **SANTA_CRUZ_MUNICIPAL_CODES["21.03.010"]}
        ]
        
    return {
        "status": "success",
        "query": query_topic,
        "jurisdiction": jurisdiction,
        "matched_statutes_count": len(matches),
        "statutes": matches,
        "current_sc_cpi_rate": CURRENT_SANTA_CRUZ_CPI,
        "max_allowable_rent_increase_percentage": MAX_ALLOWED_RENT_INCREASE_PERCENT
    }

def calculate_rent_cap(current_rent: float, proposed_rent: float, zip_code: str = "95060") -> Dict[str, Any]:
    """calculates if proposed rent increase exceeds Santa Cruz CPI + AB 1482 limits."""
    dollar_increase = proposed_rent - current_rent
    percent_increase = (dollar_increase / current_rent) * 100.0 if current_rent > 0 else 0.0
    
    max_allowed_percent = MAX_ALLOWED_RENT_INCREASE_PERCENT
    max_allowed_dollar_increase = current_rent * (max_allowed_percent / 100.0)
    max_legal_rent = current_rent + max_allowed_dollar_increase
    
    is_excessive = percent_increase > max_allowed_percent
    excess_amount_monthly = max(0.0, proposed_rent - max_legal_rent)
    excess_amount_annual = excess_amount_monthly * 12.0
    
    required_notice_days = 90 if percent_increase > 10.0 else 30

    return {
        "status": "success",
        "zip_code": zip_code,
        "current_rent": current_rent,
        "proposed_rent": proposed_rent,
        "dollar_increase": round(dollar_increase, 2),
        "percent_increase": round(percent_increase, 2),
        "max_allowed_percent": round(max_allowed_percent, 2),
        "max_legal_rent": round(max_legal_rent, 2),
        "is_excessive": is_excessive,
        "excess_amount_monthly": round(excess_amount_monthly, 2),
        "excess_amount_annual": round(excess_amount_annual, 2),
        "required_notice_days": required_notice_days,
        "governing_statutes": ["Santa Cruz Municipal Code 21.04.020", "California AB 1482"]
    }

def verify_eviction_notice(notice_type: str, lease_duration_months: int, stated_reason: str, relocation_offered: float = 0.0, current_rent: float = 2500.0) -> Dict[str, Any]:
    """verifies eviction notice against Santa Cruz Just Cause Eviction Ordinance (21.03.010)."""
    reason_lower = stated_reason.lower()
    has_just_cause_protection = lease_duration_months >= 12
    
    is_valid_at_fault = any(r.lower() in reason_lower for r in SANTA_CRUZ_MUNICIPAL_CODES["21.03.010"]["at_fault_reasons"])
    is_valid_no_fault = any(r.lower() in reason_lower for r in SANTA_CRUZ_MUNICIPAL_CODES["21.03.010"]["no_fault_reasons"]) or "owner move-in" in reason_lower or "renovation" in reason_lower or "demolition" in reason_lower or "ellis act" in reason_lower
    
    required_relocation = 0.0
    relocation_violation = False
    
    if is_valid_no_fault:
        required_relocation = max(current_rent * 2.0, 3000.0)
        if relocation_offered < required_relocation:
            relocation_violation = True
            
    is_unlawful = False
    violations = []
    
    if has_just_cause_protection and not (is_valid_at_fault or is_valid_no_fault):
        is_unlawful = True
        violations.append("notice fails to specify a legally recognized just cause reason under Santa Cruz Municipal Code 21.03.010.")
        
    if relocation_violation:
        is_unlawful = True
        violations.append(f"no-fault eviction notice provides ${relocation_offered:.2f} relocation assistance, but Santa Cruz Municipal Code 21.03.050 requires at least ${required_relocation:.2f} (2 months rent or $3,000).")
        
    return {
        "status": "success",
        "notice_type": notice_type,
        "lease_duration_months": lease_duration_months,
        "has_just_cause_protection": has_just_cause_protection,
        "is_unlawful": is_unlawful,
        "stated_reason": stated_reason,
        "is_valid_at_fault": is_valid_at_fault,
        "is_valid_no_fault": is_valid_no_fault,
        "required_relocation_assistance": required_relocation,
        "relocation_offered": relocation_offered,
        "relocation_violation": relocation_violation,
        "violations": violations,
        "code_reference": "Santa Cruz Municipal Code Chapter 21.03"
    }

def check_security_deposit(deposit_amount: float, monthly_rent: float) -> Dict[str, Any]:
    """checks if security deposit violates California AB 12 (1 month max rent)."""
    max_legal_deposit = monthly_rent
    is_excessive = deposit_amount > max_legal_deposit
    excess_amount = max(0.0, deposit_amount - max_legal_deposit)
    
    return {
        "status": "success",
        "monthly_rent": monthly_rent,
        "deposit_amount": deposit_amount,
        "max_legal_deposit": max_legal_deposit,
        "is_excessive": is_excessive,
        "excess_amount": round(excess_amount, 2),
        "statute": "California AB 12 (Civil Code § 1950.5)",
        "effective_date": "July 1, 2024",
        "recommendation": "request landlord issue a written credit or refund for deposit amount exceeding 1 month rent."
    }

def check_habitability_and_retaliation(issue_description: str) -> Dict[str, Any]:
    """checks for retaliatory lease clauses and severe habitability violations under CA Civil Code § 1942.5 & § 1953."""
    desc_lower = issue_description.lower()
    violations = []
    
    is_retaliatory_clause = any(w in desc_lower for w in ["inspector", "report", "city code", "defect", "consent"]) and any(w in desc_lower for w in ["terminate", "breach", "evict", "prohibit"])
    is_habitability_issue = any(w in desc_lower for w in ["mold", "leak", "plumbing", "water", "heat", "rodent", "substandard"])
    
    if is_retaliatory_clause:
        violations.append("unlawful retaliatory lease clause: lease terms prohibiting tenants from reporting building defects to Santa Cruz City Inspectors are void and unenforceable under CA Civil Code § 1953.")
        
    if is_habitability_issue:
        violations.append("severe habitability breach: failure to remediate hazardous conditions (mold/plumbing leaks) violates the Implied Warranty of Habitability under CA Civil Code § 1941.1.")
        
    return {
        "status": "success",
        "has_violations": len(violations) > 0,
        "violations": violations,
        "governing_codes": ["California Civil Code § 1941.1", "California Civil Code § 1942.5", "California Civil Code § 1953"]
    }

def get_legal_aid_contacts(zip_code: str = "95060", category: str = "general") -> Dict[str, Any]:
    """retrieves Santa Cruz County legal aid intake contacts."""
    return {
        "status": "success",
        "county": "Santa Cruz",
        "zip_code": zip_code,
        "resources_count": len(SANTA_CRUZ_LEGAL_AID_RESOURCES),
        "resources": SANTA_CRUZ_LEGAL_AID_RESOURCES
    }
