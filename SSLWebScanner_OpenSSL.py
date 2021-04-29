import OpenSSL
import ssl, socket
import argparse
import datetime

# SECTION NAME: Current Date
current_time = datetime.datetime.now()

# SECTION NAME: Get Domain
parser = argparse.ArgumentParser()
# This tells the parser to look for an argument from the user after the script is called.
parser.add_argument('domain')
args = parser.parse_args()
domain = args.domain

# SECTION NAME: Get SSL Cert info
cert = ssl.get_server_certificate((domain, 443))
x509 = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, cert)
x509info = x509.get_notAfter()

# The numbers below (6:8, 4:6, :4) relate to the byte positions within the SSL Certificate.
exp_day = x509info[6:8].decode("utf-8")
exp_month = x509info[4:6].decode("utf-8")
exp_year = x509info[:4].decode("utf-8")

exp_date = str(exp_day) + '-' + str(exp_month) + '-' + str(exp_year)

# SECTION NAME: Print out results

if exp_year == current_time.year:
    print('SSL Certificate for domain', domain, 'will be expired on (DD-MM-YYYY)', exp_date)
else:
    print('SSL Certificate does not expire this year')
