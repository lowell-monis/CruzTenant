"""
Santa Cruz Legal Knowledge Base & Rules Engine (CruzTenant)
Encodes Santa Cruz Municipal Code (Chapters 21.03 & 21.04),
City of Santa Cruz Tenant Protection Ordinances, California AB 1482 (Tenant Protection Act),
California AB 12 (Security Deposit Limits), and local legal aid resources.
"""

from typing import Dict, Any, List, Optional
import datetime

# Santa Cruz Metro Area CPI & Max Rent Increase Constants
CURRENT_SANTA_CRUZ_CPI = 3.8  # Percent annual CPI for Santa Cruz Metro Area
AB1482_BASE_CAP = 5.0          # 5.0% base cap under CA AB 1482
MAX_ALLOWED_RENT_INCREASE_PERCENT = AB1482_BASE_CAP + CURRENT_SANTA_CRUZ_CPI # 8.8%

SANTA_CRUZ_MUNICIPAL_CODES = {
    "21.03.010": {
        "title": "Santa Cruz Just Cause Eviction Protections",
        "description": "Landlords must provide a valid 'at-fault' or 'no-fault' just cause reason to terminate a tenancy for tenants occupying a property for 12+ months.",
        "jurisdiction": "City of Santa Cruz",
        "at_fault_reasons": [
            "Nonpayment of rent",
            "Material breach of lease terms after written notice to cure",
            "Nuisance or illegal activity on premises",
            "Refusal to execute a written extension of lease with similar terms"
        ],
        "no_fault_reasons": [
            "Owner or owner's immediate family intent to occupy",
            "Substantial rehabilitation or demolition of property",
            "Withdrawal of residential rental unit from rental market (Ellis Act)",
            "Compliance with a government order or court order to vacate"
        ]
    },
    "21.03.050": {
        "title": "Mandatory Relocation Assistance for No-Fault Eviction",
        "description": "If a landlord terminates a tenancy under a no-fault cause in Santa Cruz, they must provide relocation assistance equal to two (2) months of the tenant's current rent or $3,000, whichever is greater, paid within 15 days of notice service.",
        "jurisdiction": "City of Santa Cruz",
        "relocation_multiplier_months": 2,
        "minimum_relocation_usd": 3000
    },
    "21.04.020": {
        "title": "Rent Stabilization & Excessive Rent Increase Notice",
        "description": "Rent increases exceeding 5% + CPI (8.8% total for current cycle) within any 12-month period trigger mandatory 90-day written notice and tenant mediation rights under City Ordinance.",
        "max_allowable_annual_increase_pct": MAX_ALLOWED_RENT_INCREASE_PERCENT,
        "required_notice_days_large_increase": 90, # For increases > 10%
        "required_notice_days_standard": 30       # For increases <= 10%
    },
    "CA_AB_12": {
        "title": "California AB 12 - Security Deposit Limits (Effective July 1, 2024)",
        "description": "Landlords in California are legally restricted from collecting more than one (1) month's rent as a security deposit for residential leases, regardless of whether the unit is furnished or unfurnished.",
        "effective_date": "2024-07-01",
        "max_deposit_months": 1.0,
        "small_landlord_exception": "Landlords owning <= 2 properties with <= 4 total units may collect up to 2 months' rent."
    },
    "CA_AB_1482": {
        "title": "California Tenant Protection Act of 2019 (AB 1482)",
        "description": "Statewide rent cap (5% + local CPI, max 10%) and just-cause eviction protections. Exempts single-family homes (unless corporate owned) and units built in the last 15 years.",
        "base_cap_pct": 5.0,
        "max_overall_cap_pct": 10.0
    }
}

SANTA_CRUZ_LEGAL_AID_RESOURCES = [
    {
        "name": "Senior Citizens Legal Services - Santa Cruz",
        "address": "501 Soquel Ave, Suite F, Santa Cruz, CA 95062",
        "phone": "(831) 426-8824",
        "services": ["Eviction Defense", "Rent Increase Disputes", "Housing Discrimination"],
        "eligibility": "Santa Cruz County residents aged 60+ or low-income households"
    },
    {
        "name": "California Rural Legal Assistance (CRLA) - Watsonville/Santa Cruz",
        "address": "21 Carr St, Watsonville, CA 95076",
        "phone": "(831) 724-2253",
        "services": ["Tenant Rights", "Substandard Housing Litigation", "Unlawful Detainer Defense"],
        "eligibility": "Low-income tenants and agricultural workers in Santa Cruz County"
    },
    {
        "name": "Conflict Resolution Center of Santa Cruz County",
        "address": "147 S River St, Suite 206, Santa Cruz, CA 95060",
        "phone": "(831) 475-6117",
        "services": ["Landlord-Tenant Mediation", "Rent Dispute Settlement"],
        "eligibility": "All Santa Cruz County landlords and tenants"
    },
    {
        "name": "Santa Cruz County Law Library Tenant Self-Help",
        "address": "701 Ocean Street, Room 080, Santa Cruz, CA 95060",
        "phone": "(831) 457-2525",
        "services": ["Legal Form Filing", "Tenant Answer Assistance", "Municipal Code Research"],
        "eligibility": "Public access"
    }
]

def query_tenant_law(query_topic: str, jurisdiction: str = "Santa Cruz") -> Dict[str, Any]:
    """Queries Santa Cruz and California tenant protection laws for a specific topic."""
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
    """Calculates whether a proposed rent increase exceeds Santa Cruz CPI + AB 1482 limits."""
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
    """Verifies an eviction notice against Santa Cruz Just Cause Eviction Ordinance (21.03.010)."""
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
        violations.append("Notice fails to specify a legally recognized Just Cause reason under SC Municipal Code 21.03.010.")
        
    if relocation_violation:
        is_unlawful = True
        violations.append(f"No-Fault Eviction notice provides ${relocation_offered:.2f} relocation assistance, but Santa Cruz Municipal Code 21.03.050 requires at least ${required_relocation:.2f} (2 months rent or $3,000).")
        
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
    """Checks whether security deposit violates California AB 12 (1 month max rent)."""
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
        "recommendation": "Request landlord issue a written credit or refund for the deposit amount exceeding 1 month's rent."
    }

def get_legal_aid_contacts(zip_code: str = "95060", category: str = "general") -> Dict[str, Any]:
    """Retrieves Santa Cruz County legal aid intake contacts."""
    return {
        "status": "success",
        "county": "Santa Cruz",
        "zip_code": zip_code,
        "resources_count": len(SANTA_CRUZ_LEGAL_AID_RESOURCES),
        "resources": SANTA_CRUZ_LEGAL_AID_RESOURCES
    }
