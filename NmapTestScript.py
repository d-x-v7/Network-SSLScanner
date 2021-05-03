import nmap

nm = nmap.PortScanner()
iprange = '173.241.154.15/27'

# Defines the range of which to scan along with the port.
scan_range = nm.scan(iprange, '443')
# scan_range = nm.scan('173.241.154.15', '443')

## All Hosts found

nm.all_hosts()
for host in nm.all_hosts():
    httpshosts = host
    # print("Open TCP Ports:" "%s" % (nm[host].all_tcp()))
    # print(scan_range['scan'])
    print(httpshosts)


# ### https://www.geeksforgeeks.org/port-scanner-using-python-nmap/
# begin = 75
# end = 80
#
# target = '173.241.154.15/30'
#
# scanner = nmap.PortScanner()
#
# for i in range(begin,end+1):
#     res = scanner.scan(target,str(i))
#
#     res = res['scan'][target]['tcp'][i]['state']
#
#     print (f'port {i} is {res}.')