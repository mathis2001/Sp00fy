# Sp00fy
Simple python script to check for email spoofing on a given domain.

## Install:
```bash
$ git clone https://github.com/mathis2001/Sp00fy

$ cd Sp00fy

$ python3 sp00fy.py
```
## Requirements:

- Python3

- Pip3

- dns.resolver

- requests

if you want to use the email find funtion you will have to copy your [hunter.io](https://hunter.io/api-keys) api key access and paste it in your environment variables as 'HUNTER_KEY'.

![image](https://user-images.githubusercontent.com/40497633/173600536-26996bd7-4a7d-490f-bb16-bbf5a659d962.png)


## Usage:
```bash
usage: ./sp00fy.py [-h] [-d DOMAIN] [-f] [-l LIMIT]
```
## options:
```bash
optional arguments:
  -h, --help            show this help message and exit
  -d DOMAIN, --domain DOMAIN   Target domain
  -f, --find-emails     Find emails for the given domain
  -l LIMIT, --limit LIMIT   Number of results wanted

```

## Use case

You want to verify if your domain is vulnerable to email spoofing ?

You can use this tool to simply check your DMARC record. If it is potentially vulnerable, you can check for emails by using the '-f' option and use one of them to simulate the spoofing of it (exp: info@target.xyz). The anonymous message send is not already available so you can use https://emkei.cz to send your mail for the moment.

If you receive the mail in your mailbox or spam, it confirm that your domain is vulnerable.

Disclaimer: This tool have been made to help testing your own domain or your company domain with authorizations. Please, do not use it for illegal purposes.

## Screens:

![tempsnip](https://user-images.githubusercontent.com/40497633/173594850-7715522f-4c6c-4cae-a18a-0c8d9ec5feae.png)

![tempsnip](https://user-images.githubusercontent.com/40497633/173595580-9fea5ca5-d811-46ae-ae0f-2053d19a748a.png)

## TO DO:

add an option to send an anonymous mail with @target.xyz name
