from lxml.html import fromstring
import requests

import traceback
import pandas as pd 

def get_proxies():
	url = 'https://free-proxy-list.net/'
	response = requests.get(url)
	parser = fromstring(response.text)
	proxies = []
	for i in parser.xpath('//tbody/tr'):
		if i.xpath('.//td[7][contains(text(),"yes")]'):
			proxy = ":".join([i.xpath('.//td[1]/text()')[0], i.xpath('.//td[2]/text()')[0]])
			proxies.append(proxy)
			# print(proxy)
	return proxies

df = pd.DataFrame(get_proxies())
df.to_csv('proxies.csv')