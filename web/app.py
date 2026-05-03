import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA_FILE = ROOT.parent / "pipeline-ai-insights.json"

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            self.path = "/index.html"

        try:
            file_path = ROOT / self.path.strip("/")
            if file_path.exists():
                self.send_response(200)
                self.end_headers()
                self.wfile.write(file_path.read_bytes())
            else:
                self.send_response(404)
                self.end_headers()
        except:
            self.send_response(500)
            self.end_headers()

    def do_POST(self):
        if self.path == "/data":
            self.send_response(200)
            self.end_headers()

            if DATA_FILE.exists():
                data = json.loads(DATA_FILE.read_text())
            else:
                data = {
                    "total_rows": 0,
                    "clean_rows": 0,
                    "rejected_rows": 0,
                    "quality_rate": 0,
                    "ai_copilot": {}
                }

            self.wfile.write(json.dumps(data).encode())

        elif self.path == "/chat":
            length = int(self.headers.get("Content-Length",0))
            body = self.rfile.read(length).decode()

            if DATA_FILE.exists():
                data = json.loads(DATA_FILE.read_text())
            else:
                data = {}

            ai = data.get("ai_copilot", {})
            q = body.lower()

            # ===== dynamic logic =====
            if "funnel" in q or "drop" in q:
                answer_text = f"Signup={data.get('accounts_with_signup',0)}, Activation={data.get('accounts_with_activation',0)}, Purchase={data.get('accounts_with_purchase',0)}."
                evidence_text = "Derived from funnel counts in pipeline summary."
                next_text = "Investigate conversion gaps between stages."
                rec_text = "Improve activation triggers and onboarding."
                decision_text = "Funnel needs optimization before scaling."

            elif "reject" in q or "error" in q:
                answer_text = f"Rejected rows: {data.get('rejected_rows',0)}"
                evidence_text = f"Reasons: {json.dumps(data.get('top_rejection_reasons',{}))}"
                next_text = "Fix validation failures at ingestion."
                rec_text = "Add schema + ID validation."
                decision_text = "Block promotion until rejection issues fixed."

            elif "risk" in q:
                answer_text = "Main risks identified in pipeline."
                evidence_text = ", ".join(ai.get("top_risks", []))
                next_text = "Mitigate top risks first."
                rec_text = ai.get("recommendation","Reduce data risk.")
                decision_text = ai.get("decision","Proceed carefully.")

            elif "action" in q or "improve" in q:
                answer_text = "Recommended engineering actions."
                evidence_text = ", ".join(ai.get("operator_actions", []))
                next_text = "Execute top 3 actions."
                rec_text = ai.get("recommendation","Improve validation.")
                decision_text = "Proceed after fixes."

            else:
                answer_text = f"Pipeline processed {data.get('total_rows',0)} rows with {data.get('clean_rows',0)} clean and {data.get('rejected_rows',0)} rejected."
                evidence_text = f"Quality rate is {round(data.get('quality_rate',0)*100,1)}%."
                next_text = "Review anomalies and improve quality."
                rec_text = ai.get("recommendation","Improve upstream validation.")
                decision_text = ai.get("decision","Proceed with caution")

            answer = {
                "answer": answer_text,
                "evidence": evidence_text,
                "next_action": next_text,
                "recommendation": rec_text,
                "decision": decision_text
            }

            self.send_response(200)
            self.end_headers()
            self.wfile.write(json.dumps(answer).encode())

def run():
    server = HTTPServer(("localhost", 8003), Handler)
    print("UI running at http://localhost:8003")
    server.serve_forever()

if __name__ == "__main__":
    run()