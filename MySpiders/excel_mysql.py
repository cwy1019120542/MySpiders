import pymysql,openpyxl
db=pymysql.connect(host='localhost',user='root',passwd='never1019120542,',db='smi',charset='utf8')
db.autocommit(True)
cursor=db.cursor()
workbook=openpyxl.load_workbook(r'C:\Users\Administrator\Desktop\智灵通表\GSM基础数据0718.xlsx')
sheet=workbook['Sheet1']
for row_values in sheet.values:
	#print(row_values)
	sql1='select id from smi_city where name="{}"'.format(row_values[0])
	cursor.execute(sql1)
	city=cursor.fetchone()
	#print(city)
	sql="insert into smi_district (name,city_id) values ('{}',{})".format(row_values[1],city[0])
	cursor.execute(sql)
	print('{}导入成功~'.format(row_values[1]))
print('end')
db.close()