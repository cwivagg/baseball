from lxml import etree
import urllib2
import time
import re

# Teams By Year DataBase
#  a data structure specifying which MLB teams exist in which year
#     -teams is a list of teams by their three-letter baseball-reference.com abbreviation
#     -years is a list of years
#     -pres_abs is a list of lists indicating whether the team existed in a given year
#         the ith jth element indicates whether team j existed in year i
class tby_db:
	def __init__(self, teams, years, pres_abs):
		self.teams = teams
		self.years = years
		self.pres_abs = pres_abs

# Teams By Year DataBase Creator
#  imports an externally created csv containing
#     -header row of team names
#     -one year per row
#     -0 or 1 for whether the team in the column existed in that year
#  returns a tby_db object
def tby_db_creator(f):
	t = f.readline().split(',')
	y = [];
	tf = [];
	for line in f:
		data_line = line.split(',')
		y.append(data_line[0])
		tf.append(data_line[1:-1])
	return tby_db(t[1:-1], y, tf)

# Object for storing the hand with which a player throws and hits
#  -1 for left
#   0 for switch
#   1 for right
class player_record:
	def __init__(self, name, throws, hits):
		self.name = name
		self.throws = throws
		self.hits = hits

# Hand Database Creator
#  Reads an external file containing rows with the following structure:
#  playername,throwing hand[-1/1],batting hand[-1/0/1]
# Returns a list of player_record objects.
def hand_db_creator(f):
	hand_db = []
	for line in f:
		data_line = line.split(',')
		p = player_record(data_line[0],data_line[1],data_line[2])
		hand_db.append(p)
	return hand_db

# Checks whether a player_record object exists in a list of player_record object for
#    a player with a given name
def hand_db_no_match(db, name):
	for player in db:
		if player.name == name:
			return False
	return True

# Retrieves a player's throwing and hitting hands from baseball-reference.com
#    Prints a screen message on success or failure.
#    No currently known page formats that cannot be read (includes all players in last
#       25 years), so function does not throw errors.
def get_player_hands(name):
	player_url = 'http://www.baseball-reference.com/players/' + name + '.shtml'
	print "Failing on " + player_url
	parser = etree.HTMLParser()
	page = urllib2.urlopen(player_url)
	tree = etree.parse(page, parser)
	root = tree.getroot()
	try:
		handString = root.xpath('/html/body/div/div[3]/table/tr/td[2]/p[2]')[0]
	except:
		handString = root.xpath('/html/body/div/div[3]/p[2]')[0]
	handString = etree.tostring(handString)
	time.sleep(3)
	print 'Retrieved hand from', player_url
	return [handString[re.search('Bats:', handString).end()+10], \
		handString[re.search('Throws:', handString).end()+10] ]