# 1. Get yesterday's games.
	# a. Parse boxes.
	# b. Predict starting lineups.
# 2. Get today's games.
	# a. Predict starting pictures.
import datetime
from data_retrieval_functions import tby_db
from data_retrieval_functions import tby_db_creator
from lxml import etree
import os
from lxml.etree import tostring

teams = ['ANA','ARI','ATL','BAL','BOS','CHA','CHN','CIN','CLE','COL','DET','HOU','KCA','LAN','MIA','MIL','MIN','NYA','NYN','OAK','PHI','PIT','SDN','SEA','SFN','SLN','TBA','TEX','TOR','WAS']

import urllib2
import time

possibleGames = ['0','1','2']

d = datetime.date.today() - datetime.timedelta(1)

for i in possibleGames:
	for j in range(0,len(teams)):
		myURL = 'http://www.baseball-reference.com/boxes/' + teams[j] + \
			'/' + teams[j] + '2016' + d.strftime("%m%d") + i + '.shtml'
#		myURL = 'http://www.baseball-reference.com/boxes/' + teams[j] + \
#			'/' + teams[j] + '20160710' + i + '.shtml'
		print "Attempting " + myURL
		page = urllib2.urlopen(myURL)
		print "Retrieved " + myURL
		if page.geturl() == myURL:
			pageText = page.read()
			myFileName = 'box_scores/' + teams[j] + '2016' + d.strftime("%m%d") + i + '.txt'
#			myFileName = 'box_scores/' + teams[j] + '20160710' + i + '.txt'
			myFile = open(myFileName,'w')
			myFile.write(pageText)
			myFile.close()
		time.sleep(3)
parser = etree.HTMLParser()
outFile = open("todays_lineups.txt",'w')
for file in os.listdir('box_scores'):
	if file[0] != '.':
		tree = etree.parse('box_scores/' + file, parser)
		root = tree.getroot()
		box_score = root.xpath('//td[contains(@class," highlight_text bold_text")]/table/tr/td[1]/a/text()')
		awayTeam = box_score[0]
		homeTeam = box_score[1]
		lineups = root.xpath('//table[@class="sortable  stats_table"]')[4]
		for ind in range(9):
			batterIndex = ind+1
			batter = lineups.xpath('./tbody/tr[%i]/td[2]/a/@href' % batterIndex)[0][11:-6]
			outFile.write(str(batterIndex) + ',' + batter + ',' + awayTeam + '\n')
			batter = lineups.xpath('./tbody/tr[%i]/td[6]/a/@href' % batterIndex)[0][11:-6]
			outFile.write(str(batterIndex) + ',' + batter + ',' + homeTeam + '\n')
outFile.close()
outFile = open("todays_opposing_pitchers.txt",'w')
myURL = 'http://www.baseball-reference.com/previews/'
page = urllib2.urlopen(myURL)
tree = etree.parse(page, parser)
root = tree.getroot()
games = root.xpath('//table[@width]/tr/td/p')
for game in games:
	team1 = game.xpath('./b[2]/text()')[0][0:3]
	pitcher1 = game.xpath('./a[2]/@href')[0][11:-6]
	team2 = game.xpath('./b[1]/text()')[0][0:3]
	pitcher2 = game.xpath('./a[3]/@href')[0][11:-6]
	outFile.write(pitcher1 + ',' + team1 + '\n' + pitcher2 + ',' + team2 + '\n')
outFile.close()