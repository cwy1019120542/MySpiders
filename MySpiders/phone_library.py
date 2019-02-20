def zggys_spider():	
	zggys=SuperSpider()
	zggys.source='中国供应商'
	zggys.website='-'
	html1=zggys.get_request('https://cn.china.cn/')
	url_list1=(i+'?p={}' for i in zggys.data_search(html1,'xpath','//*[@id="content"]/div[1]/div[1]/div/div[2]/div/div[2]/div/ul/li/div[2]/a','href'))	
	for url1 in url_list1:
		page=1
		while True:
			print(f'第{page}页')
			html2=zggys.get_request(url1.format(page))
			url_list2=zggys.data_search(html2,'find','h3.title a','href')
			if not url_list2:
				break
			for url2 in url_list2:
				html3=zggys.get_request(url2)
				try:
					zggys.company_name=zggys.data_search(html3,'find','.column_xx p a','title').__next__()
				except:
					continue
				company_info_list=(i for i in zggys.data_search(html3,'find','.business_xx').__next__().split('\n') if '|' in i)
				company_info_dict={i.split('|')[0]:i.split('|')[1] for i in company_info_list}
				zggys.business_mode=company_info_dict.get('经营模式','-') 
				zggys.register_money=company_info_dict.get('注册资本','-') 
				zggys.company_type=company_info_dict.get('企业类型','-') 
				zggys.main_product=company_info_dict.get('主营产品','-') 
				zggys.address=company_info_dict.get('公司地址','-') 
				#print(business_mode,register_money,company_type,main_product,address)
				zggys.person_name=zggys.data_search(html3,'find','.personal_top .t span').__next__()
				phone_list=zggys.data_search(html3,'find','.personal_bottom span')
				#print(phone_list)
				cell_phone_list=[]
				phone_code_list=[]
				for phone in phone_list:
					if not phone:
						js='var btn=document.querySelector(".see_a.inactive_scode");btn.click();'
						zggys.use_selenium()
						zggys.selenium_js(url2,js)
						zggys.cell_phone=zggys.selenium_search('css_selector','.inactive_top .number').__next__()
						phone_info_dict={i.split('\n')[0]:i.split('\n')[1].strip('QQ交谈') for i in zggys.selenium_search('css_selector','.inactive_right .txt p')}	
						zggys.phone_code=phone_info_dict.get('电话','-')
						zggys.fax=phone_info_dict.get('传真','-')
						zggys.qq=phone_info_dict.get('Q  Q','-')
					else:
						if not phone.startswith('1'):
							phone_code_list.append(phone)
						else:
							cell_phone_list.append(phone)
				if cell_phone_list or phone_code_list:
					zggys.phone_code='/'.join(phone_code_list) if phone_code_list else '-'
					zggys.cell_phone='/'.join(cell_phone_list) if cell_phone_list else '-'
					zggys.fax='-'
					zggys.qq='-'
				zggys.data_save()
				print(f'中国供应商——{zggys.company_name}信息导入完成')
			page+=1
	zggys.spider_end()
#zggys_spider()
def zjmyqyw():
	zjmyqyw=SuperSpider()
	zjmyqyw.source='浙江名营企业网'
	zjmyqyw.fax='-'
	html1=zjmyqyw.get_request('http://www.zj123.com/')
	url_list1=('http://www.zj123.com/'+i.replace('1.','{}.') for i in zjmyqyw.data_search(html1,'find','.indsort dd a','href'))
	for url1 in url_list1:
		page=1
		while True:
			print(f'第{page}页')
			html2=zjmyqyw.get_request(url1.format(page))
			page_judge=zjmyqyw.data_search(html2,'find','.sleft .m.m1 .fred').__next__().split()[0]
			if int(page_judge) != page:
				break
			print(page_judge)
			url_list2=('http://www.zj123.com/member/VIPContact/'+i.split('-')[1]+'/index.htm' for i in zjmyqyw.data_search(html2,'find','.listdetail22 .listdetail dt a','href'))
			url_list3=('http://www.zj123.com/member/VIPCompany/'+i.split('-')[1]+'/index.htm' for i in zjmyqyw.data_search(html2,'find','.listdetail22 .listdetail dt a','href'))
			#print(url_list2)
			for url2,url3 in zip(url_list2,url_list3):
				html3=zjmyqyw.get_request(url2)
				contact_info_dict={i.split('：')[0].strip():i.split('：')[-1].strip().replace('\xa0','') for i in zjmyqyw.data_search(html3,'find','.rkbody table tr')}
				zjmyqyw.company_name=contact_info_dict['公司名称'] if contact_info_dict['公司名称'] else '-'
				zjmyqyw.person_name=contact_info_dict['联系人'] if contact_info_dict['联系人'] else '-'
				zjmyqyw.address=contact_info_dict['地 址'] if contact_info_dict['地 址'] else '-'
				zjmyqyw.phone_code=contact_info_dict['电 话'] if contact_info_dict['电 话'] else '-'
				zjmyqyw.cell_phone=contact_info_dict['手机'] if contact_info_dict['手机'] else '-'
				zjmyqyw.qq=contact_info_dict['QQ'] if contact_info_dict['QQ'] else '-'
				zjmyqyw.website=contact_info_dict['网 址'] if contact_info_dict['网 址'] else '-'
				html4=zjmyqyw.get_request(url3)
				company_info_list=list(zjmyqyw.data_search(html4,'find','.rkbody table tr td'))
				company_info_dict={company_info_list[n].strip('： '):company_info_list[n+1].strip(': ') for n in range(0,24,2)}
				#print(company_info_dict)
				zjmyqyw.main_product=company_info_dict['主营产品或服务'] if company_info_dict['主营产品或服务'] else '-'
				zjmyqyw.business_mode=company_info_dict['经营模式'] if company_info_dict['经营模式'] else '-'
				zjmyqyw.company_type=company_info_dict['企业类型'] if company_info_dict['企业类型'] else '-'
				zjmyqyw.register_money=company_info_dict['注册资本'] if company_info_dict['注册资本'] else '-'
				zjmyqyw.data_save()
				print(f'浙江企业网——{zjmyqyw.company_name}信息导入完成')
			page+=1
	zjmyqyw.spider_end()
				
				
#zjmyqyw()
# test_obj=PhoneLibrary('测试')
# html=test_obj.post_request('https://www.china.cn/common/spider.php?v=9382').html
# print(html)