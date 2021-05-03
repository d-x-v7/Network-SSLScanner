import subprocess
import sys

IP_ADDRESS = sys.argv[1]

# Goals are identify subnets for a specific company and scan those ips for hosts listening on port 443
# Extract HTTPS certificate and see when it will expire
# Generate output that can be used to determine which certs are expired or which ones will expire in within the next year. Could be email or a report.

# This outputs the subnet, but has a new line in it.
# scan2 = subprocess.run(['grep', '-E', '-o', '(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])(\/(3[0-2]|[1-2][0-9]|[0-9]))'],
#     capture_output=True,
#     text=True,
#     input=scan.stdout
# )

whois1 = subprocess.run(['whois', IP_ADDRESS],
    capture_output=True,
    text=True,
)

whois2 = subprocess.run(['grep', '-E', '-o', '(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])(\/(3[0-2]|[1-2][0-9]|[0-9]))'],
    capture_output=True,
    text=True,
    input=whois1.stdout,
)

finalsubnet = subprocess.run(['tr', '-d', "\n"],
    capture_output=True,
    text=True,
    input=whois2.stdout
)

whoisresults = str(finalsubnet.stdout)

# scan = subprocess.run(['whois', IP_ADDRESS], capture_output=True, text=True)
# print(scan2.stdout)
print(whoisresults)
# Script to identify and scan subnets