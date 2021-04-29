import OpenSSL
import ssl, socket
cert=ssl.get_server_certificate(('www.google.com', 443))
x509 = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, cert)
x509.get_notAfter()
x509info = x509.get_notAfter()
alldata = x509info[6:8].decode("utf-8")
print(cert)
print(alldata)