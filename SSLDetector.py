import subprocess
import sys
import nmap
import OpenSSL
import ssl, socket
import argparse
import datetime

IP_ADDRESS = sys.argv[1]

### ABOUT THIS SCRIPT
# Goals are identify subnets for a specific company and scan those ips for hosts listening on port 443
# Extract HTTPS certificate and see when it will expire
# Generate output that can be used to determine which certs are expired or which ones will expire in within the next year. Could be email or a report.

print('Starting Whois lookup...')

### IDENTIFY THE SUBNET FOR THE GIVEN IP ADDRESS
### ---------------------------------------------------------------
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

# This was to test the output of the whois results
print(f"Whois lookup returned {whoisresults} as the subnet")


### RUN AN NMAP SCAN ON THE SUBNET TO IDENTIFY HOSTS RUNNING ON PORT 443
### ---------------------------------------------------------------

print(f"Starting nmap scan on {whoisresults} for hosts with port 443 open...")

nm = nmap.PortScanner()

# Defines the range of which to scan along with the port.
scan_range = nm.scan(whoisresults, '443')
# scan_range = nm.scan('173.241.154.15', '443')


nm.all_hosts()
for host in nm.all_hosts():
    httpshosts = host
    # Below is used to test the results
    # print(httpshosts)
    # print("Open TCP Ports:" "%s" % (nm[host].all_tcp()))
    # print(scan_range['scan'])


### USING THE RESULTS OF THE NMAP SCAN TO CHECK THE SSL CERTIFICATES
### ---------------------------------------------------------------

print("Found hosts running port 443, will now check to see their SSL certificate status...")

# SECTION NAME: Current Date
current_time = datetime.datetime.now()

# # SECTION NAME: Get Domain
# parser = argparse.ArgumentParser()
# # This tells the parser to look for an argument from the user after the script is called.
# parser.add_argument('domain')
# args = parser.parse_args()
# domain = args.domain

# SECTION NAME: Get SSL Cert info and Expiration
cert = ssl.get_server_certificate((httpshosts, 443))
x509 = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, cert)
x509info = x509.get_notAfter()

# The numbers below (6:8, 4:6, :4) relate to the byte positions within the SSL Certificate.
exp_day = x509info[6:8].decode("utf-8")
exp_month = x509info[4:6].decode("utf-8")
exp_year = x509info[:4].decode("utf-8")

exp_date = str(exp_day) + '-' + str(exp_month) + '-' + str(exp_year)

# SECTION NAME: Print out results

if exp_year == current_time.year:
    print(f'SSL Certificate for domain {httpshosts} will be expired on (DD-MM-YYYY) {exp_date}')
elif exp_year != current_time.year:
    print(f'SSL Certificate for {httpshosts} does not expire this year')
elif exp_year == None:
    print('No SSl Certificate exists')
else:
    print('Oops, something went wrong')