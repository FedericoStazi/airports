#based on the .dat files in the data folder, downloaded from https://openflights.org/data.html

#-----     -----     imports     -----     -----#

from mpl_toolkits.basemap import Basemap
import numpy as np
import matplotlib.pyplot as plt, mpld3
import sys
import csv
import os
import json
import urllib.request

#-----     -----     variables     -----     -----#

airport_point = {}
m = Basemap(projection='robin',lon_0=0,resolution='c')
fig, ax = plt.subplots()
fig.set_size_inches(4, 2.5, forward=True)
data_is_read = False

#-----     -----     data variables     -----     -----#

airport_location = {}
airport_routes = {}
airline_routes = {}
airport_name = {}
airline_name = {}
airport_codes = {}
airline_codes = {}

#-----     -----     read data     -----     -----#

def read_data(): #read all data

	global data_is_read

	if data_is_read:
		return
	data_is_read = True

	print("reading data...")

	path=str(os.path.dirname(__file__))
	if not path:
		path="."

	if os.path.isfile(path+'/data/routes.dat') == False:
		print("Downloading routes.dat")
		urllib.request.urlretrieve('https://raw.githubusercontent.com/jpatokal/openflights/master/data/routes.dat', path+'/data/routes.dat')
	if os.path.isfile(path+'/data/airports.dat') == False:
		print("Downloading airports.dat")
		urllib.request.urlretrieve('https://raw.githubusercontent.com/jpatokal/openflights/master/data/airports.dat', path+'/data/airports.dat')
	if os.path.isfile(path+'/data/airlines.dat') == False:
		print("Downloading airlines.dat")
		urllib.request.urlretrieve('https://raw.githubusercontent.com/jpatokal/openflights/master/data/airlines.dat', path+'/data/airlines.dat')


	# reading csv files
	# they are converted to list to make the script faster

	airports_file = list(csv.reader(open(path+'/data/airports.dat')))
	airlines_file = list(csv.reader(open(path+'/data/airlines.dat')))
	routes_file = list(csv.reader(open(path+'/data/routes.dat')))

	#read airports' coordinates (eg. airport_location[548]=[42.123, 42.123])
	for row in airports_file:
		airport_location[row[0]]=[float(row[6]),float(row[7])]

	#read airports' routes (eg. airport_routes[548]=[123, 678, ...])
	for row in routes_file:
		if row[3] not in airport_routes:
			airport_routes[row[3]] = []
		airport_routes[row[3]].append(row[5])

	#read airlines' routes (eg. airline_routes[548]=[[123, 678], ...])
	for row in routes_file:
		if row[1] not in airline_routes:
			airline_routes[row[1]] = []
		airline_routes[row[1]].append([row[3],row[5]])

	#read airports' and airlines' names (eg. name[548]="Stansted")
	for row in airports_file:
		airport_name[row[0]]=row[1]
	for row in airlines_file:
		airline_name[row[0]]=row[1]

	#read airports' and airlines' iata codes (eg. airport_codes["STN"]=548) (may be a list)
	for row in airports_file:
		if row[4] not in airport_codes:
			airport_codes[row[4]] = []
		airport_codes[row[4]].append([row[1], row[0]])
	for row in airlines_file:
		if row[3] not in airline_codes:
			airline_codes[row[3]] = []
		airline_codes[row[3]].append([row[1], row[0]])

#-----     -----     draw routes and map     -----     -----#

def prepare_map(a): #draw map and plot title
	m.drawlsmask(land_color='green', ocean_color='aqua', resolution='c')
	plt.title(str(a))

def show_map():
	plt.show()

def print_map(code): #currently not used
	fig.savefig(code+".png", dpi=1600)

def html_map():
	return json.dumps(mpld3.fig_to_dict(fig))
	#for i in range(len(D["axes"][0]["collections"])):
	#	D["axes"][0]["collections"][i]["edgewidths"]=D["axes"][0]["collections"][i]["edgewidths"].tolist()

def point(a, interactive): #draw a point on airport a
	airport_point[a]=True
	m.scatter(\
		airport_location[a][1], airport_location[a][0],\
		5, marker='o',color='red', latlon='true', zorder=3\
	)

def line(a, b, interactive): #draw a line from airport a to airport b
	point(a, interactive)
	point(b, interactive)
	m.drawgreatcircle(\
		airport_location[a][1], airport_location[a][0],\
		airport_location[b][1], airport_location[b][0],\
		linewidth= .5, color='orange', zorder=2\
	)

#-----     -----     routes adders     -----     -----#

def draw_airport_routes(airport, interactive):

	prepare_map(airport_name[airport])

	if airport not in airport_routes:
		print("No route found for airport "+airport_name[airport]+" ("+airport+")")
		exit()

	for destination in airport_routes[airport]:
		try:
			if destination != '\\N':
				line(airport, destination, interactive)
		except:
			print(destination+' not found')

	if interactive:
		show_map()
	else:
		return html_map()
		#return print_map("p"+airport)

def draw_airline_routes(airline, interactive):

	prepare_map(airline_name[airline])

	if airline not in airline_routes:
		print("No route found for airline "+airline_name[airline]+" ("+airline+")")
		exit()

	for route in airline_routes[airline]:
		try:
			if route[0] != '\\N' and route[1] != '\\N':
				line(route[0], route[1], interactive)
		except:
			print(route+' not found')

	if interactive:
		show_map()
	else:
		return html_map()
		#return print_map("p"+airport)

#-----    ------     data soritng -----     -----#

def best_airports(num):

	if num > len(airport_routes):
		num = len(airport_routes)

	v = []
	for i in airport_routes:
		v.append([len(airport_routes[i]),i])
	return sorted(v, reverse=True)[:num]

def best_airlines(num):

	if num > len(airline_routes):
		num = len(airline_routes)

	v = []
	for i in airline_routes:
		v.append([len(airline_routes[i]),i])
	return sorted(v, reverse=True)[:num]


#-----     -----     input     -----     -----#

def show_routes(code):

	read_data()

	interactive = False
	if code[0] == "i":
		interactive = True
		code = code[1:]

	if code[0] == "p":
		return draw_airport_routes(code[1:], interactive)
	elif code[0] == "l":
		return draw_airline_routes(code[1:], interactive)
	else:
		print("ERROR")
		exit(0)

def get_list(num):

	read_data()

	dict = {}
	dict['name_id'] = {}
	dict['id_name'] = {}

	for i in best_airports(num):
		id=i[1]
		try:
			dict['id_name']["p"+id]=airport_name[id]
			dict['name_id'][airport_name[id]]="p"+id
		except:
			pass

	for i in best_airlines(num):
		id=i[1]
		try:
			dict['id_name']["l"+id]=airline_name[id]
			dict['name_id'][airline_name[id]]="l"+id
		except:
			pass

	return json.dumps(dict)

#-----     -----     command line input     -----     -----#

if __name__ == "__main__": #TODO da togliere

	read_data()
	print("DEBUG VERSION")

	if len(sys.argv) != 2:
		print("ERROR")
		exit(0)

	show_routes(sys.argv[1])
