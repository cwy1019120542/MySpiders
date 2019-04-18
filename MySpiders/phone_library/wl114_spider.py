from super_spider import SuperSpider
def wl114_spider():
	wl114=SuperSpider()
	wl114.source_name='网络114'
	wl114.business_mode='-'
	wl114.register_money='-'
	wl114.website='-'
	wl114.qq='-'
	wl114.get_request('http://www.net114.com/')
	url_list1=[i.replace('.html','-p-{}.html') for i in wl114.data_search('xpath','//*[@id="product_center_content"]/div/ul/li/p/a',attr='href') if i.endswith('.html')]
	profession_list1=[i for i in wl114.data_search('xpath','//*[@id="product_center_content"]/div/ul/li/p/a') if i!='更多>>']
	error_index=profession_list1.index('维护工具')
	url_list2=(i for i in wl114.data_search('xpath','//*[@id="product_center_content"]/div/ul/li/p/a',attr='href') if not i.endswith('.html'))
	profession_list2=(i for i in wl114.data_search('xpath','//*[@id="product_center_content"]/div/ul/li/p/a') if i=='更多>>')
	for url1,profession1 in zip(url_list1[error_index:],profession_list1[error_index:]):
		try:
			wl114.get_request(url1.format(1))
			all_page=wl114.data_search('find','.page_p:not(span)').__next__().split('\xa0')[1]
		except:
			continue
		for page in range(1,int(all_page)+1):
			print(f'{profession1}——第{page}页')
			try:
				wl114.get_request(url1.format(page))
			except:
				continue
			url_list3=list(wl114.data_search('find','.product_list_div_h143 h2 a','href'))
			if not url_list3:
				break
			for url3 in url_list3:
				try:
					wl114.get_request(url3)
					company_info_dict={i.split('：')[0].strip():i.split('：')[-1].strip() for i in wl114.data_search('find','.right.w_250 .border.p_8 li') if '：' in i}
					phone_url=wl114.data_search('find','.right.w_250 .border.p_8 li a','href').__next__()
				except:
					continue
				wl114.company_type=company_info_dict.get('企业性质','-')
				wl114.main_product=company_info_dict.get('企业主营','-')
				wl114.address=company_info_dict.get('企业地址','-')
				try:
					wl114.get_request(phone_url)
				except:
					continue
				phone_info_data=wl114.data_search('find','td[valign="top"]:first-child')
				try:
					phone_info_list=phone_info_data.__next__().split('\n')
					phone_info_dict={i.split('：')[0].strip():i.split('：')[-1].strip() for i in phone_info_list if '：' in i}
				except:
					continue
				wl114.company_name=phone_info_dict.get('公司名称','-') 
				if wl114.company_name == '-':
					wl114.company_name=phone_info_dict.get('企业名称','-') 
				wl114.person_name=phone_info_dict.get('联系人','-')
				wl114.fax=phone_info_dict.get('传真','-')
				wl114.phone_number=phone_info_dict.get('手机','-')
				wl114.source_page=url3
				wl114.data_save()
				wl114.phone_number=phone_info_dict.get('联系电话','-')
				wl114.data_save()
				print(f'{profession1}——第{page}页——{wl114.company_name}信息导入完成')
			page+=1
	for url2 in url_list2:
		try:
			wl114.get_request(url2)
		except:
			continue
		url_list4=(i.replace('.html','-p-{}.html') for i in wl114.data_search('find','.product_w369_list a[href]','href'))
		profession_list4=wl114.data_search('find','.product_w369_list a[href]')
		for profession4,url4 in zip(profession_list4,url_list4):
			try:
				wl114.get_request(url4.format(1))
				all_page=wl114.data_search('find','.page_p:not(span)').__next__().split('\xa0')[1]
			except:
				continue
			for page in range(1,int(all_page)+1):
				print(f'{profession4}——第{page}页')
				try:
					wl114.get_request(url4.format(page))
				except:
					continue
				url_list3=list(wl114.data_search('find','.product_list_div_h143 h2 a','href'))
				if not url_list3:
					break
				for url3 in url_list3:
					try:
						wl114.get_request(url3)
						company_info_dict={i.split('：')[0].strip():i.split('：')[-1].strip() for i in wl114.data_search('find','.right.w_250 .border.p_8 li') if '：' in i}
						phone_url=wl114.data_search('find','.right.w_250 .border.p_8 li a','href').__next__()
					except:
						continue
					wl114.company_type=company_info_dict.get('企业性质','-')
					wl114.main_product=company_info_dict.get('企业主营','-')
					wl114.address=company_info_dict.get('企业地址','-')
					try:
						wl114.get_request(phone_url)
					except:
						continue
					phone_info_data=wl114.data_search('find','td[valign="top"]:first-child')
					try:
						phone_info_list=phone_info_data.__next__().split('\n')
						phone_info_dict={i.split('：')[0].strip():i.split('：')[-1].strip() for i in phone_info_list if '：' in i}
					except:
						continue
					wl114.company_name=phone_info_dict.get('公司名称','-') 
					if wl114.company_name == '-':
						wl114.company_name=phone_info_dict.get('企业名称','-') 
					wl114.person_name=phone_info_dict.get('联系人','-')
					wl114.fax=phone_info_dict.get('传真','-')
					wl114.phone_number=phone_info_dict.get('手机','-')
					wl114.source_page=url3
					wl114.data_save()
					wl114.phone_number=phone_info_dict.get('联系电话','-')
					wl114.data_save()
					print(f'{profession4}——第{page}页——{wl114.company_name}信息导入完成')
				page+=1
	wl114.spider_end()
wl114_spider()