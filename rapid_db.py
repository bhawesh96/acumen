import csv
import MySQLdb as sql

flag=0
count =0
# round1 = {}
# db  = sql.connect('139.59.17.132','user2','passw','acumen')
db  = sql.connect('103.50.162.66','kodamr13_inquiz','rtg8055','kodamr13_inquizitive')

c = db.cursor()

query = " INSERT INTO rapid VALUES "
with open('rapid_questions.tsv') as file:
	flag =1
	for r in file:
		# print r

		r = r.strip("\r|\n").split("\t")
		# print r

		##handling quotes if any##
		r[2] = r[2].replace("\'","\'")
		r[2] = r[2].replace("\"","\'")
		# print r
		

		if (r[0] == 'lvl'):
			continue
		ques_id = r[0]+"_" + r[1]
		if(flag==1):
			if(r[0]=='120'):
				flag=0
			count +=1
			# r[0] == lvl			
			# r[1] == qno
			# r[2] == ques 
			# r[3] == option1			
			# r[4] == option2		
			# r[5] == option3
			# r[6] == option4
			# r[7] == answer
			if(r[1] == ''):
				continue
			# questions table format = `question_id` VARCHAR(20),  `question` VARCHAR(400),  `option1` VARCHAR(100),  `option2` VARCHAR(100),  `option3` VARCHAR(100),  `option4` VARCHAR(100),  `answer` INT,  PRIMARY KEY (`question_id`));


			val = "('" + ques_id +"','" + r[2] +"','"+ r[3] +"','"+ r[4] +"','"+ r[5] +"','"+ r[6] +"',"+ r[7] + ")"
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
			# break
		# if(count == 60):
			# flag=0
# disconnect from server
db.close()