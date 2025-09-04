import ipaddress, sys
from fastapi import FastAPI, Request, HTTPException

# Instantiate FastAPI object
app = FastAPI(title="Listener API", version='0.1.1')

QR_SCRIPT = "/opt/jobs/qr_gen.py" # Inputs: Date, CSV File Path
MAIL_SCRIPT = "/opt/jobs/mail.py" # Inputs: Course, Body, 

# Define list of permitted IPs
IP_ALLOWED = [ipaddress.ip_network(var) for var in [
    "PERMITTED IP ADDRESS HERE", # TAremote IP 1
    "127.0.0.1/32" # Local Testing
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
    if not check_ip(client_ip):
        raise HTTPException(status_code=403, detail="IP not permitted")
    response = await call_next(req)
    return response

# Read json data that has been posted to http://<server-ip>:<port>/data_qr
@app.post("/data_qr")
async def run_sript(req: Request):
    data = await req.json()
    
    # Fields extracted from data
    student_id = str(data.get("student_id", ""))
    course = str(data.get("course", ""))

    # Define the command to execute and python binary
    cmd = [sys.executable, QR_SCRIPT, student_id, course]

    # Feedback Output
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True
        )
        return {
            "status": "ok",
            "stdout": result.stdout,
            "stderr": result.stderr,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/scan")
async def scan(req: Request): 
    data = await req.json
    
    # Extract QR_data
    qr_dat = str(data.get("qr_dat", ""))
    cmd = [sys.executable, READ_SCRIPT]

    # Feedback Output
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True
        )
        return {
            "status": "ok",
            "stdout": result.stdout,
            "stderr": result.stderr,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))