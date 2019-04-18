import aiohttp
import asyncio
from super_spider import SuperSpider
ip=SuperSpider(host='192.168.0.172')
session=aiohttp.ClientSession()
async def ip_check(sem,proxies):
	async with sem:
		try:
			key='http' if not proxies.startswith('https') else 'https'
			url=f'{key}://www.baidu.com'
			async with session.get(url,headers=ip.random_headers(),proxy=proxies,timeout=3) as response:
				status_code=response.status
				if status_code != 200:
					ip.sql_search(f'delete from ip_pool where ip="{proxies}"')
					print(f'{proxies}-不可用已删除')
				else:
					print(f'{proxies}-可用')
		except:
			ip.sql_search(f'delete from ip_pool where ip="{proxies}"')
			print(f'{proxies}-不可用已删除')
proxies_list=ip.sql_search('select ip from ip_pool')
async def split_task():
	sem=asyncio.Semaphore(500)
	tasks=[ip_check(sem,proxies[0]) for proxies in proxies_list]
	await asyncio.wait(tasks)

loop=asyncio.get_event_loop()
loop.run_until_complete(split_task())
loop.close()
ip.spider_end()

				

