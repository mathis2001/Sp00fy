import requests
import sys
import dns.resolver
import argparse
import os

class bcolors:
	OK = '\033[92m'
	WARNING = '\033[93m'
	FAIL = '\033[91m'
	RESET = '\033[0m'
	INFO = '\033[94m'

parser = argparse.ArgumentParser()
parser.add_argument("-d", "--domain", help="Target domain", type=str)
parser.add_argument("-f", "--find-emails", help="Find emails for the given domain", action="store_true")
parser.add_argument("-l", "--limit", help="Number of results wanted", type=str)
args = parser.parse_args()

def mailFinder():
	HUNTER_KEY=os.getenv('HUNTER_KEY')
	emails=[]

	if args.limit:
		limit = args.limit
	else:
		limit = '10'

	hunter = "https://api.hunter.io/v2/domain-search?domain="+args.domain+"&api_key="+HUNTER_KEY+"&limit="+limit
	r = requests.get(hunter, timeout=5, allow_redirects=True)
	response = r.json()

	for email in response['data']['emails']:
		emails.append(str(email['value']))
	return emails

def main():

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
		print(bcolors.FAIL+"[!] "+bcolors.RESET+"DMARC policy is set to "+bcolors.FAIL+"none"+bcolors.RESET+".")
		print(bcolors.OK+"[+] "+bcolors.RESET+"Target is potentially vulnerable.")
	elif "p=quarantine" in record:
		print(bcolors.WARNING+"[-] "+bcolors.RESET+"DMARC policy is set to "+bcolors.WARNING+"quarantine"+bcolors.RESET+".")
		print(bcolors.FAIL+"[!] "+bcolors.RESET+"Target must not be vulnerable.")
	elif "p=reject" in record:
		print(bcolors.OK+"[+] "+bcolors.RESET+"DMARC policy is set to "+bcolors.OK+"reject"+bcolors.RESET+".")
		print(bcolors.FAIL+"[!] "+bcolors.RESET+"Target must not be vulnerable.")
	else:
		print(bcolors.FAIL+"[!] "+bcolors.RESET+"No DMARC policy found.")
		exit(0)

	if args.find_emails:
		emails = mailFinder()
		print(bcolors.INFO+"\n [*] "+bcolors.RESET+"emails found:\n")
		for email in emails:
			print(bcolors.OK+"[+] "+bcolors.RESET+email)
try:
	main()
except Exception as e:
	print(e)
except KeyboardInterrupt:
	print(bcolors.FAIL+"[!] "+bcolors.RESET+"Script canceled.")
