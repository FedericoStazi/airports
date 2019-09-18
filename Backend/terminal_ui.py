import show_routes as sr

def multiple_choice(question, options):

	if len(options) == 1:
		return options[0][1]

	print(question)

	i=0
	for opt in options:
		print("["+str(i+1)+"] "+opt[0])
		i=i+1

	try:
		res = int(input())-1
	except:
		print("Please enter a valid answer")
		return multiple_choice(question, options)

	if 0 <= res and res < len(options):
		return options[res][1]
	else:
		print("Please enter a valid answer")
		return multiple_choice(question, options)

def call(mode, code):

	print("call "+mode+" "+code)

	if mode == "p":
		name = sr.airport_name[code]
	elif mode == "l":
		name = sr.airline_name[code]

	print("Drawing routes for: "+name)
	sr.show_routes(interactive+mode+code)

print("GENERAL INFOS")
interactive = multiple_choice("Interactive map or print an image?", [["interactive", "i"],["print the image", ""]])
mode = multiple_choice("Airport or airline?", [["airport","p"],["airline","l"]])

if mode == "p":

	print("Write the IATA code of the airport:")
	iata=input().upper()

	if len(sr.airport_codes[iata]):
		call(mode, multiple_choice("Choose the airport: ", sr.airport_codes[iata]))
	else:
		print(iata+" code not found")

elif mode == "l":

	print("Write the IATA code of the airline:")
	iata=input().upper()

	if len(sr.airline_codes[iata]):
		call(mode, multiple_choice("Choose the airline: ", sr.airline_codes[iata]))
	else:
		print(iata+" code not found")
