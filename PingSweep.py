#!/bin/python3
import os
import wget
import sys
from urllib.error import HTTPError
import socket
import csv

# Ideally we could have a centralised location where we can keep our hosts file 
# and use GoogleDrive API to download the (private) hosts.txt file locally. 
# In this example we will download a public file from GitHub
# We use wget, so we need to install the wget package: pip install wget before we run this script

# Run this script and include the exit code option:  ./PingSweep.py; echo $?
# Exit Code = 2 : Issues with the file
# Exit Code = 1 : One or more hosts not online
# Exit Code = 0 : All hosts online


# We will create two functions that can help us to silence the stdout when needed. 

def enablePrint():
    sys.stdout = sys.__stdout__

def blockPrint():
    sys.stdout = open(os.devnull, 'w')

# Block any output related to file download
blockPrint()

# First of all check if the file exists and remove it first, so we can download the latest version.
if os.path.exists("hosts.txt"):
        os.remove("hosts.txt")

url='https://raw.githubusercontent.com/theulis/Python-Ping/main/hosts.txt'

# Check if the file exists in GitLab
try:
    hosts_file=wget.download(url)
except HTTPError as err:
        enablePrint()
        print("------> Problem while downloading file (hosts.txt) for GitHub repo")
        sys.exit(2)

else:
    
# Check if the file is a valid CSV file with a comma as the delimiter

    def check_data_validity(file):
        with open(file, newline='') as csvfile:
            try:
                dialect = csv.Sniffer().sniff(csvfile.read(1024), delimiters = ",")
            except:
                enablePrint()
                print("------> File hosts.txt not a valid CSV comma delimited file")
                sys.exit(2)
    check_data_validity("hosts.txt")
    
# Now let's enabled stdout and get our results
    enablePrint()

# Open the file and store the information as a dictionary: Key-Value pair (IP Address: Host Description)

    ip_address_list = {}
    source_file = open("hosts.txt")
    for line in source_file:
        key, value = line.split(",")
        ip_address_list[key] = value

# Ping each IP address and confirm if online

    print("Online\tStatus\tAddress\t\tName")
    print("------\t------\t------------\t--------")


    offline_hosts=0   # Parameter will be used to monitor if we have offline hosts

    for ip_address in list(ip_address_list)[1:]:

# Check if the IP Address is valid
        try:
            socket.inet_aton(ip_address)
        except OSError as error:
            print(f"xxxxx\txxxxx\tInvalid_IP\t{ip_address_list[ip_address]}",end='')
            continue

# If IP address is valid start a ping pequest for each IP Address

        response = os.popen(f"ping {ip_address} -c 1 -W 1").read()
        if "64 bytes" in response:
            print(f"True\tSuccess\t{ip_address:<10s}\t{ip_address_list[ip_address]}",end='')
        else:
            print(f"False\tFailed\t{ip_address:<10s}\t{ip_address_list[ip_address]}",end='')
            offline_hosts='true'    # We have a device offline

    if offline_hosts == 'true':
        sys.exit(1)
    else : 
        sys.exit(0)
