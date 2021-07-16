import requests

url = 'https://api.pwnedpasswords.com/range/' + '5747B'
res = requests.get(url)
print(res)