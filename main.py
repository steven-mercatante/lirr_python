import argparse
import requests
import time
from bs4 import BeautifulSoup

class Lirr():

	stations = {
		44: 'Albertson',
		137: 'Amagansett',
		115: 'Amityville',
		12: 'Atlantic Terminal',
		21: 'Auburndale',
		118: 'Babylon',
		107: 'Baldwin',
		119: 'Bay Shore',
		22: 'Bayside',
		33: 'Bellerose',
		110: 'Bellmore',
		126: 'Bellport',
		32: 'Belmont',
		68: 'Bethpage',
		73: 'Brentwood',
		135: 'Bridgehampton',
		20: 'Broadway',
		54: 'Carle Place',
		96: 'Cedarhurst',
		74: 'Central Islip',
		101: 'Centre Avenue',
		59: 'Cold Spring Harbor',
		116: 'Copiague',
		38: 'Country Life Press',
		72: 'Deer Park',
		23: 'Douglaston',
		136: 'East Hampton',
		14: 'East New York',
		102: 'East Rockaway',
		43: 'East Williston',
		99: 'Far Rockaway',
		69: 'Farmingdale',
		34: 'Floral Park',
		18: 'Flushing Main Street',
		10: 'Forest Hills',
		108: 'Freeport',
		37: 'Garden City',
		93: 'Gibson',
		50: 'Glen Cove',
		47: 'Glen Head',
		49: 'Glen Street',
		25: 'Great Neck',
		121: 'Great River',
		61: 'Greenlawn',
		82: 'Greenport',
		46: 'Greenvale',
		132: 'Hampton Bays',
		39: 'Hempstead',
		91: 'Hempstead Gardens',
		94: 'Hewlett',
		56: 'Hicksville',
		30: 'Hollis',
		2: 'Hunterspoint Avenue',
		60: 'Huntington',
		98: 'Inwood',
		104: 'Island Park',
		120: 'Islip',
		15: 'Jamaica',
		11: 'Kew Gardens',
		63: 'Kings Park',
		90: 'Lakeview',
		85: 'Laurelton',
		97: 'Lawrence',
		117: 'Lindenhurst',
		24: 'Little Neck',
		84: 'Locust Manor',
		51: 'Locust Valley',
		105: 'Long Beach',
		1: 'Long Island City',
		100: 'Lynbrook',
		89: 'Malverne',
		26: 'Manhasset',
		113: 'Massapequa',
		114: 'Massapequa Park',
		127: 'Mastic Shirley',
		80: 'Mattituck',
		508: 'Meadowlands',
		77: 'Medford',
		41: 'Merillon Avenue',
		109: 'Merrick',
		17: 'Mets-Willets Point',
		42: 'Mineola',
		138: 'Montauk',
		19: 'Murray Hill',
		36: 'Nassau Boulevard',
		40: 'New Hyde Park',
		62: 'Northport',
		13: 'Nostrand Avenue',
		122: 'Oakdale',
		103: 'Oceanside',
		53: 'Oyster Bay',
		124: 'Patchogue',
		8: 'Penn Station',
		70: 'Pinelawn',
		27: 'Plandome',
		67: 'Port Jefferson',
		28: 'Port Washington',
		31: 'Queens Village',
		79: 'Riverhead',
		106: 'Rockville Centre',
		75: 'Ronkonkoma',
		86: 'Rosedale',
		45: 'Roslyn',
		123: 'Sayville',
		48: 'Sea Cliff',
		112: 'Seaford',
		64: 'Smithtown',
		134: 'Southampton',
		81: 'Southold',
		129: 'Speonk',
		83: 'St. Albans',
		65: 'St. James',
		35: 'Stewart Manor',
		66: 'Stony Brook',
		58: 'Syosset',
		87: 'Valley Stream',
		111: 'Wantagh',
		92: 'West Hempstead',
		55: 'Westbury',
		130: 'Westhampton',
		88: 'Westwood',
		95: 'Woodmere',
		9: 'Woodside',
		71: 'Wyandanch',
		78: 'Yaphank'
	}

	def __init__(self):
		pass

	def get_stations(self):
		for id, name in self.stations.iteritems():
			print id, name

	def get_times(self, from_station, to_station):
		# These get populated later on
		depart_times = []
		arrive_times = []

		# Query LIRR for times
		payload = {
			'FromStation': from_station,
			'ToStation': to_station,
			'RequestDate': time.strftime('%m/%d/%Y'),
			'RequestTime': time.strftime('%I:%M'),
			'RequestAMPM': time.strftime('%A'),
			'sortBy': 1,
			'schedules': 'Schedules'
		}
		r = requests.post('http://lirr42.mta.info/index.php', data=payload)

		# Extract the departure, arrival times from response
		soup = BeautifulSoup(r.content)
		tag_params = {'class': 'schedulesTD', 
			'style': 'text-align:right; width=60px;'
		}
		for i, node in enumerate(soup.findAll('td', tag_params)):
			if i % 2 == 0:
				depart_times.append(node.find(text=True))
			else:
				arrive_times.append(node.find(text=True))

		return ' | '.join(depart_times)

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('from_station', type=int)
	parser.add_argument('to_station', type=int)
	args = parser.parse_args()

	lirr = Lirr()
	print lirr.get_times(args.from_station, args.to_station)