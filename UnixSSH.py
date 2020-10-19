#!/usr/bin/python
#---------------------------------------------------
#   UnisSSH Change Password
#   V1.0
#
# Stratus Change
# Created : May, 2020
# Updated : --
#      By : Xavier Aguila
#---------------------------------------------------

import io
import os
import ctypes
import urllib
import sys
import paramiko
import argparse
import shutil
import shlex
import subprocess
from time import time, sleep
from subprocess import PIPE
from subprocess import check_output
from StringIO import StringIO
from CAUtils import *
from CAParamikoUtils import *

#----------------------------------
# Consts
#----------------------------------

class UnixSSHConnection():
    def __init__(self, address, port, username, password):
        self.address=address
        self.username=username
        self.password=password
        if(port == ""):
            port = "22"
        self.port = port

    def logon(self):
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.client.connect(self.address, username=self.username, password=self.password)

    def logoff(self):
        self.client.close()

    def changepass(self, command):
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.client.connect(self.address, username=self.username, password=self.password)
        #remote_conn = self.client.invoke_shell()
        #remote_conn.send(command)
        stdin, stdout, stderr = self.client.exec_command(command)
        stdin.flush()
        return stdout.readlines()
        #self.client.close()

def Main():

    parser = argparse.ArgumentParser()
    parser.add_argument("--address",required=True, help="Address/Hostname")
    parser.add_argument("--username",required=False, help="Username")
    parser.add_argument("--password",required=False, help="Password")
    parser.add_argument("--logonusername",required=False, help="Logon Username")
    parser.add_argument("--logonpassword",required=False, help="Logon Password")
    parser.add_argument("--newpassword",required=False, help="New Password")
    parser.add_argument("--action",required=False, help="verifylogon/changepass/reconpass")
    args = parser.parse_args()

    inputaction = raw_input("Action to do:")

    # Password Logon or Password Verify
    if (inputaction=="verifylogon"):
        connectionSSH = UnixSSHConnection(args.address,5022,args.username, args.password)
        connectionSSH.logon()
        print('Successfull Login')
        connectionSSH.logoff()

    # Password Change
    if (inputaction=="changepass"):
        connectionSSH = UnixSSHConnection(args.address,5022,args.username, args.password)
        sleep(5)
        SendChangePass = 'set_registration_info ' + str(args.username) + ' -password ' + str(args.newpassword)
        outchange = connectionSSH.changepass(SendChangePass)
        print (outchange)
        print('Successfull Change')
        connectionSSH.logoff()

    # Password Reconciliate
    if (inputaction=="reconpass"):
        connectionSSH = UnixSSHConnection(args.address,5022,args.logonusername, args.logonpassword)
        print ("usuario login: " + args.logonusername)
        print ("passowrd login: " + args.logonpassword)
        sleep(8)
        SendChangePass = 'set_registration_info ' + str(args.username) + ' -password ' + str(args.newpassword)
        outrecon = connectionSSH.changepass(SendChangePass)
        print ("comando ejecutado: " + SendChangePass)
        print (outrecon)
        print('Successfull Reconciliate')
        connectionSSH.logoff()

if __name__ == "__main__":
    Main()
