from super_spider import SuperSpider
import time
def xarcw_spider():
	word_list=['网络']
	xarcw=SuperSpider(host='192.168.0.172',default_field='-')
	xarcw.source_name='新安人才网'
	data={
	'memberName': '13155291086',
	'password': 'never1019120542,'}
	xarcw.post_request('https://login.goodjobs.cn/index.php/action/UserLogin',data=data)
	for word in word_list:
		for city_code in range(1043,1061):
			for page in range(1,61):
				print(f'{word}-{city_code}-第{page}页')
				try:
					url_list=xarcw.data_search(f'https://search.goodjobs.cn/index.php?keyword={word}&boxwp=c{city_code}&page={page}','//div[@class="dw_table"]//span[@class="e1"]/a/@href')
				except:
					print(f'{word}-{city_code}-第{page}页获取失败')
					continue
				if not url_list:
					print(f'{word}-{city_code}-第{page}页-爬取结束')
					break
				for url in url_list:
					# print(url)
					xarcw.source_page=url
					time.sleep(1)
					data_list=xarcw.data_search(url,['//p[@class="cname"]/a/text()','//p[@class="msg ltype"]/text()','//div[@class="w706 clearfix"]/text()','//div[@class="w706 clearfix"]/img/@src','//div[@class="comadress clearfix"]/text()'])
					if not data_list[0] or not data_list[3]:
						continue
					if not data_list[0]:
						data_list=xarcw.data_search(url,['//div[@class="w240 whitespace pb16"]//a[@class="org"]/text()','//div[@class="w240 whitespace pb16"]//p[@class="grey lh28"]/span[@class="black"]/text()','//p[@class="duol mt20"]/text()','//p[@class="duol mt20"]/img/@src','//div[@class="comadress clearfix"]/text()'])
						xarcw.company_type=data_list[1][0]
						xarcw.main_product=data_list[1][2]
					else:
						company_info_list=[i.strip('\xa0\xa0\n ') for i in data_list[1][0].split('|')]
						xarcw.company_type=company_info_list[0]
						for j in company_info_list[1:]:
							if '-' in j:
								xarcw.staff_number=j
							else:
								xarcw.main_product=j
					xarcw.company_name=data_list[0][0]
					xarcw.person_name=[i for i in data_list[2] if i.strip()][0]
					try:
						xarcw.phone_number=xarcw.use_tesseract(url=data_list[3][0],lang=None)
					except:
						continue
					xarcw.address=data_list[4][0].strip('工作地点：\u3000\n ')
					xarcw.data_save()
					print(f'{xarcw.company_name}-{xarcw.person_name}-{xarcw.phone_number}-导入完成')
xarcw_spider()
