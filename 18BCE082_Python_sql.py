#Connector for connecting MySQL and Python
import mysql.connector

#Schema of table
#Attribute_name: [field length, datatype,mandatory, Key column]
schema = {
			'Customer_Name':[255,'VARCHAR','Y','Y']
			,'Customer_ID':[18,'VARCHAR','Y','N']
			,'Customer_Open_Date':[8,'DATE','Y','N']
			,'Last_Consulted_Date':[8,'DATE','N','N']
			,'Vaccination_Type':[5,'CHAR','N','N']
			,'Doctor_Consulted':[255,'CHAR','N','N']
			,'State':[5,'CHAR','N','N']
			,'Country':[5,'CHAR','N','N']
			,'Post_Code':[5,'INT','N','N']
			,'Date_of_Birth':[8,'DATE','N','N']
			,'Active_Customer':[1,'CHAR','N','N']
		}



# Query for table creation
def create_table(split_data):
	country = split_data[8] # Represents Country name

	query="Create table "+ country + "("

	for col in schema:
		query = query + col + " " + schema[col][1]

		#If its a date attribute, then no need to specify length
		if schema[col][1] != "DATE":
			query = query + "("+ str(schema[col][0]) +") "

		if(schema[col][2] == 'Y'):
			query = query + " NOT NULL"

		if (schema[col][3] == 'Y'):
			query = query + " PRIMARY KEY "

		if(col != "Active_Customer"): # If its last column, then dont add ','
			query = query + ", "

	return query + ")"
	



#Open the file in read mode
f = open("Incubyte_data.txt","r")

#Create database connection
mydb = mysql.connector.connect(host="localhost", user="ayush", passwd="Ayushjain1290#", database="ayush")
mycursor = mydb.cursor() #Gives a pointer to database

#Set for storing the tablenames that are already present
s=set()

#Read file line by line
for line in f:
	trimmed_line = line[1:len(line)-1] # Remove initial '|' and new line character
	splitted_data = trimmed_line.split('|') # Split the line by using '|' as delimeter


	#Iterate through each data, and if its a number than store in the form of int
	for i in range(len(splitted_data)):
		if (splitted_data[i].isnumeric()):
			splitted_data[i] = int(splitted_data[i])


	#Convert list into tuple for insert query
	splitted_data=tuple(splitted_data)


	#Ignore the line, if its header or trailer
	if(splitted_data[0] == 'H' or splitted_data[0] == 'T' ):
		continue
	elif (splitted_data[0] == 'D'):
		if(splitted_data[8] not in s):  # Check if table already exists
			s.add(splitted_data[8])
			mycursor.execute(create_table(splitted_data)) # Execute create table


# Commit data in database and deallocate cursor
mydb.commit()
mycursor.close()
mydb.close()


#Close the file		
f.close()


