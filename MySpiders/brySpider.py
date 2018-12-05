import time,re,pymysql,requests,json
from pyquery import PyQuery as pq
from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime,timedelta
db=pymysql.connect(host='localhost',db='bry_data',user='root',passwd='never1019120542,',charset='utf8')
db.autocommit(True)
cursor=db.cursor()
headers={
'Accept-Encoding':'gzip, deflate',
'Accept-Language':'zh-CN,zh;q=0.9',
'Connection':'keep-alive',
'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}

def mian_spider(url,scode,tdate,sname):
	q=pq(url=url,encoding='gb2312')
	field_lists=[None,None,None,None,None,None,None]
	field_lists2=[None,None,None,None,None,None,None]
	sql1='insert into lhb_data (date,type,code,name,kind,trade_department,buy_money,buy_proportion,sell_money,sell_proportion,net) values ("{}","{}","{}","{}","买入金额最大的第{}名","{}","{}","{}","{}","{}","{}")'
	sql2='insert into lhb_data (date,type,code,name,kind,trade_department,buy_money,buy_proportion,sell_money,sell_proportion,net) values ("{}","{}","{}","{}","卖出金额最大的第{}名","{}","{}","{}","{}","{}","{}")'
	sql3='insert into lhb_data (date,type,code,name,trade_department,buy_money,buy_proportion,sell_money,sell_proportion,net,kind) values ("{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","合计")'
	for k,l in enumerate(q('.left.con-br').items()):
		field_lists2[k]=l.text().split('类型：')[1]
	for h,i in enumerate(q('.content-sepe').items()):
		stype=field_lists2[h]
		for j in i.find('#tab-2 tbody tr').items():
			for k,l in enumerate(j.find('td').items()):
				field_lists[k]=l.text().split()[0]
			cursor.execute(sql1.format(tdate,stype,scode,sname,*field_lists))
			print('{}_{}_{}买入金额第{}名_导入成功'.format(tdate,stype,sname,field_lists[0]))
		for j in i.find('#tab-4 tbody tr').items():
			if not j.attr['class']:
				for k,l in enumerate(j.find('td').items()):
					field_lists[k]=l.text().split()[0]
				cursor.execute(sql2.format(tdate,stype,scode,sname,*field_lists))
				print('{}_{}_{}卖出金额第{}名_导入成功'.format(tdate,stype,sname,field_lists[0]))
		for k,l in enumerate(i.find('.total-tr td').items()):
			field_lists[k]=l.text()
		cursor.execute(sql3.format(tdate,stype,scode,sname,*field_lists))
		print('{}_{}_{}买入卖出合计_导入成功'.format(tdate,stype,sname))

def days30_spider():
	html1=requests.get(r'http://data.eastmoney.com/stock/tradedetail/2018-11-02.html',headers=headers).text
	date_group=re.findall(r'<li id="">近30日<input type="hidden" value="(.*?),(.*?)" /></li>',html1,re.RegexFlag.S)
	#print(date_group)
	start_date,end_date=date_group[0]
	#print(start_date,end_date)
	url2='http://data.eastmoney.com/DataCenter_V3/stock2016/TradeDetail/pagesize=50,page=1,sortRule=-1,sortType=,startDate={},endDate={},gpfw=0,js=var%20data_tab_2.html?rt=25731729'.format(start_date,end_date)
	html2=requests.get(url2,headers=headers).text
	#print(html2)
	json_data=json.loads(html2.lstrip('var data_tab_2='))
	#print(json_data)
	all_pages=json_data['pages']
	for page in range(1,all_pages+1):
		url3='http://data.eastmoney.com/DataCenter_V3/stock2016/TradeDetail/pagesize=50,page={},sortRule=-1,sortType=,startDate={},endDate={},gpfw=0,js=var%20data_tab_2.html?rt=25731729'.format(page,start_date,end_date)
		html3=requests.get(url3,headers=headers).text
		data_lists=json.loads(html3.lstrip('var data_tab_2='))['data']
		for data in data_lists:
			scode=data['SCode']
			tdate=data['Tdate']
			sname=data['SName']
			url4='http://data.eastmoney.com/stock/lhb,{},{}.html'.format(tdate,scode)
			print(url4)
			mian_spider(url4,scode,tdate,sname)
	db.close()
	print('end')

def latest_spider():
	q1=pq(url=r'http://data.eastmoney.com/stock/lhb.html',encoding='gb2312')
	for i in q1('.contentBox').items():
		tdate=i.find('.tit a').text().split()[0]
		for j in i.find('.lhbtable .wname a').items():
			#print(j.attr.href)
			if j.attr.title and j.attr.href and j.attr.data_code:
				sname=j.attr.title
				scode=j.attr.data_code
				url1='http://data.eastmoney.com'+j.attr.href
				print(url1)
				mian_spider(url1,scode,tdate,sname)
		break
	db.close()
	print('end')

def delete_data():
	last_year=(datetime.now()+timedelta(days=0)).strftime('%Y-%m-%d')
	sql4='delete from lhb_data where date<"{}"'.format(last_year)
	cursor.execute(sql4)
	print('已删除{}以前的数据'.format(last_year))
def run_spider():
	q2=pq(url=r'http://data.eastmoney.com/stock/lhb.html',encoding='gb2312')
	today=datetime.now().strftime('%Y-%m-%d')
	while True:
		#print(today)
		for i in q2('.contentBox').items():
			tdate=i.find('.tit a').text().split()[0].strip()
			break
		if tdate == today:
			print('数据已刷新，开始爬取')
			latest_spider()
			delete_data()
			break
		print('数据暂未刷新，等待10分钟')
		time.sleep(600)
	print('{}号数据爬取完成'.format(today))

if __name__ == '__main__':
	#days30_spider()
	scheduler=BlockingScheduler()
	scheduler.add_job(func=run_spider,trigger='cron',hour='17',minute='10',second='*')
	scheduler.start()




			



