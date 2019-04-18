from super_spider import SuperSpider
import time
from faker import Faker
import hashlib
import random
def md5_passwd(phone_number,passwd):
	deal_text=phone_number[:5]+passwd+phone_number[6:]
	m=hashlib.md5()
	m.update(deal_text.encode('utf8'))
	return m.hexdigest()
def xarcw_spider():
	f=Faker(locale='zh_CN')
	word_list=['python','web','数据库','运维']
	xarcw=SuperSpider(db='supery',table_name='post_tag',default_field='null',field_list=('post_id','tag_id'))
	# data={
	# 'memberName': '13155291086',
	# 'password': 'never1019120542,'}
	# xarcw.post_request('https://login.goodjobs.cn/index.php/action/UserLogin',data=data)
	post_list=xarcw.sql_search('select id from post')
	tag_list=xarcw.sql_search('select id from tag')
	number_list=(2,3,4,5)
	for post in post_list:
		number=random.choice(number_list)
		aim_tag=random.sample(tag_list,number)
		for tag in aim_tag:
			xarcw.post_id=post[0]
			xarcw.tag_id=tag[0]
			xarcw.data_save()
			print(f'{xarcw.post_id}-{xarcw.tag_id}-导入完成')
	# for word in word_list:
	# 	for city_code in range(1043,1061):
	# 		for page in range(1,61):
	# 			print(f'{word}-{city_code}-第{page}页')
	# 			try:
	# 				url_list=xarcw.data_search(f'https://search.goodjobs.cn/index.php?keyword={word}&boxwp=c{city_code}&page={page}','//div[@class="dw_table"]//span[@class="e1"]/a/@href')
	# 			except:
	# 				print(f'{word}-{city_code}-第{page}页获取失败')
	# 				continue
	# 			if not url_list:
	# 				print(f'{word}-{city_code}-第{page}页-爬取结束')
	# 				break
	# 			for url in url_list:
	# 				print(url)
	# 				time.sleep(1)
					# data_list=xarcw.data_search(url,['//p[@class="cname"]/a/text()','//p[@class="msg ltype"]/text()','//div[@class="w706 clearfix"]/text()','//div[@class="w706 clearfix"]/img/@src','//div[@class="comadress clearfix"]/text()','//p[@class="mt20 wdr lh28"]/text()'])
					# if not data_list[0]:
					# 	data_list=xarcw.data_search(url,['//div[@class="w240 whitespace pb16"]//a[@class="org"]/text()','//div[@class="w240 whitespace pb16"]//p[@class="grey lh28"]/span[@class="black"]/text()','//p[@class="duol mt20"]/text()','//p[@class="duol mt20"]/img/@src','//div[@class="comadress clearfix"]/text()','//p[@class="mt20 wdr lh28 corp_info_ind"]/text()'])
					# 	try:
					# 		xarcw.company_type=data_list[1][0]
					# 		xarcw.main_product=data_list[1][2]
					# 	except:
					# 		continue
					# else:
					# 	company_info_list=[i.strip('\xa0\xa0\n ') for i in data_list[1][0].split('|')]
					# 	xarcw.company_type=company_info_list[0]
					# 	for j in company_info_list[1:]:
					# 		if '-' in j:
					# 			xarcw.staff_number=j
					# 		else:
					# 			xarcw.main_product=j
					# xarcw.company_name=data_list[0][0]
					# if not data_list[3]:
					# 	xarcw.phone_number=f.phone_number()
					# else:
					# 	try:
					# 		xarcw.phone_number=xarcw.use_tesseract(url=data_list[3][0],lang=None)
					# 	except:
					# 		continue
					# if not xarcw.phone_number.startswith('1'):
					# 	xarcw.phone_number=f.phone_number()
					# xarcw.person_name=f.name()
					# xarcw.address=data_list[4][0].strip('工作地点：\u3000\n ')
					# xarcw.company_info='   '.join([i.strip(' \r\n•\xa0') for i in data_list[-1]])
					# xarcw.passwd=md5_passwd(xarcw.phone_number,'666666')
					# xarcw.mail=f.email()
					# xarcw.business_licence='business_licence.jpg'
					# xarcw.register_datetime=xarcw.spider_datetime
					# xarcw.is_check=1
					# xarcw.data_save()
					# print(f'{xarcw.company_name}-{xarcw.person_name}-{xarcw.phone_number}-导入完成')
					# data_list=xarcw.data_search(url,['//div[@class="cn"]//h1/text()','//div[@class="op"]//strong/text()','//div[@class="comadress clearfix"]/text()','//div[@class="t1 clearfix"]//span[@class="sp4"]/text()','//p[@class="duol mt20"]/text()'])
					# if not data_list[0]:
					# 	data_list=xarcw.data_search(url,['//h1[@class="fl fz22 w500"]/text()','//div[@class="fr zwx"]//strong/text()','//div[@class="comadress clearfix"]/text()','//div[@class="t1 clearfix"]//span[@class="sp4"]/text()','//p[@class="duol mt20 lh28 pb10"]/text()'])
					# # print(data_list)
					# xarcw.post_name=data_list[0][0].strip()
					# xarcw.salary=data_list[1][0].strip()
					# xarcw.work_place=data_list[2][0].strip('工作地点：\u3000\n ')
					# xarcw.post_info='   '.join([i.strip(' \r\n•\xa0') for i in data_list[-1]])
					# for info2 in data_list[3]:
					# 	if '招聘' in info2:
					# 		xarcw.recruit_number=info2
					# 	elif '经验' in info2:
					# 		xarcw.experience_require=info2
					# 	elif '学历' in info2:
					# 		xarcw.graduate_require=info2
					# if xarcw.recruit_number=='null':
					# 	xarcw.recruit_number='招聘5人' 
					# if xarcw.experience_require=='null':
					# 	xarcw.experience_require='一年以上工作经验' 
					# if xarcw.graduate_require=='null':
					# 	xarcw.graduate_require='本科学历' 
					# xarcw.update_datetime=xarcw.spider_datetime
					# xarcw.company_id=random.choice(id_list)[0]
					# xarcw.data_save()
					# print(f'{xarcw.post_name}-{xarcw.salary}-{xarcw.graduate_require}-导入完成')

xarcw_spider()

