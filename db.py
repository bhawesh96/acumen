import csv
import MySQLdb as sql

flag=0
count =0
# round1 = {}
db  = sql.connect('139.59.17.132','user2','passw','acumen')
c = db.cursor()

query = " INSERT INTO questions2 VALUES "
with open('acumen.csv') as file:
	flag =1

	readr = csv.reader(file)
	for r in readr:
		if (r[0] == 'id'):
			continue
		# print r
		# if(r[0] == "ROUND6"):
			# continue;
		if(flag==1):
			if(r[0]=='60'):
				flag=0
			count +=1
			# r[0] == ques_id			
			# r[1] == story in quotes			
			# r[2] == ques 			
			# r[3] == ques_img			
			# r[4] ==ans			
			# r[5] == hint			
			# r[6] == op4
			if(r[5] == ''):
				r[5] = 'False'
			if(r[3] == 'FALSE'):
				r[3] = 'False'
				# r[10] = 'null'
			val = "('" + r[0] +"','" + r[1] +"','" + r[2] +"','"+ r[3] +"','"+ r[4] +"','"+ r[5] + "')"
			# print(val)
			try:
				print(c.execute(query + val + ";"))
				# print(query + val + ";")
				# c.execute(sql)
				# Commit your changes in the database
				db.commit()

			except Exception as e:
				# Rollback in case there is any error
				print(e)
				db.rollback()
				pass
		if(count == 60):
			flag=0
# disconnect from server
db.close()