import json
import sys
import os

try:
	from urllib.request import Request, urlopen
	from urllib.error import HTTPError
except ImportError:
	from urllib2 import Request, urlopen, HTTPError


def get_certificates(config):
	print('Downloading certs for ' + config['domain'])
	url = '{}/ssl/retrieve/{}'.format(config['endpoint'], config['domain'])
	headers = {'Content-Type': 'application/json'}
	data = json.dumps({'apikey': config['apikey'], 'secretapikey': config['secretapikey']}).encode('utf-8')
	try:
		response = urlopen(Request(url, data=data, headers=headers))
	except HTTPError as e:
		print('HTTP error: {} {}'.format(e.code, e.read().decode('utf-8')))
		sys.exit(1)
	response_json = json.loads(response.read())
	if response_json['status'] == 'ERROR':
		print('Error retrieving SSL: ' + response_json['message'])
		sys.exit(1)
	return response_json


def write_file(path, contents):
	if path:
		with open(path, 'w') as f:
			print('Installing ' + path)
			f.write(contents)


if len(sys.argv) <= 1:
	print(
		'certbun, a simpler way to keep your web server\'s SSL certificates current.\n\n'
		'Error: not enough arguments. Example:\n'
		'python certbun.py /path/to/config.json\n\n'
		'The config file contains your Porkbun API keys as well as the '
		'domain in question, the location on your file system to copy '
		'the keys, and the command to restart/reload the web server.'
	)
else:
	with open(sys.argv[1]) as f:
		config = json.load(f)

	cert_json = get_certificates(config)
	write_file(config['domainCertLocation'], cert_json['certificatechain'])
	write_file(config['privateKeyLocation'], cert_json['privatekey'])
	write_file(config.get('intermediateCertLocation'), cert_json['intermediatecertificate'])
	write_file(config.get('publicKeyLocation'), cert_json['publickey'])

	print('Done installing certificates.')

	restart_command = config.get('commandToReloadWebserver')
	if restart_command:
		print('Reloading server...')
		output = os.popen(restart_command).read()
		print(output + '\n')
