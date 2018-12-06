import requests,re,pymysql,time
headers={
'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
'Accept-Encoding':'gzip, deflate, br',
'Accept-Language':'zh-CN,zh;q=0.9',
'Connection':'keep-alive'}
db=pymysql.connect(host='localhost',user='root',passwd='never1019120542,',db='jsn_data',charset='utf8')
db.autocommit(True)
cursor=db.cursor()
print('start')
html=requests.get(r'https://cn.made-in-china.com/',headers=headers).text
#print(html)
url_lists=re.finditer(r'<dt class="sub-cata-item-hd">.*?<a target="_blank" href="(.*?)">.*?</a>',html,re.RegexFlag.S)
#print(url_lists)
for url in url_lists:
	url=url.group(1)
	#print(url)
	judge_url='https://cn.made-in-china.com'+url
	#print(judge_url)
	judge_html=requests.get(judge_url,headers=headers).text
	if re.findall(r'<div class="sl-vam-inner">',judge_html,re.RegexFlag.S):
		print('格式不符')
		continue
	url1_lists=re.finditer(r'<dd><a target="_blank" href="(.*?)">.*?</a></dd>',judge_html,re.RegexFlag.S) if re.findall(r'<dd><a target="_blank" href="(.*?)">.*?</a></dd>',judge_html,re.RegexFlag.S) else re.findall(r'<li><a href="(.*?)">.*?<img class="tagNew"',judge_html,re.RegexFlag.S)
	#print(url1_lists)
	if not url1_lists:
		continue
	for url1 in url1_lists:
		#print(url1)
		judge_url='https://cn.made-in-china.com'+url1
		try:
			judge_html=requests.get(judge_url,headers=headers).text
		except Exception as error:
			print(error)
			continue
		if re.findall(r'<input type="hidden" id="code" name="code" value="(.*?)"',judge_html,re.RegexFlag.S):
			code=re.findall(r'<input type="hidden" id="code" name="code" value="(.*?)"',judge_html,re.RegexFlag.S)[0]
		else:
			continue
		print('开始爬取{}类产品'.format(code))
		url3='https://cn.made-in-china.com/productdirectory.do?propertyValues=&action=item&senior=0&certFlag=0&code={0}&code4BrowerHistory={0}&order=3&style=b&comProvince=&comCity=&size=20&viewType=3&sizeHasChanged=0&uniqfield=1&priceStart=&priceEnd=&quantityBegin=&tradeType=&from=item&flag=999&channel=jixie'.format(code)
		page=0
		while True:
			page+=1
			url4=url3+'&page='+str(page)
			try:
				print('第{}页'.format(page))
				reponse2=requests.get(url4,headers=headers)
			except Exception as error:
				print(error)
				continue
			if reponse2.status_code != 200:
				break
			html2=reponse2.text
			url5_lists=re.finditer(r'<div class="sl-vam-inner">.*?<a href="(.*?)"',html2,re.RegexFlag.S)
			for url5 in url5_lists:
				#print(url5.group(1))
				time.sleep(3)
				try:
					print(url5.group(1))
					html3=requests.get(url5.group(1),headers=headers).text
				except Exception as error:
					print(error)
					continue
				if re.findall(r'<span class="tit">(.*?)</span>',html3,re.RegexFlag.S):
					company_name=re.findall(r'<span class="tit">(.*?)</span>',html3,re.RegexFlag.S)[0].strip()
				elif re.findall(r'<h2 class="only-tit">(.*?)</h2>',html3,re.RegexFlag.S):
					company_name=re.findall(r'<h2 class="only-tit">(.*?)</h2>',html3,re.RegexFlag.S)[0].strip()
				elif re.findall(r'<h2 class="only-tit js-comname4seo">(.*?)</h2>',html3,re.RegexFlag.S):
					company_name=re.findall(r'<h2 class="only-tit js-comname4seo">(.*?)</h2>',html3,re.RegexFlag.S)[0].strip()
				elif re.findall(r'<div class="only-tit">(.*?)</div>',html3,re.RegexFlag.S):
					company_name=re.findall(r'<div class="only-tit">(.*?)</div>',html3,re.RegexFlag.S)[0].strip()
				elif re.findall(r'<div class="company-hd clear"> \n      <h2>(.*?)</h2>',html3,re.RegexFlag.S):
					company_name=re.findall(r'<div class="company-hd clear"> \n      <h2>(.*?)</h2>',html3,re.RegexFlag.S)[0].strip()
				else:
					continue
				boss_name=re.findall(r'<li> <strong>(.*?)</strong>.*?</li>',html3,re.RegexFlag.S)[0] if re.findall(r'<li> <strong>(.*?)</strong>.*?</li>',html3,re.RegexFlag.S) else '暂无'
				telephone=re.findall(r'电话：</span><strong class="contact-bd org">(.*?)</strong></li>',html3,re.RegexFlag.S)[0] if re.findall(r'电话：</span><strong class="contact-bd org">(.*?)</strong></li>',html3,re.RegexFlag.S) else '暂无'
				mobilephone=re.findall(r'手机：</span><strong class="contact-bd org">(.*?)</strong></li>',html3,re.RegexFlag.S)[0] if re.findall(r'手机：</span><strong class="contact-bd org">(.*?)</strong></li>',html3,re.RegexFlag.S) else '暂无'
				fax=re.findall(r'传真：</span><span class="contact-bd">(.*?)</span></li>',html3,re.RegexFlag.S)[0] if re.findall(r'传真：</span><span class="contact-bd">(.*?)</span></li>',html3,re.RegexFlag.S) else '暂无'
				address=re.findall(r'地址：</span> <span class="contact-bd">(.*?)</span> </li>',html3,re.RegexFlag.S)[0].replace(' &nbsp; ',' ') if re.findall(r'地址：</span> <span class="contact-bd">(.*?)</span> </li>',html3,re.RegexFlag.S) else '暂无'
				#print(company_name,boss_name,telephone,mobilephone,fax,address)
				sql="insert into china_made values ('{}','{}','{}','{}','{}','{}')".format(company_name,boss_name,telephone,mobilephone,fax,address)
				try:
					cursor.execute(sql)
				except Exception as error:
					print(error)
					continue
				print('{}公司信息导入完成'.format(company_name))
db.close()
print('end')