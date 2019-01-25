import mysql.connector
import csv
from sklearn import tree
cnx = mysql.connector.connect(user='root', password='mesbah',host='127.0.0.1',database='data')
cursor = cnx.cursor()
query = 'SELECT * FROM houses;'
cursor.execute(query)
DATA = list(cursor)
DATA = list(map(lambda x: list(x),DATA))
def subset(name,list):
	control = 0
	i = 0
	while i < len(list):
		if list[i] == name: control = 1
		i += 1
	if control == 1: return True
	else: return False
x = []
y = []
location = []
#print(len(DATA))
for i in range(len(DATA)):
    if subset(DATA[i][3],location) == False: location.append(DATA[i][3])
#for i in location: print(i)
def loc_to_dig(string):
	if subset(string,location):
		for i in range(len(location)):
			if string == location[i]: return i
	else: return False

for i in range(len(DATA)): DATA[i][3] = loc_to_dig(DATA[i][3])
for i in range(len(DATA)):
    x.append(DATA[i][1:4])
    y.append(DATA[i][4])
#for i in x:print(i)
#for i in y:print(i)
clf = tree.DecisionTreeClassifier()
clf = clf.fit(x, y)
print(len(DATA))
while True:
	area = input('please enter area of the flat: ')
	if area.isdigit():
		area = int(area)
		break 
	else: print("%s is not an integer"%area)
while True:
	beds = input('Enter the number of beds: ')
	if beds.isdigit():
		beds = int(beds)
		break
	else: print("%s is not an integer"%area)
print("available locations:")
for i in location: print(i)
while True:
	loc = input('Enter the location: ')
	if subset(loc,location):
		loc = loc_to_dig(loc)	
		break
	else: print('%s is not available!'%loc)
new_data = [[area, beds, loc]]
answer = clf.predict(new_data)
print("Estimated price is %i T"%answer[0])



