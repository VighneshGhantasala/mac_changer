#!/usr/bin/env python
#author:Vighnesh Ghantasala
#mac_changer_v1.0 - mask your mac address

import subprocess as sp
import optparse
import re

def banner():
    banner = """
                                   
  ( *   )                            
` )  /( (         (   *   )         
 ( )(_)))(    (   )\  ( /(   (     
(_(_())(()\   )\ ((_) )(_))  )\ )  
|_   _| ((_) ((_)  ! ((_)_  _(_/(  
  | |  | '_|/ _ \ | |/ _` || ' \)) 
  |_|  |_|  \___/_/ |\__,_||_||_|  
                |__/               

    """
    print(banner)
    print("\n author: Vighnesh Ghantasala \n github:https://github.com/VighneshGhantasala/ \n\n")
    print("mac_changer_v1.0")
flag = 0
def list_interface():
    global flag
    flag = 1
    ifconfig_result = sp.check_output(["ifconfig", "-a", "-s"])
    result_lines = ifconfig_result.splitlines()
    print("Interfaces:")
    for i in range(1,len(result_lines)):
        interfaces = result_lines[i].split()[0]
        print(interfaces)
def get_args():
    parser = optparse.OptionParser()
    # Options -----------
    parser.add_option("-i", "--interface", dest="interface", help="interface to select for changing mac")
    parser.add_option("-m", "--mac", dest="new_mac", help="new mac address to change, ex. 00:11:22:33:44:55")
    parser.add_option("-l","--list",action="store_true",dest="interface_list",help="Lists the interfaces available")

    (options, arguments) = parser.parse_args()
    if options.interface_list:
        list_interface()
    else:
        if not options.interface:
            parser.error("no interface detected , please type an interface\n use -l to list interfaces available")
        elif not options.new_mac:
            parser.error("new mac not found , pleas enter new mac for interface")
        else:
            return options
#-------------------------

def get_current_mac(interface):
    ifconfig_check = re.search(r'\w\w:\w\w:\w\w:\w\w:\w\w:\w\w',sp.check_output(["ifconfig",interface]))
    if ifconfig_check:
        current_mac = ifconfig_check.group(0)
        return current_mac
    else:
        return "[-] No mac found for interface"

def change_mac(interface,new_mac):
    interface = options.interface
    new_mac = options.new_mac
    current_mac = get_current_mac(interface)
    print("[+] Changing "+ current_mac +" of " + options.interface + " to " + new_mac)
    sp.call(["ifconfig", interface, "down"])
    sp.call(["ifconfig", interface, "hw", "ether", new_mac])
    sp.call(["ifconfig", interface, "up"])
banner()
options = get_args()
if flag==0:
    current_mac = get_current_mac(options.interface)
    if current_mac == "[-] No mac found for interface":
        print(current_mac)
    else:
        change_mac(options.interface, options.new_mac)
        current_mac = get_current_mac(options.interface)
        if current_mac == options.new_mac:
            print("[+] Your mac has been changed to " + current_mac)
        else:
            print("[-] Unable to change mac")