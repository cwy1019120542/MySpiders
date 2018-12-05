import requests,re,pymysql
db=pymysql.connect(host='localhost',user='root',passwd='never1019120542,',db='jsn_data',charset='utf8')
db.autocommit(True)
cursor=db.cursor()
html=requests.get(r'https://cn.made-in-china.com/').text
#print(html)
url_lists=re.finditer(r'<dt class="sub-cata-item-hd">.*?<a target="_blank" href="(.*?)">.*?</a>',html,re.RegexFlag.S)
#print(url_lists)
for url in url_lists:
	url=url.group(1)
	#print(url)
	judge_url='https://cn.made-in-china.com'+url
	print(judge_url)
	judge_html=requests.get(judge_url).text
	if not re.findall(r'<dd><a target="_blank" href=".*?">.*?</a></dd>|<li><a href=".*?">.*?<img class="tagNew"',judge_html,re.RegexFlag.S):
		continue
	url1_lists=re.finditer(r'<dd><a target="_blank" href="(.*?)">.*?</a></dd>',judge_html,re.RegexFlag.S) if re.findall(r'<dd><a target="_blank" href="(.*?)">.*?</a></dd>',judge_html,re.RegexFlag.S) else re.findall(r'<li><a href="(.*?)">.*?<img class="tagNew"',judge_html,re.RegexFlag.S)
	#print(url1_lists)
	for url1 in url1_lists:
		url1=url1.group(1)
		#print(url1)
		url2=url1.split('/')[-1]
		page=1
		url3=url2[:-5]
		#print(url3)
		while True:
			url4='https://cn.made-in-china.com/catalog/item999i132/'+url3+'-'+str(page)+'.html'
			html2=requests.get(url4).text
			url5_lists=re.finditer(r'<div class="sl-vam-inner">.*?<a href="(.*?)"',html2,re.RegexFlag.S)
			#print(url5_lists)
			for url5 in url5_lists:
				html3=requests.get(url5.group(1)).text
				if re.findall(r'<span class="tit">(.*?)</span>',html3,re.RegexFlag.S):
					company_name=re.findall(r'<span class="tit">(.*?)</span>',html3,re.RegexFlag.S)[0].strip()
				elif re.findall(r'<h2 class="only-tit">(.*?)</h2>',html3,re.RegexFlag.S):
					company_name=re.findall(r'<h2 class="only-tit">(.*?)</h2>',html3,re.RegexFlag.S)[0].strip()
				elif re.findall(r'<div class="only-tit">(.*?)</div>',html3,re.RegexFlag.S):
					company_name=re.findall(r'<div class="only-tit">(.*?)</div>',html3,re.RegexFlag.S)[0].strip()
				else:
					company_name='暂无'
				boss_name=re.findall(r'<li> <strong>(.*?)</strong>.*?</li>',html3,re.RegexFlag.S)[0] if re.findall(r'<li> <strong>(.*?)</strong>.*?</li>',html3,re.RegexFlag.S) else '暂无'
				telephone=re.findall(r'电话：</span><strong class="contact-bd org">(.*?)</strong></li>',html3,re.RegexFlag.S)[0] if re.findall(r'电话：</span><strong class="contact-bd org">(.*?)</strong></li>',html3,re.RegexFlag.S) else '暂无'
				mobilephone=re.findall(r'手机：</span><strong class="contact-bd org">(.*?)</strong></li>',html3,re.RegexFlag.S)[0] if re.findall(r'手机：</span><strong class="contact-bd org">(.*?)</strong></li>',html3,re.RegexFlag.S) else '暂无'
				fax=re.findall(r'传真：</span><span class="contact-bd">(.*?)</span></li>',html3,re.RegexFlag.S)[0] if re.findall(r'传真：</span><span class="contact-bd">(.*?)</span></li>',html3,re.RegexFlag.S) else '暂无'
				address=re.findall(r'地址：</span> <span class="contact-bd">(.*?)</span> </li>',html3,re.RegexFlag.S)[0].replace(' &nbsp; ',' ') if re.findall(r'地址：</span> <span class="contact-bd">(.*?)</span> </li>',html3,re.RegexFlag.S) else '暂无'
				#print(company_name,boss_name,telephone,mobilephone,fax,address)
				if company_name != '暂无':
					sql="insert into china_made values ('{}','{}','{}','{}','{}','{}')".format(company_name,boss_name,telephone,mobilephone,fax,address)
					cursor.execute(sql)
					print('{}公司信息导入完成'.format(company_name))
			page+=1
			url5='https://cn.made-in-china.com/catalog/item999i132/'+url3+'-'+str(page)+'.html'
			if requests.get(url5).url == url4:
				break
db.close()
print('end')