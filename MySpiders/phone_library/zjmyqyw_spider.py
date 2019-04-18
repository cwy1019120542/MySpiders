import sys
sys.path.append(r'C:\Users\Administrator\Desktop\phone_library')
from super_spider import SuperSpider
from collections import deque
def zjmyqyw_spdier():
	company_deque=deque([],maxlen=35)
	zjmyqyw=SuperSpider()
	zjmyqyw.source_name='浙江名营企业网'
	zjmyqyw.fax='-'
	zjmyqyw.get_request('http://www.zj123.com/')
	url_list1=['http://www.zj123.com/'+i.replace('1.','{}.') for i in zjmyqyw.data_search('find','.indsort dd a','href')]
	profession_list=list(zjmyqyw.data_search('find','.indsort dd a'))
	error_index=profession_list.index('特种印刷')
	for profession,url1 in zip(profession_list[error_index:],url_list1[error_index:]):
		for page in range(1,100):
			print(f'{profession}——第{page}页')
			try:
				zjmyqyw.get_request(url1.format(page))
				page_judge=zjmyqyw.data_search('find','.sleft .m.m1 .fred').__next__().split()[0]
			except:
				print(f'获取第{page}页失败')
				page+=1
				continue
			if int(page_judge) != page:
				break
			url_list2=('http://www.zj123.com/member/VIPContact/'+i.split('-')[1]+'/index.htm' for i in zjmyqyw.data_search('find','.listdetail22 .listdetail dt a','href'))
			url_list3=('http://www.zj123.com/member/VIPCompany/'+i.split('-')[1]+'/index.htm' for i in zjmyqyw.data_search('find','.listdetail22 .listdetail dt a','href'))
			#print(url_list2)
			for url2,url3 in zip(url_list2,url_list3):
				try:
					zjmyqyw.get_request(url2)
				except:
					continue
				contact_info_dict={i.split('：')[0].strip():i.split('：')[-1].strip().replace('\xa0','') for i in zjmyqyw.data_search('find','.rkbody table tr')}
				zjmyqyw.company_name=contact_info_dict['公司名称'] if contact_info_dict['公司名称'] else '-'
				if zjmyqyw.company_name in company_deque:
					print('信息重复')
					continue
				zjmyqyw.person_name=contact_info_dict['联系人'] if contact_info_dict['联系人'] else '-'
				zjmyqyw.address=contact_info_dict['地 址'] if contact_info_dict['地 址'] else '-'
				zjmyqyw.phone_number=contact_info_dict['电 话'] if contact_info_dict['电 话'] else '-'
				zjmyqyw.qq=contact_info_dict['QQ'] if contact_info_dict['QQ'] else '-'
				zjmyqyw.website=contact_info_dict['网 址'] if contact_info_dict['网 址'] else '-'
				try:
					zjmyqyw.get_request(url3)
				except:
					continue
				company_info_list=list(zjmyqyw.data_search('find','.rkbody table tr td'))
				company_info_dict={company_info_list[n].strip('： '):company_info_list[n+1].strip(': ') for n in range(0,24,2)}
				#print(company_info_dict)
				zjmyqyw.main_product=company_info_dict['主营产品或服务'] if company_info_dict['主营产品或服务'] else '-'
				zjmyqyw.business_mode=company_info_dict['经营模式'] if company_info_dict['经营模式'] else '-'
				zjmyqyw.company_type=company_info_dict['企业类型'] if company_info_dict['企业类型'] else '-'
				zjmyqyw.register_money=company_info_dict['注册资本'] if company_info_dict['注册资本'] else '-'
				zjmyqyw.register_money=company_info_dict['员工人数'] if company_info_dict['员工人数'] else '-'
				zjmyqyw.source_page=url2
				zjmyqyw.data_save()
				zjmyqyw.phone_number=contact_info_dict['手机'] if contact_info_dict['手机'] else '-'
				zjmyqyw.data_save()
				company_deque.append(zjmyqyw.company_name)
				print(f'{profession}——第{page}页——{zjmyqyw.company_name}信息导入完成')
	zjmyqyw.spider_end()

if __name__ == '__main__':
	zjmyqyw_spdier()