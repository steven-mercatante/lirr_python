import argparse
import requests
import time
import sys
from bs4 import BeautifulSoup

# Todos:
# catch and report invalid station combos
# ensure from, to station ids are valid

class Lirr():

	def __init__(self):
		self.stations = {
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

		self.routes_methods = ['list', 'add', 'del', 'def']


	def show_stations(self):
		"""
		Prints list of LIRR train stations
		"""
		for id, name in self.stations.iteritems():
			print id, name

	def get_times(self, from_station, to_station):
		"""
		Fetches upcoming LIRR train times
		"""
		# Query LIRR for times
		alt_time = self.get_altered_time()
		payload = {
			'FromStation': from_station,
			'ToStation': to_station,
			'RequestDate': time.strftime('%m/%d/%Y', alt_time),
			'RequestTime': time.strftime('%I:%M', alt_time),
			'RequestAMPM': time.strftime('%p', alt_time),
			'sortBy': 1,
			'schedules': 'Schedules'
		}
		r = requests.post('http://lirr42.mta.info/index.php', data=payload)

		# Extract the departure, arrival times from response
		soup = BeautifulSoup(r.content)

		station_links = soup.find('table', {'style': 'width:100%;'}) \
			.findAll('a')[0:2]

		label = '%s to %s' % (station_links[0].text.strip(), 
			station_links[1].text.strip())

		depart_times = []
		arrive_times = []
		tag_params = {'class': 'schedulesTD', 
			'style': 'text-align:right; width=60px;'
		}
		for i, node in enumerate(soup.findAll('td', tag_params)):
			if i % 2 == 0:
				depart_times.append(node.find(text=True))
			else:
				arrive_times.append(node.find(text=True))

		output = label + ': '
		output += ' | '.join(depart_times)
		return output

	def get_altered_time(self):
		"""
		LIRR always returns the previous two train times. I only want train
		times in the future - by altering the time we send to their server,
		we should get back future times only.
		"""
		t = time.time() + 3600
		return time.localtime(t)

class RouteManager():
	def list():
		pass

	def add():
		pass

	def delete():
		pass

	def default():
		pass

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('-s', '--stations', dest='show_stations', 
		action='store_true', default=False,
		help='Shows list of stations')
	parser.add_argument('-f', '--from', dest='from_station', type=int, 
		help='The station to depart from')
	parser.add_argument('-t', '--to', dest='to_station', type=int, 
		help='The station to arrive at')
	parser.add_argument('--routes', default=False, nargs='+')
	args = parser.parse_args()	

	if args.from_station and not args.to_station:
		parser.error('Please provide a destination station')

	if args.to_station and not args.from_station:
		parser.error('Please provide a departure station')

	if (args.from_station and args.to_station) and (args.from_station == args.to_station):
		parser.error('The departure and destination stations cannot be the same')

	lirr = Lirr()

	if args.show_stations:
		lirr.show_stations()
	elif args.routes:
		pass
	else: 
		print lirr.get_times(args.from_station, args.to_station)
