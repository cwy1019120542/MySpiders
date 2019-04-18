from super_spider import SuperSpider
from collections import deque
import time
import random
import asyncio
import aiohttp
# def hy88_spider():
# 	hy88=SuperSpider(default_field='-')
# 	hy88_list=deque([],maxlen=35)
# 	proxies_list=hy88.sql_search('select ip from ip_pool')
# 	url_list1=hy88.data_search('http://www.huangye88.com/','//div[@class="main_box main_box1"]//div[@class="dl_list clearfix"]//dl//dd/a/@href')
# 	for url1 in url_list1:
# 		url_list2=hy88.data_search(url1,['//ul[@class="app_list app_list2 clearfix"]//li//a/text()','//ul[@class="app_list app_list2 clearfix"]//li//a/@href'])
# 		if url_list2[0]:
# 			for profession,url2 in zip(url_list2[0],url_list2[1]):
# 				try:
# 					page_all=hy88.data_search(url2,'//div[@class="pages"]//span[1]/text()')[0].strip('共页')
# 				except:
# 					page_all=1
# 				for page in range(1,int(page_all)+1):
# 					url3=url2+f'pn{page}/'
# 					url_list3=hy88.data_search(url3,'//ul[@class="pros"]//li//h2//a/@href')
# 					for url4 in url_list3:
# 						for i in range(10):
# 							proxies=random.choice(proxies_list)[0]
# 							key='http' if not proxies.startswith('https') else 'https'
# 							proxies_dict={key:proxies}
# 							print(f'使用代理-{proxies}')
# 							try:
# 								company_info_list=hy88.data_search(url4,['//div[@class="rigtop"]//p[@class="qyname"]//a/text()','//div[@class="rigtop"]//ul[@class="zying"]//li//span/text()','//div[@class="leftpron"]//p[@class="names"]//a/text()','//div[@class="leftpron"]//p[@class="iphone"]//span/text()','//div[@class="leftpron"]//div[@class="addres"]//p[@class="adtel"]//font/text()'],proxies=proxies_dict,timeout=3)
# 							except Exception as error:
# 								print(error)
# 								continue
# 							else:
# 								if not company_info_list[0]:
# 									continue
# 								hy88.company_name=company_info_list[0][0]
# 								if hy88.company_name in hy88_list:
# 									print(f'{hy88.company_name}-信息重复')
# 									continue
# 								else:
# 									hy88_list.append(hy88.company_name)
# 								hy88.main_product=company_info_list[1][0]
# 								hy88.person_name=company_info_list[2][0]
# 								hy88.phone_number=company_info_list[3][0]
# 								print(company_info_list)
# 								break

hy88=SuperSpider()
proxies_list=hy88.sql_search('select ip from ip_pool')




async def hy88_spider_task(url_list):
	sem=asyncio.Semaphore(500)
	tasks=[hy88_spider(sem,url) for url in url_list]
	await asyncio.wait(tasks)

async def hy88_spider(sem,url):
	async with sem:
		async with aiohttp.ClientSession() as session:
			for i in range(20):
				try:
					proxies=random.choice(proxies_list)[0]
					print(f'使用代理-{proxies}')
					async with session.get(url,headers=hy88.random_headers(),proxy=proxies,timeout=5) as response:
						html= await response.text()
						url_list2=hy88.data_search(html=html,xpath=['//ul[@class="app_list app_list2 clearfix"]//li//a/text()','//ul[@class="app_list app_list2 clearfix"]//li//a/@href'])
						if url_list2[0]:
							for profession,url2 in zip(url_list2[0],url_list2[1]):
								for i in range(20):
									try:
										proxies=random.choice(proxies_list)[0]
										print(f'使用代理-{proxies}')
										async with session.get(url2,headers=hy88.random_headers(),proxy=proxies,timeout=5) as response2:
											html2=await response2.text()
											try:
												page_all=hy88.data_search(html=html2,xpath='//div[@class="pages"]//span[1]/text()')[0].strip('共页')
											except:
												page_all=1
											for page in range(1,int(page_all)+1):
												url3=url2+f'pn{page}/'
												for i in range(20):
													try:
														proxies=random.choice(proxies_list)[0]
														print(f'使用代理-{proxies}')
														async with session.get(url3,headers=hy88.random_headers(),proxy=proxies,timeout=5) as response3:
															html3=await response3.text()
															url_list3=hy88.data_search(html=html3,xpath='//ul[@class="pros"]//li//h2//a/@href')
															for url4 in url_list3:
																for i in range(20):
																	try:
																		proxies=random.choice(proxies_list)[0]
																		print(f'使用代理-{proxies}')
																		async with session.get(url4,headers=hy88.random_headers(),proxy=proxies,timeout=5) as response4:
																			html4=await response4.text()
																			company_info_list=hy88.data_search(html=html4,xpath=['//div[@class="rigtop"]//p[@class="qyname"]//a/text()','//div[@class="rigtop"]//ul[@class="zying"]//li//span/text()','//div[@class="leftpron"]//p[@class="names"]//a/text()','//div[@class="leftpron"]//p[@class="iphone"]//span/text()','//div[@class="leftpron"]//div[@class="addres"]//p[@class="adtel"]//font/text()'])
																			print(company_info_list)
																	except Exception as error:
																		print(error)
																		continue
													except Exception as error:
														print(error)
														continue
									except Exception as error:
										print(error)
										continue
				except Exception as error:
					print(error)
					continue





def hy88_spider_run():
	url_list=hy88.data_search('http://www.huangye88.com/','//div[@class="main_box main_box1"]//div[@class="dl_list clearfix"]//dl//dd/a/@href')
	loop=asyncio.get_event_loop()
	loop.run_until_complete(hy88_spider_task(url_list))

hy88_spider_run()