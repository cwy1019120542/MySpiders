import re,requests,pymysql,time,random
db=pymysql.connect(host='localhost',db='proxy_ip',user='root',passwd='never1019120542,',charset='utf8')
db.autocommit(True)
cursor=db.cursor()
headers1={
'Accept':'image/webp,image/apng,image/*,*/*;q=0.8',
'Accept-Encoding':'gzip, deflate, br',
'Accept-Language':'zh-CN,zh;q=0.9',
'Connection':'keep-alive',
'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
}
headers2={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
for page in range(1,1000):
	url1='http://www.xicidaili.com/nn/'+str(page)
	print(url1)
	sql1='select * from ip'
	cursor.execute(sql1)
	all_url=cursor.fetchall()
	#print(all_url)
	time.sleep(3)
	while True:
		try:
			http_https=random.choice(all_url)
			html1=requests.get(url1,headers=headers1,proxies={'https':http_https[1],'http':http_https[0]},timeout=15).text
			if not re.findall(r'<td>([0-9.]+)</td>\n      <td>(\d+)</td>',html1,re.RegexFlag.S):
				print('{}代理被封'.format(http_https[1]))
				continue
		except Exception as error:
			print(error)
			continue
		else:
			break
	ip_lists=re.finditer(r'<td>([0-9.]+)</td>\n      <td>(\d+)</td>',html1,re.RegexFlag.S)
	#print(ip_lists)
	for ip_port in ip_lists:
		ip=ip_port.group(1)
		port=ip_port.group(2)
		url_http='http://'+ip+':'+port
		url_https='https://'+ip+':'+port
		try:
			reponse2=requests.get('https://www.baidu.com/',headers=headers2,proxies={'http':url_http,'https':url_https},timeout=15)
		except:
			print('{}代理失效'.format(url_https))
			continue
		if reponse2.status_code == 200:
			sql="insert into ip values ('{}','{}')".format(url_http,url_https)
			cursor.execute(sql)
			print('{}代理爬取完成'.format(url_https))
db.close()
print('end')