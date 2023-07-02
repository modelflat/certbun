# certbun

Slightly improved version of [certbun](https://github.com/porkbundomains/certbun).

## What?

Porkbun's minimalist Certbot alternative leaves the certificate generation to Porkbun and simply downloads certs to the location of your choosing, then reloads your web server with the command of your choosing.

## Why?

Automated SSL cert generation software such as Certbot can be tricky to set up, especially if you want a wildcard certificate, which requires DNS access, or you use an unusual web server. Porkbun already has a massive certificate generation infrastructure, and a certificate API. You can let Porkbun handle the hassle of generating the certificate, and use certbun to pull it via the API and install it locally.

## Before you install

For `certbun` to work you'll need to generate API keys. Check out our [Getting Started Guide](https://kb.porkbun.com/article/190-getting-started-with-the-porkbun-dns-api) for more info on that.

We recommend [manually downloading the certificate bundle](https://kb.porkbun.com/article/71-how-your-free-ssl-certificate-works) and getting it working with your web server first, before trying to automate the process via certbun. Once your web server is reliably serving HTTPS traffic with no issue, you can automate the renewal process with certbun.

## Installation 

1. Install Python if it's not already installed
2. Drop `certbun.py` and `config.json.example` to the location of your choice
3. Rename `config.json.example` to `config.json` and fill it in:
	- set `apikey` and `secretapikey` fields to your API keys
	- set `domain` field to the domain you wish to pull certs for
	- set `domainCertLocation`, `privateKeyLocation`, `intermediateCertLocation` and `publicKeyLocation` fields with where you want the retrieved certificates to be saved. If your web server doesn't need the intermediate cert and public key, you can remove these fields.
	- set `commandToReloadWebserver` field with the command you typically execute to get your web server to load the new certificate bundle. This command will run immediately after the files have been copied into place. I usually use `/sbin/service nginx reload` on Amazon Linux VPS instances I administer, but the command will vary depending on your web server and operating system. If you don't want `certbun.py` to run any command, remove this field.

## Running certbun

### Manually

```bash
python certbun.py /path/to/config.json
```

### Add it to cron

Since this client works in a fairly non-sophisticated way, you probably just want to download certs every week or so and restart your web server. 

Edit your crontab with:

```bash
crontab -e
```

If you've never done this before, you may want to read a guide on how to do it. 

Assuming you wanted certbun to run once per week, you'd add a line like:

```
23 1 * * 1 python /path/to/certbun.py /path/to/config.json | logger
```