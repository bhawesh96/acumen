import csv
import MySQLdb as sql

flag=0
count =0
# round1 = {}
# db  = sql.connect('139.59.17.132','user2','passw','acumen')
db  = sql.connect('103.50.162.66','kodamr13_inquiz','oEO8CI1![0D=','kodamr13_inquizitive')

c = db.cursor()

query = " INSERT INTO questions VALUES "
with open('Temp_questions2.tsv') as file:
	flag =1

	# readr = csv.reader(file)
	# print readr
	for r in file:
		# print r

		r = r.strip("\r|\n").split("\t")
		# print r
		r[2] = r[2].replace("'","\\'")
		# print r
		if (r[0] == 'question_id'):
			continue
		
		# print r
		# if(r[0] == "ROUND6"):
			# continue;
		if(flag==1):
			if(r[0]=='120'):
				flag=0
			count +=1
			# r[0] == ques_id			
			# r[1] == image if any
			# r[2] == ques 			
			# r[3] == option1			
			# r[4] == option2		
			# r[5] == option3
			# r[6] == option4
			# r[7] == answer
			# r[8] == difficulty
			if(r[1] == ''):
				r[1] = 'False'
			# if(r[3] == 'FALSE' or r[3] == ''):
				# r[3] = 'False'


			##handling quotes if any##
			

			# questions table format = `question_id` VARCHAR(20),  `question` VARCHAR(400), `option1` VARCHAR(100),
  							# `option2` VARCHAR(100), `option3` VARCHAR(100), `option4` VARCHAR(100),
  							# `question_image` varchar(200), `answer` INT, `difficulty` INT,
  			val = "('" + r[0] +"','" + r[2] +"','"+ r[3] +"','"+ r[4] +"','"+ r[5] +"','"+ r[6] +"','"+ r[1] +"',"+ r[7] +","+ r[8] + ")"
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
				if(e[0]!=1062):
					print(query + val + ";")
				db.rollback()
				pass
		# if(count == 60):
			# flag=0
# disconnect from server
db.close()