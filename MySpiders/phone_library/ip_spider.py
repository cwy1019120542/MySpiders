from super_spider import SuperSpider
import time
import random
from apscheduler.schedulers.blocking import BlockingScheduler
import aiohttp
import asyncio
def ip_spider1():
	ip=SuperSpider(host='192.168.0.172',table_name='ip_pool',field_list=['spider_datetime','source_name','source_page','ip','address'])
	ip.source_name='快代理'
	for page in range(1,100):
		print(f'第{page}页')
		ip.source_page=f'https://www.kuaidaili.com/free/inha/{page}/'
		data_list=ip.data_search(f'https://www.kuaidaili.com/free/inha/{page}/','//table[@class="table table-bordered table-striped"]//td/text()')
		for i in range(0,105,7):
			try:
				ip.ip=f'http://{data_list[i]}:{data_list[i+1]}'
				ip.address=data_list[i+4]
			except:
				break
			ip.data_save()
			print(f'{ip.source_name}-第{page}页-{ip.ip}-导入完成')
		time.sleep(10)
	ip.spider_end()

def ip_spider2():
	ip=SuperSpider(host='192.168.0.172',table_name='ip_pool',field_list=['spider_datetime','source_name','source_page','ip','address'])
	ip.source_name='89免费代理'
	page=1
	while True:
		ip.source_page=f'http://www.89ip.cn/index_{page}.html'
		data_list=ip.data_search(f'http://www.89ip.cn/index_{page}.html','//table[@class="layui-table"]//td/text()')
		if not data_list:
			break
		print(f'第{page}页')
		for i in range(0,75,5):
			try:
				ip_value=data_list[i].strip(' \n\t')
				ip_port=data_list[i+1].strip(' \n\t')
				ip.ip=f"http://{ip_value}:{ip_port}"
				ip.address=data_list[i+2].strip(' \n\t')
			except:
				break
			ip.data_save()
			print(f'{ip.source_name}-第{page}页-{ip.ip}-导入完成')
		page+=1
		time.sleep(2)
	ip.spider_end()
# ip_spider2()

async def ip_spider3(sem,url,ip,proxies_list):
	async with sem:
		async with aiohttp.ClientSession() as session:
			for i in range(20):
				try:
					proxies=random.choice(proxies_list)[0]
					print(f'使用代理-{proxies}')
					async with session.get(url,headers=ip.random_headers(),proxy=proxies,timeout=5) as response:
						html=await response.text()
						url_list2=['http://ip.zdaye.com/dayProxy/ip/'+ip.re_find(r'\d+',i).__next__().group()+'.html' for i in ip.data_search(html=html,xpath='//div[@class="col-md-12"]//div[@class="title"]//a/@href')]
						for url2 in url_list2:
							async with session.get(url2,headers=ip.random_headers(),proxy=proxies,timeout=5) as response2:
								html2=await response2.text()
								data_list=ip.data_search(html=html2,xpath='//div[@class="cont"]//text()',charset='gbk')
								if not data_list:
									continue
								else:
									for data in data_list:
										ip_index=data.find('@')
										ip.ip=f'http://{data[:ip_index]}'
										address_index=data.find(']')
										ip.address=data[address_index+1:]
										ip.source_name='站大爷'
										ip.source_page=url2
										ip.data_save()
										print(f'{ip.source_name}-{ip.ip}-导入完成')
									break
				except Exception as error:
					print(error)
					continue


async def ip_spider3_task(ip,proxies_list):
	sem=asyncio.Semaphore(500)
	tasks=[ip_spider3(sem,f'http://ip.zdaye.com/dayProxy/{page}.html',ip,proxies_list) for page in range(1,6)]
	await asyncio.wait(tasks)

