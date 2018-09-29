from requests import Request,Session
from bs4 import BeautifulSoup 

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