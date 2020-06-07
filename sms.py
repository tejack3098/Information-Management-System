import requests
url = "https://www.fast2sms.com/dev/bulk"
numbers = [9930894939]
message = "Test okay"
#payload = "sender_id=FSTSMS&message=test&language=english&route=p&numbers=7045815501,9167639352"
def main(numbers,message):
    payload = "sender_id=FSTSMS&message="+message+"&language=english&route=p&numbers="
    for no in numbers:
        payload = payload+str(no)+","
    payload = payload[0:len(payload)-1]
    headers = {
    'authorization': "o7WLcylGHnUTp5sd4IiuxvEMYOSQZJq0N1R92ePmkKzwD3ha8rYurpD9Voc8e3CK5jbdSzkgiGMlXyQH",
    'Content-Type': "application/x-www-form-urlencoded",
    'Cache-Control': "no-cache",
    }
    print(payload)

    response = requests.request("POST", url, data=payload, headers=headers)
    print(response.text)

if __name__ == '__main__':
    main(numbers,message)
