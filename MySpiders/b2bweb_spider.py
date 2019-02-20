from requests_html import HTMLSession
import re
headers={
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
'Accept-Encoding': 'gzip, deflate',
'Accept-Language': 'zh-CN,zh;q=0.9',
'Connection': 'keep-alive',
'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.96 Safari/537.36'
}
session=HTMLSession()
html1=session.get(r'http://www.benbenseo.com/product/html/?92.html',headers=headers).html
tag_obj_list=html1.xpath('//*[@id="spdv_11413"]/div/div[2]/div/a')
for tag_obj in tag_obj_list:
	url=tag_obj.attrs['href']
	number=re.findall(r'\d+',url)[0]
	#print(number)
	html3=session.get(f'http://www.benbenseo.com/product/class/index.php?page=1&catid={number}&myord=uptime&myshownums=9&showtj=&author=&key=',headers=headers).html
	page_all=html3.xpath('//*[@id="pagesinfo"]/text()')[0][-1]
	#print(page_list)
	page=1
	for page in range(1,int(page_all)+1):
		html2=session.get(f'http://www.benbenseo.com/product/class/index.php?page={page}&catid={number}&myord=uptime&myshownums=9&showtj=&author=&key=',headers=headers).html
		name_list=html2.xpath('//*[@id="spdv_11390"]/div/div[2]/div/div[2]/a')
		web_list=html2.xpath('//*[@id="spdv_11390"]/div/div[2]/div/div[1]/div/div/a')
		for name,web in zip(name_list,web_list):
			name=name.text.strip()
			url='http://www.benbenseo.com/'+web.attrs['href'].strip('./')
			html3=session.get(url,headers=headers).html
			try:
				web_url=html3.xpath('//*[@id="prop"]/text()[6]')[0].strip().strip(r'网址： ')
			except Exception as error:
				print(error)
				continue
			print(name+r'		'+web_url)
		page+=1
print('end')