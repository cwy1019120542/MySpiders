from super_spider import SuperSpider
test=SuperSpider(use_selenium=True)
test.selenium_get('https://www.cnblogs.com/songshu120/p/5182043.html')
a=test.selenium_label('//pre[@class="prettyprint http" and position()=3]')
print(a)