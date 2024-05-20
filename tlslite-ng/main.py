import sys
sys.dont_write_bytecode = True

# HTTPTLSConnection = tlslite-ng + http.client
from tlslite import HTTPTLSConnection

domain = "raw.githubusercontent.com"
file = "TrueCat17/Ren-Engine/master/README.md"

conn = HTTPTLSConnection(domain, 443) # 443 - usual port for https
conn.request("GET", file)            # method, path
response = conn.getresponse()

data = response.read(100)
print(data)
