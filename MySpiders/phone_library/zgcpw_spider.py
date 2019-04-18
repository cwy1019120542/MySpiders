from super_spider import SuperSpider
from collections import deque
def zgcpw_spider():
	zgcpw=SuperSpider()
	company_list=deque([],maxlen=35)
	zgcpw.source_name='中国产品网'
	zgcpw.get_request('http://www.pe168.com/')
	url_list1=zgcpw.data_search('find','td div:nth-child(2) a','href')
	profession_list=zgcpw.data_search('find','td div:nth-child(2) a')
	for profession,url1 in zip(profession_list,url_list1):
		try:
			zgcpw.get_request(url1)
			page_all=zgcpw.data_search('find','.pages cite').__next__()
			page_all_number=zgcpw.re_find(r'/(\d+)页',page_all).__next__().group(1)
		except:
			continue
		for page in range(1,int(page_all_number)+1):
			print(f'{profession}——第{page}页')
			url2=url1.replace('.html',f'-{page}.html')
			try:
				zgcpw.get_request(url2)
			except:
				continue
			url_list3=zgcpw.data_search('find','.left_box form tr ul li:nth-last-child(1) a','href')
			company_list3=zgcpw.data_search('find','.left_box form tr ul li:nth-last-child(1) a')
			for company_name,url3 in zip(company_list3,url_list3):
				if company_name in company_list:
					print('信息重复')
					continue
				company_list.append(company_name)
				zgcpw.company_name=company_name
				try:
					zgcpw.get_request(url3)
				except:
					continue
				zgcpw.source_page=url3
				try:
					company_info_url=zgcpw.data_search('find','a[title="公司介绍"]','href').__next__()
				except:
					company_list.append(company_name)
					continue
				try:
					zgcpw.get_request(company_info_url)
				except:
					continue
				company_info_list=list(zgcpw.data_search('find','.main_body:nth-last-child(1) td'))
				zgcpw.company_type=company_info_list[company_info_list.index('公司类型：')+1] if '公司类型：' in company_info_list else '-'
				zgcpw.staff_number=company_info_list[company_info_list.index('公司规模：')+1] if '公司规模：' in company_info_list else '-'
				zgcpw.register_money=company_info_list[company_info_list.index('注册资本：')+1] if '注册资本：' in company_info_list else '-'
				zgcpw.business_mode=company_info_list[company_info_list.index('经营模式：')+1] if '经营模式：' in company_info_list else '-'
				zgcpw.main_product=company_info_list[company_info_list.index('经营范围：')+1] if '经营范围：' in company_info_list else '-'
				try:
					phone_info_url=zgcpw.data_search('find','a[title="联系方式"]','href').__next__()
				except:
					company_list.append(company_name)
					continue
				try:
					zgcpw.get_request(phone_info_url)
				except:
					continue
				phone_info_list=list(zgcpw.data_search('find','.px13.lh18 td'))
				zgcpw.address=phone_info_list[phone_info_list.index('公司地址：')+1] if '公司地址：' in phone_info_list else '-'
				zgcpw.fax=phone_info_list[phone_info_list.index('公司传真：')+1] if '公司传真：' in phone_info_list else '-'
				zgcpw.website=phone_info_list[phone_info_list.index('公司网址：')+1] if '公司网址：' in phone_info_list else '-'
				zgcpw.person_name=phone_info_list[phone_info_list.index('联 系 人：')+1] if '联 系 人：' in phone_info_list else '-'
				zgcpw.phone_number=phone_info_list[phone_info_list.index('公司电话：')+1] if '公司电话：' in phone_info_list else '-'
				zgcpw.data_save()
				zgcpw.phone_number=phone_info_list[phone_info_list.index('手机号码：')+1] if '手机号码：' in phone_info_list else '-'
				zgcpw.data_save()
				print(f'{profession}——第{page}页——{company_name}导入完成')
	zgcpw.spider_end()
zgcpw_spider()
# test_obj=SuperSpider()
# test_obj.get_request('http://xmqiangjiu.com.pe168.com/contact/')
# print(list(test_obj.data_search('find','.px13.lh18 td')))
