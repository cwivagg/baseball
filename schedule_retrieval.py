# Carl Wivagg
# schedule_retrieval.py
# This script uses an external file containing lists of MLB teams by year.
# For each year, for each team, it retrieves from baseball-reference.com the team's
#    schedule for that year.
# It then stores the entire schedule in a "schedules" subdirectory of the current
#    directory.

from data_retrieval_functions import tby_db
from data_retrieval_functions import tby_db_creator
from lxml import etree
import urllib2
import time

fteams = open('teams_by_year.csv', 'r')
db = tby_db_creator(fteams)
fteams.close()
teams = db.teams
years = db.years
pres_abs = db.pres_abs

for i in range(0,len(years)):
	for j in range(0,len(teams)):
		if pres_abs[i][j] == '1':
			myURL = 'http://www.baseball-reference.com/teams/' + teams[j] + \
				'/' + years[i] + '-schedule-scores.shtml'
			page = urllib2.urlopen(myURL)
			pageText = page.read()
			myFileName = 'schedules/' + teams[j] + years[i] + '.txt'
			myFile = open(myFileName,'w')
			myFile.write(pageText)
			myFile.close()
			time.sleep(3)