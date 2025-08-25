import ipaddress
from fastapi import FastAPI, Request, HTTPException

# Instantiate FastAPI object 

app = FastAPI(title="Listener API", version='0.1.1')

# Define list of permitted IPs

IP_ALLOWED = [ipaddress.ip_address(var) for var in [
    # TAremote IP 1
    "44.3.2.28/32"
    # TAremote IP 2
    #"127.0.0.1/32"
]]

# Helper function to check if IP address is in the list of permitted IPs

def check_ip(ip_str: str):
    ip = ipaddress.ip_address(ip_str)
    return any(ip in addr for addr in IP_ALLOWED)

# Middleware to handle unpermitted IPs
# custom HTTPException: https://fastapi.tiangolo.com/tutorial/handling-errors/
# middleware: https://fastapi.tiangolo.com/tutorial/middleware/?utm_source=chatgpt.com#create-a-middleware
@app.middleware("http")
async def enforce_allowlist(req: Request, call_next):
    client_ip = req.client.host
    if not check_ip(client_ip)
        raise HTTPException(status_code=403, detail="IP not permitted")
    return await call_next(req)


