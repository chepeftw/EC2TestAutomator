# mongo_hello_world.py
# Author: Bruce Elgort
# Date: March 18, 2014
# Purpose: To demonstrate how to use Python to
# 1) Connect to a MongoDB document collection
# 2) Insert a document
# 3) Display all of the documents in a collection</code>
 
from pymongo import MongoClient
 
# connect to the MongoDB on MongoLab
# to learn more about MongoLab visit http://www.mongolab.com
# replace the "" in the line below with your MongoLab connection string
# you can also use a local MongoDB instance
connection = MongoClient('54.186.74.114', 27017)
connection.admin.authenticate('chepeftw', 'GJadPPCoxofZhK3RnjvLWFXtUEwoKLYTDJTThYAJouMsFvdZZRf7xTgdRBAsCxNg', mechanism='SCRAM-SHA-1')
 
# connect to the students database and the ctec121 collection
db = connection.students.test
 
# create a dictionary to hold student documents
 
# create dictionary
student_record = {}
 
# set flag variable
flag = True
 
# loop for data input
while (flag):
   # ask for input
   # student_name,student_grade = input("Enter student name and grade: ").split(',')
   student_name = 'chepe'
   student_grade = 90
   # place values in dictionary
   student_record = {'name':student_name,'grade':student_grade}
   # insert the record
   db.insert(student_record)
   flag = False
 
# find all documents
results = db.find()
 
print()
print('+-+-+-+-+-+-+-+-+-+-+-+-+-+-')
 
# display documents from collection
for record in results:
	# print out the document
	print(record['name'] + ',',record['grade'])
 
print()
 
# close the connection to MongoDB
connection.close()