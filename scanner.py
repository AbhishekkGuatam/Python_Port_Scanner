import socket
import sys
import threading
import queue
import time
from datetime import datetime

print("""
*************************************************************
* ____  ____ ____ ___    ____ ____ ____ _  _ _  _ ____ ____ *
* |__]  |  | |__/  |     [__  |    |__| |\ | |\ | |___ |__/ *
* |     |__| |  \  |     ___] |___ |  | | \| | \| |___ |  \ *
*                                                           *
*************************************************************""")
print("Made By: Abhishek Gautam")
#Defining Dictionary of common ports
common_ports = {
    "21": "FTP",
    "22": "SSH",
    "23": "Telnet",
    "25": "SMTP",
    "53": "DNS",
    "67":"DHCP",
    "68":"DHCP",
    "69":"TFTP",
    "80": "HTTP",
    "110":"POPv3",
    "123":"NTP",
    "143":"IMAP",
    "194": "IRC",
    "389":"LDAP",
    "443": "HTTPS",
    "3306": "MySQL",
    "25565": "Minecraft"
}

#printing basic info about the scans
print("\n[*]Host: {}       IP: {}  ".format(sys.argv[1], socket.gethostbyname(sys.argv[1])))

#returns the value of host , start port and end port
def get_scan_args():
    if len(sys.argv) == 2:
        print("\n[*]Starting Port: {}       Ending Port: {}".format(0, 1024))
        return (sys.argv[1], 0, 1024)
    elif len(sys.argv) == 3:
        print("\n[*]Starting Port: {}       Ending Port: {}".format(1, sys.argv[2]))
        return (sys.argv[1],0,  int(sys.argv[2]))
    elif len(sys.argv) == 4:
        print("\n[*]Starting Port: {}       Ending Port: {}".format(sys.argv[2], sys.argv[3]))
        return (sys.argv[1], int(sys.argv[2]), int(sys.argv[3]))


#tries to establish a connection
def is_port_open(host, port): #Return boolean
    try:
        # create an INET, STREAMing socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.5)
        sock.connect((host, port))
    except socket.error:
        return False
    return True

def scanner_worker_thread(host):
    while True:
        port = port_queue.get()
        if is_port_open(host, port):
            if str(port) in common_ports:
                print("[*]{}({}) is OPEN!".format(str(port), common_ports[str(port)]))
            else:
                print("[*]{} is OPEN!".format(port))
        port_queue.task_done()



scan_args = get_scan_args()
port_queue = queue.Queue()
for _ in range(30):
    t = threading.Thread(target=scanner_worker_thread, kwargs={"host": scan_args[0]})
    t.daemon = True
    t.start()
 
start_time = time.time()
print("[*] Scanning started at %s    \n" %(time.strftime("%H:%M:%S")))
for port in range(scan_args[1], scan_args[2]):
    port_queue.put(port)

port_queue.join()
end_time = time.time()
print("\n\n[*] Scanning ended at %s    \n" %(time.strftime("%H:%M:%S")))
print("Done! Scanning took {:.3f} seconds.".format(end_time - start_time))

