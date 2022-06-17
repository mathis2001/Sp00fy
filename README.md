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

- requests_html

if you want to use the email find funtion you will have to copy your [hunter.io](https://hunter.io/api-keys) api key access and paste it in your environment variables as 'HUNTER_KEY'.

![image](https://user-images.githubusercontent.com/40497633/173600536-26996bd7-4a7d-490f-bb16-bbf5a659d962.png)


## Usage:
```bash
usage: ./sp00fy.py [-h] [-d DOMAIN] [-f] [-l LIMIT] [-s]
```
## options:
```bash
optional arguments:
  -h, --help            show this help message and exit
  -d DOMAIN, --domain DOMAIN   Target domain
  -f, --find-emails     Find emails for the given domain
  -s, --send   Send email anonymously
  -l LIMIT, --limit LIMIT   Number of results wanted

```

## Use case

You want to verify if your domain is vulnerable to email spoofing ?

You can use this tool to simply check your DMARC record. If it is potentially vulnerable, you can check for emails by using the '-f' option and use one of them to simulate the spoofing of it (exp: info@target.xyz). The anonymous mailer option is now available, it use https://emkei.cz to send your anonymous spoofed email.

If you receive the mail in your mailbox or spam, it confirm that your domain is vulnerable.

### Disclaimer: This tool have been designed to help testing email spoofing for your own domain or your company domain with authorizations. Please, do not use it for illegal purposes.

## Screens:

![tempsnip](https://user-images.githubusercontent.com/40497633/173594850-7715522f-4c6c-4cae-a18a-0c8d9ec5feae.png)

![tempsnip](https://user-images.githubusercontent.com/40497633/173595580-9fea5ca5-d811-46ae-ae0f-2053d19a748a.png)

![code](https://user-images.githubusercontent.com/40497633/174271419-496bf363-5fcb-437d-9d20-899d0d89383a.png)

![mail1](https://user-images.githubusercontent.com/40497633/174272921-0321ab52-ed7d-49dd-b124-c06b837ad99b.png)

![mail2](https://user-images.githubusercontent.com/40497633/174272998-4f57a252-571a-46a2-80d5-6a1910f9f04e.png)

