"""
CruzTenant Backend Web Server & REST API
Serves static frontend assets and REST API endpoints for Santa Cruz tenant lease analysis.
"""

import http.server
import socketserver
import json
import os
import urllib.parse
from agent import GemmaAgentEngine
import santa_cruz_legal_db as sc_db

PORT = 8000
PUBLIC_DIR = os.path.join(os.path.dirname(__file__), "public")
agent_engine = GemmaAgentEngine()

SAMPLE_CASES = [
    {
        "id": "case_1",
        "title": "Downtown SC Excessive 18% Rent Hike",
        "category": "Rent Stabilization Violation",
        "location": "Downtown Santa Cruz (95060)",
        "tenant_name": "Alex Rivera",
        "landlord_name": "Pacific Vista Management",
        "description": "Tenant received a written notice raising rent from $2,800/month to $3,304/month (an 18.0% increase) with 30 days notice.",
        "input_text": "I live on Pacific Ave in Downtown Santa Cruz. My current rent is $2,800 per month. Yesterday my landlord served me a 30-day rent increase notice raising my monthly rent to $3,304 starting next month. That is an 18% increase! Is this legal under Santa Cruz law?"
    },
    {
        "id": "case_2",
        "title": "Beach Flats Unlawful Eviction (No Relocation)",
        "category": "Just Cause & Relocation Violation",
        "location": "Beach Flats, Santa Cruz (95060)",
        "tenant_name": "Maria & Carlos Santos",
        "landlord_name": "Oceanfront Investments LLC",
        "description": "Tenant of 3 years received a 60-day notice to terminate tenancy for 'major property remodeling' offering $0 relocation assistance.",
        "input_text": "We have rented our apartment in Beach Flats near the Boardwalk for over 3 years. We pay $3,200/month. Last week the landlord served a 60-day Notice to Terminate Tenancy stating they plan to do building renovations. They offered $0 in relocation assistance and told us to move out. Is this allowed under Santa Cruz Municipal Code?"
    },
    {
        "id": "case_3",
        "title": "Live Oak Excessive Security Deposit",
        "category": "California AB 12 Violation",
        "location": "Live Oak / East Cliff (95062)",
        "tenant_name": "Jordan Chen (UCSC Student)",
        "landlord_name": "Seabright Properties",
        "description": "Landlord demanding a 2-month security deposit ($5,600) on a $2,800/month unfurnished apartment.",
        "input_text": "I am a UCSC student moving into an unfurnished apartment near Seabright. Monthly rent is $2,800. The landlord is demanding I pay a security deposit of $5,600 (two full months of rent) prior to move-in. Didn't California pass AB 12 limiting security deposits to 1 month's rent?"
    },
    {
        "id": "case_4",
        "title": "Westside Substandard Housing & Repair Refusal",
        "category": "Habitability & Retaliation Threat",
        "location": "Westside Santa Cruz (95060)",
        "tenant_name": "Samantha Taylor",
        "landlord_name": "Westside Residential Co",
        "description": "Lease clause threatening tenant with immediate eviction if tenant reports severe mold or plumbing failures to City Code Enforcement.",
        "input_text": "My lease on the Westside has a clause stating: 'Tenant agrees not to report any physical building defects to Santa Cruz City Inspectors without prior landlord consent, or tenancy will be immediately terminated for breach.' The bathroom has severe black mold and leaking pipes that the landlord refuses to fix."
    }
]

class CruzTenantRequestHandler(http.server.SimpleHTTPRequestHandler):
    def translate_path(self, path):
        # Serve files from PUBLIC_DIR if request path starts with / or static assets
        clean_path = urllib.parse.urlparse(path).path
        if clean_path == "/" or clean_path == "/index.html":
            return os.path.join(PUBLIC_DIR, "index.html")
        elif clean_path.startswith("/public/"):
            rel_path = clean_path.replace("/public/", "")
            return os.path.join(PUBLIC_DIR, rel_path)
        elif os.path.exists(os.path.join(PUBLIC_DIR, clean_path.lstrip("/"))):
            return os.path.join(PUBLIC_DIR, clean_path.lstrip("/"))
        return super().translate_path(path)

    def do_GET(self):
        clean_path = urllib.parse.urlparse(self.path).path
        if clean_path == "/api/sample-cases":
            self.send_json_response(200, {"status": "success", "cases": SAMPLE_CASES})
        elif clean_path == "/api/laws":
            law_data = sc_db.query_tenant_law("tenant rights")
            self.send_json_response(200, law_data)
        elif clean_path == "/api/legal-aid":
            aid_data = sc_db.get_legal_aid_contacts()
            self.send_json_response(200, aid_data)
        else:
            super().do_GET()

    def do_POST(self):
        clean_path = urllib.parse.urlparse(self.path).path
        content_length = int(self.headers.get('Content-Length', 0))
        body_bytes = self.rfile.read(content_length)
        
        try:
            body_json = json.loads(body_bytes.decode('utf-8')) if body_bytes else {}
        except Exception:
            body_json = {}
            
        if clean_path == "/api/analyze":
            tenant_text = body_json.get("text", "")
            tenant_name = body_json.get("tenant_name", "Jane Doe")
            landlord_name = body_json.get("landlord_name", "Landlord / Mgmt Co")
            
            if not tenant_text:
                self.send_json_response(400, {"status": "error", "message": "Missing 'text' field."})
                return
                
            analysis_result = agent_engine.analyze_scenario(
                tenant_text=tenant_text,
                tenant_name=tenant_name,
                landlord_name=landlord_name
            )
            self.send_json_response(200, analysis_result)
            
        elif clean_path == "/api/calculate-rent":
            current_r = float(body_json.get("current_rent", 0.0))
            proposed_r = float(body_json.get("proposed_rent", 0.0))
            zip_c = str(body_json.get("zip_code", "95060"))
            
            calc_result = sc_db.calculate_rent_cap(current_r, proposed_r, zip_c)
            self.send_json_response(200, calc_result)
            
        else:
            self.send_json_response(404, {"status": "error", "message": "Endpoint not found."})

    def send_json_response(self, status_code: int, data: Dict[str, Any]):
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.end_headers()
        self.wfile.write(json.dumps(data, indent=2).encode('utf-8'))

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.end_headers()

def run_server(port=PORT):
    print(f"==================================================")
    print(f" CruzTenant Local Server Starting...")
    print(f" Serving Web UI & REST API at http://localhost:{port}")
    print(f"==================================================")
    
    class ThreadedHTTPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
        allow_reuse_address = True
        
    httpd = ThreadedHTTPServer(("", port), CruzTenantRequestHandler)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server gracefully...")
        httpd.server_close()

if __name__ == "__main__":
    run_server()
