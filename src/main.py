from requests import Request,Session
from bs4 import BeautifulSoup
import pandas as pd 


def log_d(code,product,name):
	print('[+]---message sent to Name:',name,'Link:',product[0],'---code',code)

def log_e(code,id_product):
	print('[-]---message not sent to ',id_product,'---code',code)

def get_header(host):	
	headers = {
		'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
		'Accept-Encoding': 'gzip, deflate, br',
		'Cache-Control': 'max-age=0',
		'Connection': 'keep-alive',
		'Host': host,
		'Upgrade-Insecure-Requests': '1',
		'Accept-Language': 'en-US,en;q=0.8',
		'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
	}
	return headers

def getId(url):
	return url.split('/')[-2].split('.')[0]

def sendMessage(name,email,message,id_product):
	
	playload = {"body":message,"email":email,"name":name}

	host = 'api.leboncoin.fr'
	
	url = 'https://api.leboncoin.fr/api/frontend/v1/classified/'+id_product+'/reply'
	session = Session()
	regions = {}
	with session.post(url=url,json=playload,headers=get_header(host)) as response:
		code = response.status_code
		return (code,response.text)

def getProductsByPage(url,page=1):
	if page>1:
		url = url+'p-'+str(page)+'/'
	session = Session()
	items = {}
	print ('\n-----------------------',url,'-----------------------\n')
	with session.request(method='GET',url=url,headers=get_header('www.leboncoin.fr')) as response:
		text_html = response.text
		soup = BeautifulSoup(text_html,'html.parser')
		if not(len(soup.findAll('p',attrs={"class": "_2fdgs"}))):
			li = soup.findAll('li',)
			itemtype="http://schema.org/Offer"
			for script in li:
				if script.has_attr('itemtype'):
					# print(script)
					soup1 = BeautifulSoup(str(script),'html.parser')
					links = soup1.findAll('a')[0]
					items[links.get('title')]=[links.get('href'),getId(links.get('href'))]
	return (items)


def sendMessageToUrl(url,name,email,message):
	page = 1
	results = getProductsByPage(url)
	while (len(results)):
		for (name_product,product) in results.items():
			code,text_response = sendMessage(name,email,message,product[1])
			if (code == 202) or (code == 200):
				log_d(code,product,name_product)
			elif(code == 422):
				print (text_response)
				log_e(code,product[1])
		page+=1
		results = getProductsByPage(url,page)


if __name__ == '__main__':
	name = input('Enter your name: ')
	email = input('Enter your email: ')
	message = input('Enter your message: ')
	data = pd.read_csv('links.csv',header=None)
	urls = list(data[0])
	for url in urls:
		sendMessageToUrl(url,name,email,message)