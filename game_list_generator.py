from lxml import etree
import os
import urllib2
import time

parser = etree.HTMLParser()
for file in os.listdir('schedules'):
	fullFile = 'schedules/' + file
	if file[0] != '.':

		tree = etree.parse(fullFile, parser)
		root = tree.getroot()

		st = root.xpath('/html')
		scheduleTable = root.xpath('/html/body/div/div[5]/div[7]/div[2]/table/tbody')[0]
		for row in scheduleTable:
			if row.xpath('@class')[0] == '':
				if not row.xpath('./td[6]/text()'):
					p = row.xpath('./td[4]/a/@href')[0]
					myURL = 'http://www.baseball-reference.com' + p
					page = urllib2.urlopen(myURL)
					pageText = page.read()
					myFileName = 'box_scores/' + p[11:23] + '.txt'
					myFile = open(myFileName,'w')
					myFile.write(pageText)
					myFile.close()
					print 'Retrieved ' + myURL
					time.sleep(3)