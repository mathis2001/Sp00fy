import requests
import sys
import dns.resolver
import argparse

class bcolors:
	OK = '\033[92m'
	WARNING = '\033[93m'
	FAIL = '\033[91m'
	RESET = '\033[0m'
	INFO = '\033[94m'


def main():
	parser = argparse.ArgumentParser()
	parser.add_argument("-d", "--domain", help="Target domain", type=str)
	args = parser.parse_args()

	if args.domain:
		domain="_dmarc."+args.domain


	record = ""
	resolver = dns.resolver.Resolver()
    
	try:
		txt = resolver.resolve(domain, "TXT") 
		for rdata in txt: 
			record += str(rdata) + "\n"
	except:
		print(bcolors.FAIL+"[!] "+bcolors.RESET+"No record found.")
		print(bcolors.INFO+"[*] "+bcolors.RESET+"usage: ./sp00fy.py [-h] -d target.xyz")
		exit(0)
	
	print(f'''
DMARC record found for {args.domain}:
---------------------------

{record}
---------------------------
	''')

	if "p=none" in record:
        	print(bcolors.OK+"[+] "+bcolors.RESET+"Target is potentially vulnerable.")
	else:
		print(bcolors.FAIL+"[!] "+bcolors.RESET+"Target is not vulnerable.")

try:
        main()
except Exception as e:
        print(e)
except KeyboardInterrupt:
        print(bcolors.FAIL+"[!] "+bcolors.RESET+"Script canceled.")
