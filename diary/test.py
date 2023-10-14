import urllib.request as request

url = "blob:https://esia.gosuslugi.ru/6f340a4c-ae59-4e74-b08f-0777b4afaf91" 
# fake user agent of Safari
fake_useragent = 'Mozilla/5.0 (iPad; CPU OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A5355d Safari/8536.25'
r = request.Request(url, headers={'User-Agent': fake_useragent})
f = request.urlopen(r)

# print or write
print(f.read())
