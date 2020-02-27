import json

counter = 0
with open("complaints2.json", "r") as file:	
	complaintsDict = json.loads(file.read())
	for commenter in complaintsDict:
		counter += 1
		#print(commenter)

print(counter)