def ip_spider3_run():
	headers={
	'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
	'Accept-Encoding': 'gzip, deflate',
	'Accept-Language':'zh-CN,zh;q=0.9',
	'Cache-Control': 'max-age=0',
	'Connection': 'keep-alive',
	'Cookie': 'acw_tc=792b121315526282356885461e0c5a3c57c2f3644ca7854ccdbc9c502d1ef5; ASPSESSIONIDSADQRDTR=ANOPOIJBEFGBOCBAJPPMKEDH; __51cke__=; Hm_lvt_8fd158bb3e69c43ab5dd05882cf0b234=1552552479,1552628110; __tins__16949115=%7B%22sid%22%3A%201552628109404%2C%20%22vd%22%3A%2018%2C%20%22expires%22%3A%201552630850318%7D; __51laig__=18; Hm_lpvt_8fd158bb3e69c43ab5dd05882cf0b234=1552629050',
	'Host': 'ip.zdaye.com',
	'Referer': 'http://ip.zdaye.com/dayProxy/3.html',
	'Upgrade-Insecure-Requests':'1',
	'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'
	}
	ip=SuperSpider(host='192.168.0.172',table_name='ip_pool',field_list=['spider_datetime','source_name','source_page','ip','address'],headers=headers)
	proxies_list=ip.sql_search('select ip from ip_pool')
	loop=asyncio.get_event_loop()
	loop.run_until_complete(ip_spider3_task(ip,proxies_list))
	ip.spider_end()
# ip_spider3_run()

def ip_spider4():
	ip=SuperSpider(host='192.168.0.172',table_name='ip_pool',field_list=['spider_datetime','source_name','source_page','ip','address'])
	ip.source_name='方法SEO'
	ip.source_page='https://ip.seofangfa.com/'
	data_list=ip.data_search('https://ip.seofangfa.com/','//table[@class="table"]//td/text()')
	for i in range(0,250,5):
		ip.ip=f'http://{data_list[i]}:{data_list[i+1]}'
		ip.address=data_list[i+3]
		ip.data_save()
		print(f'{ip.source_name}-{ip.ip}-导入完成')
	ip.spider_end()
# ip_spider4()

def ip_spider5():
	ip=SuperSpider(host='192.168.0.172',table_name='ip_pool',field_list=['spider_datetime','source_name','source_page','ip','address'])
	ip.source_name='开心代理'
	page=1
	while True:
		ip.source_page=f'http://ip.kxdaili.com/ipList/{page}.html#ip'
		data_list=ip.data_search(f'http://ip.kxdaili.com/ipList/{page}.html#ip','//table[@class="ui table segment"]//td/text()')
		if not data_list:
			break
		for i in range(0,70,7):
			ip.address=data_list[i+5]
			h_list=data_list[i+3].split(',')
			for h in h_list:
				ip.ip=f'{h.lower()}://{data_list[i]}:{data_list[i+1]}'
				ip.data_save()
				print(f'{ip.source_name}-第{page}页-{ip.ip}-导入完成')
		page+=1
	ip.spider_end()
# ip_spider5()

async def ip_spider6(sem,url,ip,proxies_list):
	async with sem:
		async with aiohttp.ClientSession() as session:
			for i in range(20):
				try:
					proxies=random.choice(proxies_list)[0]
					print(f'使用代理-{proxies}')
					async with session.get(url,proxy=proxies,timeout=5,headers=ip.random_headers()) as response:
						html=await response.text()
						data_list=ip.data_search(html=html,xpath=[f'//table[@id="ip_list"]//tr[{i}]//text()' for i in range(2,101)])
				except Exception as error:
					print(error)
					continue
				else:
					if not data_list:
						continue
					for datas in data_list:
						datas=[i for i in datas if i.strip()]
						if len(datas) == 7:
							ip.ip=f'{datas[4].lower()}://{datas[0]}:{datas[1]}'
							ip.address=datas[2]
						elif len(datas) == 6:
							ip.ip=f'{datas[4].lower()}://{datas[0]}:{datas[1]}'
							ip.address='-'
						else:
							continue
						ip.source_name='西刺代理'
						ip.source_page=url
						ip.data_save()
						print(f'{ip.source_name}-{ip.ip}-导入完成')
					break

