import json

import scrapy

from scrapy.loader import ItemLoader

from ..items import BokfinancialItem
from itemloaders.processors import TakeFirst
import requests

import requests

url = "https://www.bokfinancial.com/"

payload="scController=Resource&scAction=getRelatedResources&id=472b483b-bd58-4762-9481-20d12fca8209"
headers = {
  'authority': 'www.bokfinancial.com',
  'pragma': 'no-cache',
  'cache-control': 'no-cache',
  'sec-ch-ua': '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',
  'accept': '*/*',
  'x-requested-with': 'XMLHttpRequest',
  'sec-ch-ua-mobile': '?0',
  'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36',
  'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
  'origin': 'https://www.bokfinancial.com',
  'sec-fetch-site': 'same-origin',
  'sec-fetch-mode': 'cors',
  'sec-fetch-dest': 'empty',
  'referer': 'https://www.bokfinancial.com/insights-and-resources/insights-and-resources/personal-finance-resources',
  'accept-language': 'en-US,en;q=0.9,bg;q=0.8',
  'cookie': 'ASP.NET_SessionId=gh2umv5msjxjvffw4yqjvi5t; visid_incap_1918805=wShccWb3S7CHOws0kEhU6mUGbGAAAAAAQUIPAAAAAAA9d4vzcubvdwsfXQNv8ABc; ARRAffinity=615d2e2d2c2be9df6be06c077e807f1f2e1dd421e13efeab9890e3a9abbabd92; nlbi_1918805=J5VPVHQVUT7zQ/EKKgbN0QAAAACgx+HnguCMhiMX0ciJ/qRi; ORA_FPC=id=2387bcf69a9b1b9d73b1617681464720; SC_ANALYTICS_GLOBAL_COOKIE=d1e3e3dbb10b46c79f0ec3d19f5db411|True; _cls_v=d1be52ae-cf03-4c2f-93a4-fb88969ae73d; _cls_s=ce11c018-1b24-45c1-ba2e-ee5062611129:0; incap_ses_730_1918805=ly4GJXWHMBjsuEfHdXshCmNrbWAAAAAAh7ZeU6EB1dLpabGYtJY8Ow==; utag_main=v_id:0178a5f9069f000347ce1325b00303072001d06a00bd0$_sn:2$_se:4$_ss:0$_st:1617785768228$ses_id:1617783654347%3Bexp-session$_pn:4%3Bexp-session; incap_ses_730_1918805=aYlBffzNVhRSUUjHdXshClZsbWAAAAAATY39KqlI05NMoJJgbcPIXQ==; nlbi_1918805=6iCMBl5YQiMoQ8Z1KgbN0QAAAABQ1ytt76M9SSl+2RnWuo/g; visid_incap_1918805=VXlqbsO6R1+i//m25SQDwVZsbWAAAAAAQUIPAAAAAABFrB5nBq+p7JLciowq79vM; ARRAffinity=a7f781fdc1f788c48d6bf2b9e17d6505b6351d67c87c9576b42cfd32167a62f4; ASP.NET_SessionId=i4o1vwlwn5rfjdmwfiyd4d4j; SC_ANALYTICS_GLOBAL_COOKIE=138f640b429342e183b12c60f3e289a0|False'
}


class BokfinancialSpider(scrapy.Spider):
	name = 'bokfinancial'
	start_urls = ['https://www.bokfinancial.com/insights-and-resources/insights-and-resources/personal-finance-resources']

	def parse(self, response):
		data = requests.request("POST", url, headers=headers, data=payload)
		raw_data = json.loads(data.text)
		for post in raw_data['resources']:
			h3 = scrapy.Selector(text=post['title'])
			link = h3.xpath('//@href').get()
			yield response.follow(link, self.parse_post)

	def parse_post(self, response):
		title = response.xpath('//h1[@class="title"]/text()').get()
		if not title:
			return
		description = response.xpath('//div[@class="m44__content"]//text()[normalize-space()]').getall()
		description = [p.strip() for p in description if '{' not in p]
		description = ' '.join(description).strip()

		item = ItemLoader(item=BokfinancialItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)

		return item.load_item()
