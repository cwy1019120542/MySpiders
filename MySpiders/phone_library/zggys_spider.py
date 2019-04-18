import sys
sys.path.append(r'C:\Users\Administrator\Desktop\phone_library')
from super_spider import SuperSpider
import time
import random
def zggys_spider():
	zggys=SuperSpider(host='192.168.0.172',default_field='-')
	zggys.source_name='中国供应商'
	proxies_list=zggys.sql_search('select ip from ip_pool')
	url_list1=[i+'?p={}' for i in zggys.data_search('https://cn.china.cn/','//*[@id="content"]/div[1]/div[1]/div/div[2]/div/div[2]/div/ul/li/div[2]/a/@href')]
	profession_list=zggys.data_search('https://cn.china.cn/','//*[@id="content"]/div[1]/div[1]/div/div[2]/div/div[2]/div/ul/li/div[2]/a/text()','GBK')
	error_index=profession_list.index('睡袋')
	for url1,profession in zip(url_list1[error_index:],profession_list[error_index:]):
		page=1
		while True:
			time.sleep(2)
			print(f'{profession}——第{page}页')
			for i in range(20):
				proxies=random.choice(proxies_list)[0]
				print(f'使用代理-{proxies}')
				key='http' if not proxies.startswith('https') else 'https'
				try:
					url_list2=zggys.data_search(url1.format(page),'//ul[@class="extension_ul"]//h3[@class="title"]/a/@href','GBK',proxies={key:proxies},timeout=5)
				except Exception as error:
					print(error)
					continue
			if not url_list2:
				print(f'{profession}——第{page}页——没有数据')
				break
			for url2 in url_list2:
				for i in range(20):
					try:
						time.sleep(2)
						proxies=random.choice(proxies_list)[0]
						print(f'使用代理-{proxies}')
						key='http' if not proxies.startswith('https') else 'https'
						html=zggys.get_html(url2,charset='GBK',proxies={key:proxies},timeout=5)
						zggys.source_page=url2
						if zggys.data_search(html=html,xpath='//div[@class="column_xx"]//p//a/text()'):
							zggys.company_name=zggys.data_search(html=html,xpath='//div[@class="column_xx"]//p//a/text()')[0]
						company_info_list=[i for i in zggys.data_search(html=html,xpath='//ul[@class="business_xx"]//li//text()') if i.strip('\r\n |')]
						# print(company_info_list)
					except Exception as error:
						print(error)
						continue
					else:
						try:
							aim_index=company_info_list.index('经营模式')
							zggys.business_mode=company_info_list[aim_index+1]
						except:
							pass
						try:
							aim_index=company_info_list.index('注册资本')
							zggys.register_money=company_info_list[aim_index+1].strip()
						except:
							pass
						try:
							aim_index=company_info_list.index('企业类型')
							zggys.company_type=company_info_list[aim_index+1]
						except:
							pass
						try:
							aim_index=company_info_list.index('主营产品')
							zggys.main_product=company_info_list[aim_index+1]
						except:
							pass
						try:
							aim_index=company_info_list.index('公司地址')
							zggys.address=company_info_list[aim_index+1]
						except:
							pass
						try:
							zggys.person_name=zggys.data_search(html=html,xpath='//div[@class="personal_top"]//div[@class="t"]//span/text()')[0]
						except:
							pass
						phone_list=zggys.data_search(html=html,xpath='//div[@class="personal_bottom"]//span/text()')
						if not phone_list:
							# js=['var btn=document.querySelector(".see_a.inactive_scode");btn.click();']
							# try:
							# 	zggys.selenium_open(url2)
							# 	zggys.selenium_js(js,sleep_time=2)
							# 	zggys.phone_number=zggys.selenium_search('css_selector','.inactive_top .number').__next__()
							# 	phone_info_dict={i.split('\n')[0]:i.split('\n')[1].strip('QQ交谈') for i in zggys.selenium_search('css_selector','.inactive_right .txt p')}	
							# except:
							# 	continue		
							# zggys.fax=phone_info_dict.get('传真','-').strip()
							# zggys.qq=phone_info_dict.get('Q  Q','-').strip()
							# zggys.data_save()
							# zggys.phone_number=phone_info_dict.get('电话','-').strip()
							# zggys.data_save()
							break
						for phone in phone_list:
							zggys.phone_number=phone.strip()
							zggys.data_save()	
						print(f'{profession}—第{page}页—{zggys.company_name}信息导入完成')
					break
			page+=1
	zggys.spider_end()
	
if __name__ == '__main__':
	zggys_spider()