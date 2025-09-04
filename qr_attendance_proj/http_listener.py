
import ipaddress
from fastapi import FastAPI, Request, HTTPException

# Instantiate FastAPI object
app = FastAPI(title="Listener API", version='0.1.1')

QR_SCRIPT = "/opt/jobs/qr_gen.py"

# Define list of permitted IPs (127.0.0.1 are placeholder IPs)
IP_ALLOWED = [ipaddress.ip_network(var) for var in [
    "127.0.0.1/32" # TAremote IP 1
    # "127.0.0.1/32" # TAremote IP 2
]]

# Helper function to check if IP address is in the list of permitted IPs
def check_ip(ip_str: str):
    ip = ipaddress.ip_address(ip_str)
    return any(ip in net for net in IP_ALLOWED)

# Middleware to handle unpermitted IPs
# custom HTTPException: https://fastapi.tiangolo.com/tutorial/handling-errors/
# middleware: https://fastapi.tiangolo.com/tutorial/middleware/?utm_source=chatgpt.com#creat>
@app.middleware("http")
async def enforce_allowlist(req: Request, call_next):
    client_ip = req.client.host
    response = await call_next(req)
    if not check_ip(client_ip):
        raise HTTPException(status_code=403, detail="IP not permitted")
    return response

# Read json data that has been posted to http://<server-ip>:<port>/data_qr
@app.post("/data_qr")
async def run_sript(req: Request)
    data = await req.json()
    
    # Pass data from json to script

    # Define the command to execute
    cmd = [sys.executable, QR_SCRIPT]
