#!/usr/bin/env python3

import requests
from requests_html import HTMLSession
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
parser.add_argument("-s", "--send", help="send anonymous email", action="store_true")
parser.add_argument("-l", "--limit", help="Number of results wanted", type=str)
args = parser.parse_args()

def send_mail(to, subject, body, debug, name, sender):
	headers = {
        	"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        	"Accept-Encoding": "gzip, deflate, br",
        	"Accept-Language": "en-US,en;q=0.9",
        	"Cache-Control": "max-age=0",
        	"Connection": "keep-alive",
        	"Content-Length": "3072",
        	#"Cookie": "",
        	"Host": "emkei.cz",
        	"Origin": "null",
        	"sec-ch-ua": '" Not A;Brand";v="99", "Chromium";v="99", "Microsoft Edge";v="99"',
        	"sec-ch-ua-mobile": "?0",
        	"sec-ch-ua-platform": '"Linux"',
        	"Sec-Fetch-Dest": "document",
        	"Sec-Fetch-Mode": "navigate",
        	"Sec-Fetch-Site": "same-origin",
        	"Sec-Fetch-User": "?1",
        	"Upgrade-Insecure-Requests": "1",
        	"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36 Edg/99.0.1150.55"
	}
	payload = {
        	"fromname": name,
        	"from": sender,
        	"rcpt": to,
        	"subject": subject,
        	"attachment": "(binary)",
        	"reply": "",
        	"errors": "",
        	"cc": "",
        	"bcc": "",
        	"importance": "normal",
        	"xmailer": "0",
        	"customxm": "",
        	"confirmd": "",
        	"confirmr": "",
        	"addh": "",
        	"smtp": "",
        	"smtpp": "",
        	"current": "on",
        	"charset": "utf-8",
        	"mycharset": "",
        	"encrypt": "no",
        	"ctype": "plain",
        	"rte": "0",
        	"text": body,
        	"ok": "Send"
    	}
	
	session=HTMLSession()
	response = session.get("https://emkei.cz/")
	for _ in range(10):
		if response.html.search('name="g-recaptcha-response" value="{}"') is None:
			response.html.render()
	payload['g-recaptcha-response']=response.html.search('name="g-recaptcha-response" value="{}"')[0]
	
	request = requests.request(
        method="POST",
        url="https://emkei.cz/",
        headers=headers,
        data=payload)

	if debug:
		print(request.status_code)
		print(bcolors.INFO+"\n[*] "+bcolors.RESET+"E-mail sent successfully.")

	if request.status_code != 200:
		if "E-mail sent successfully" not in request.text:
			return -1
	return 0

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
		print(bcolors.FAIL+"[!] "+bcolors.RESET+"Target may be vulnerable.")
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
	if args.send:
		print(bcolors.INFO+"\n [*] "+bcolors.RESET+"Create your anonymous mail with emkei.cz.\n")
		name = input("From name: ")
		sender = input("From E-mail: ")
		to = input("To: ")
		subject = "VULNERABLE"
		body ="""
		You see this email ?
	It meen that your domain is vulnerable to email spoofing.
		""",
		debug=True
		send_mail(to, subject, body, debug, name, sender)
try:
	main()
except Exception as e:
	print(e)
except KeyboardInterrupt:
	print(bcolors.FAIL+"[!] "+bcolors.RESET+"Script canceled.")
