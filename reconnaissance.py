import subprocess
import re


def valid_inputformat(input):
    ip_address_pattern = r'\b(?:\d{1,3}\.){3}\d{1,3}\b'
    web_address_pattern = r'\b(?:www\.)?([a-zA-Z0-9.-]+)\.(?:[a-zA-Z]{2,6})\b'

    # Check if input matches IP address or web address pattern
    if  re.match(ip_address_pattern, input) or  re.match(web_address_pattern, input):
        return True
    else:
        return False
    


def find_server_tech(target):
    result = subprocess.run(['whatweb', target], capture_output=True, text=True)
    output = result.stdout
    server_tech = ""
    if 'apache' in output.lower():
        server_tech += target + " uses Apache server\n"
    else:
        server_tech += target + " does not use Apache \n"
    
    if 'wordpress' in output.lower():
       server_tech += target + " uses WordPress\n"
    else:
        server_tech += target + " does not use WordPress\n"
    return server_tech
    

def nmap_vuln(target):
    try:
        result = subprocess.run(["sudo", "nmap", "--script", "http-stored-xss.nse", target], capture_output=True, text=True, check=True)
        output = result.stdout
        return output
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
    


def report (target_list):
    f = open("Reconnaissance_report_620146170.txt", "a")
   
    if len(target_list) ==1:
        target = target_list[0]
        print(f"\nSCANNING {target}. THIS MAY TAKE A WHILE... \n")
        if valid_inputformat(target):
            servertech = find_server_tech(target)
            Xss_vuln = nmap_vuln(target)
            f.write("\t***"+target+"***\n"+ servertech + "\n"+ Xss_vuln +"\n\n")
            f.close()
        else:
            return f"Invalid Address: {target}"

    else:
        for target in target_list:
            if valid_inputformat(target):
                print(f"\nSCANNING {target}. THIS MAY TAKE A WHILE... \n")
                servertech = find_server_tech(target)
                Xss_vuln = nmap_vuln(target)
                f.write("\t***"+target+"***\n"+ servertech + "\n"+ Xss_vuln +"\n\n")
            else:
                print (f"Invalid Address: {target}")
                continue
                
    print ("YOUR REPORT IS READY.\nTo view the report open Reconnaissance_report.txt\n")
    f.close()   
    

if __name__ == '__main__':
    while True:
        target_list = []  
    
        response = input("Reply with: \n[A] if looking up a single target \n[B] if submitting a file containing a list of targets  \n[X] to exit\n\n ")
        if response == "A" or response == "a":
            target = input("State the target IP or web address: ")
            target_list.append(target)
            report(target_list)
        elif response == "B" or response == "b":
            target = input("State the filepath to the file (for e.g. /home/kali/Documents/file.txt)  encompassing the target addresses (Must be txt format and each target must be separated using a new line, no commas): ")
            f = open(target, "r")
            target_list = list(f.read().split("\n"))
            report(target_list)
            f.close()
        elif response == "X" or response == "x":
            print("Exiting...")
            break     
        else:
            print("Input not valid.")
