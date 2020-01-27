import requests
r = requests.get(url='http://anek.ws/anekdot/export8.php')
text = r.text.replace("<br />", "")
text = text.replace("&quot", "")
text = text.split(">")[2].split("</")[0]
print(text)