async def ip_spider6_task(ip,proxies_list):
	sem=asyncio.Semaphore(500)
	tasks=[ip_spider6(sem,f'https://www.xicidaili.com/nn/{page}',ip,proxies_list) for page in range(1,100)]
	await asyncio.wait(tasks)

def ip_spider6_run():
	ip=SuperSpider(host='192.168.0.172',table_name='ip_pool',field_list=['spider_datetime','source_name','source_page','ip','address'])
	proxies_list=ip.sql_search('select ip from ip_pool')
	loop=asyncio.get_event_loop()
	loop.run_until_complete(ip_spider6_task(ip,proxies_list))
	ip.spider_end()

# ip_spider6_run()

def del_same():
	print('————开始去重————')
	ip=SuperSpider(host='192.168.0.172')
	ip.sql_search('create table tmp (select min(id) as id from ip_pool group by ip)')
	ip.sql_search('truncate table ip_pool_mid')
	ip.sql_search('insert into ip_pool_mid (spider_datetime,source_name,source_page,ip,address) select spider_datetime,source_name,source_page,ip,address from ip_pool where id in (select id from tmp)')
	ip.sql_search('truncate table ip_pool')
	ip.sql_search('rename table ip_pool to ip_pool2')
	ip.sql_search('rename table ip_pool_mid to ip_pool')
	ip.sql_search('rename table ip_pool2 to ip_pool_mid')
	ip.sql_search('drop table tmp')
	ip.spider_end()
	print('————去重完毕————')

async def ip_check(sem,proxies,ip):
	async with sem:
		async with aiohttp.ClientSession() as session:
			try:
				key='http' if not proxies.startswith('https') else 'https'
				url=f'{key}://www.baidu.com'
				async with session.get(url,headers=ip.random_headers(),proxy=proxies,timeout=5) as response:
					status_code=response.status
					if status_code != 200:
						ip.sql_search(f'delete from ip_pool where ip="{proxies}"')
						print(f'{proxies}-请求错误-不可用已删除')
					else:
						print(f'{proxies}-可用')
			except:
				ip.sql_search(f'delete from ip_pool where ip="{proxies}"')
				print(f'{proxies}-报错-不可用已删除')

async def ip_check_task(proxies_list,ip):
	sem=asyncio.Semaphore(500)
	tasks=[ip_check(sem,proxies[0],ip) for proxies in proxies_list]
	await asyncio.wait(tasks)

def ip_check_run():
	del_same()
	ip=SuperSpider(host='192.168.0.172')
	proxies_list=ip.sql_search('select ip from ip_pool')
	loop=asyncio.get_event_loop()
	loop.run_until_complete(ip_check_task(proxies_list,ip))
	ip.spider_end()

def ip_spider7():
	ip=SuperSpider(host='192.168.0.172',table_name='ip_pool',field_list=['spider_datetime','source_name','source_page','ip','address'])
	page_all=ip.data_search('http://www.66ip.cn/index.html','//div[@id="PageList"]//a[last()-1]/text()')[0]
	for page in range(1,int(page_all)+1):
		data_list=ip.data_search(f'http://www.66ip.cn/{page}.html','//div[@class="containerbox boxindex"]//table//tr//text()','gbk')[5:]
		for i in range(0,10000,5):
			try:
				ip.ip=f'http://{data_list[i]}:{data_list[i+1]}'
				ip.address=data_list[i+2]
				ip.source_name='66代理'
				ip.source_page=f'http://www.66ip.cn/{page}.html'
				ip.data_save()
				print(f'{ip.source_name}-第{page}页-{ip.ip}-导入完成')
			except:
				break
	ip.spider_end()






def ip_all_spider():
	for i in range(3):
		ip_spider1()
		ip_spider2()
		ip_spider4()
		ip_spider5()
		ip_spider7()
		ip_check_run()
		ip_spider6_run()
		ip_check_run()
		ip_spider3_run()
		ip_check_run()
		time.sleep(25200)

if __name__ == '__main__':
	# ip_all_spider()
	scheduler=BlockingScheduler()
	scheduler.add_job(func=ip_all_spider,trigger='cron',hour=22,minute=0)
	scheduler.start()