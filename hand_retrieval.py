from data_retrieval_functions import player_record
from data_retrieval_functions import hand_db_creator
from data_retrieval_functions import hand_db_no_match
from data_retrieval_functions import get_player_hands
import os
from lxml import etree
import time

parser = etree.HTMLParser()

prevHands = open('handdb.txt', 'r')
db = hand_db_creator(prevHands)
prevHands.close()
fetchPlayersIndex = [1, 5, 9, 11]
pH = open('handdb.txt', 'a')

for file in os.listdir('parsed_box_scores'):
	if file[0] != '.':
		fullFile = 'parsed_box_scores/' + file
		tree = etree.parse(fullFile, parser)
		root = tree.getroot()
		for ind in fetchPlayersIndex:
			for player in root.xpath('/html/body/div/div[3]/div[%i]/div[2]/table/tbody/tr/td[1]/a/@href' % ind):
				name = player[11:-6]
				if hand_db_no_match(db,name):
					hands = get_player_hands(name[0] + '/' + name)
					db.append(player_record(name, hands[0], hands[1]))
					pH.write('\n' + name + ',' + hands[0] + ',' + hands[1])