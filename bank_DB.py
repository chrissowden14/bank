import sqlite3


conn = sqlite3.connect('bank.db')
c = conn.cursor()

def creat_table():
	#all caps for SQL commands
	c.execute('CREATE TABLE IF NOT EXISTS customer(uid INT NOT NULL, password char(10) NOT NULL, first CHAR(15) NOT NULL, last CHAR(15) NOT NULL, active INT NOT NULL, PRIMARY KEY (uid))')
	c.execute('CREATE TABLE IF NOT EXISTS admins(aid INT NOT NULL, password char(10) NOT NULL, llid INT NOT NULL, name CHAR(15) NOT NULL, PRIMARY KEY (aid))')
	c.execute('CREATE TABLE IF NOT EXISTS loans(ltid INT NOT NULL, TIM INT NOT NULL, apr float NOT NULL ,PRIMARY KEY (ltid))')
	c.execute('CREATE TABLE IF NOT EXISTS checking_account(cid INT NOT NULL, amount flaot NOT NULL, PRIMARY KEY (cid))')
	c.execute('CREATE TABLE IF NOT EXISTS saving_account(sid INT NOT NULL, amount float NOT NULL, PRIMARY KEY (sid))')
	c.execute('CREATE TABLE IF NOT EXISTS loan_account(lid INT NOT NULL, amount float NOT NULL, ltid INT NOT NULL, llid INT NOT NULL,FOREIGN KEY(llid) REFERENCES admin(llid),FOREIGN KEY(ltid) REFERENCES loans(ltid), PRIMARY KEY (lid))')
	c.execute('CREATE TABLE IF NOT EXISTS accounts(uid INT NOT NULL, cid INT, sid INT, lid INT, FOREIGN KEY(cid) REFERENCES checking_account(cid),FOREIGN KEY(sid) REFERENCES saving_account(sid),FOREIGN KEY(lid) REFERENCES loan_account(lid),FOREIGN KEY(uid) REFERENCES customer(uid), PRIMARY KEY (uid))')
	c.execute('CREATE TABLE IF NOT EXISTS user_to_admin(uid INT NOT NULL, aid  INT NOT NULL,FOREIGN KEY(uid) REFERENCES customer(uid),FOREIGN KEY(aid) REFERENCES admin(aid), PRIMARY KEY (uid)) ')
	
	
def data_entry():
	c.execute("INSERT INTO customer VALUES(11111, 'tester1', 'Chris', 'Snyder',1)")
	c.execute("INSERT INTO customer VALUES(22222, 'tester2', 'Bob', 'Silver',1)")
	c.execute("INSERT INTO customer VALUES(33333, 'tester3', 'John', 'Cena',1)")
	c.execute("INSERT INTO customer VALUES(44444, 'tester4', 'Kublai', 'Khan',1)")
	c.execute("INSERT INTO customer VALUES(55555, 'tester5', 'Alexander', 'The Great',1)")
	c.execute("INSERT INTO customer VALUES(66666, 'tester6', 'Shino', 'kia',1)")
	c.execute("INSERT INTO customer VALUES(77777, 'tester7', 'Billbob', 'Thorten',1)")
	c.execute("INSERT INTO customer VALUES(88888, 'tester8', 'Amanda ', 'Please',1)")
	c.execute("INSERT INTO customer VALUES(99999, 'tester9', 'Winston', 'Churchhill',1)")
	c.execute("INSERT INTO admins VALUES(11112, 'tester1', 11000, 'John')")
	c.execute("INSERT INTO admins VALUES(22223, 'tester2', 22000,'Kevin')")
	c.execute("INSERT INTO admins VALUES(33334, 'tester3', 33000,'Pope')")
	c.execute("INSERT INTO loans VALUES(00006, 6, 0.07)")
	c.execute("INSERT INTO loans VALUES(00012, 12, 0.06)")
	c.execute("INSERT INTO loans VALUES(00018, 18, 0.05)")
	c.execute("INSERT INTO loans VALUES(00024, 24, 0.04)")
	c.execute("INSERT INTO loans VALUES(00030, 30, 0.03)")
	c.execute("INSERT INTO checking_account VALUES(01111, 6000)")
	c.execute("INSERT INTO checking_account VALUES(02222, 7000)")
	c.execute("INSERT INTO checking_account VALUES(03333, 900000000)")
	c.execute("INSERT INTO checking_account VALUES(04444, 50000)")
	c.execute("INSERT INTO checking_account VALUES(05555, 45800000)")
	c.execute("INSERT INTO checking_account VALUES(06666, 1000)")
	c.execute("INSERT INTO checking_account VALUES(07777, 69521)")
	c.execute("INSERT INTO checking_account VALUES(08888, 55568)")
	c.execute("INSERT INTO checking_account VALUES(09999, 454547)")
	c.execute("INSERT INTO loan_account VALUES(00111, 3000, 00006, 11000)")
	c.execute("INSERT INTO loan_account VALUES(00222, 300, 00006, 11000)")
	c.execute("INSERT INTO loan_account VALUES(00333, 50, 00012, 11000)")
	c.execute("INSERT INTO loan_account VALUES(00444, 6000, 00012 ,22000)")
	c.execute("INSERT INTO loan_account VALUES(00555, 5000, 00018 ,22000)")
	c.execute("INSERT INTO loan_account VALUES(00666, 9000, 00018 ,22000)")
	c.execute("INSERT INTO loan_account VALUES(00777, 200, 00024 ,33000)")
	c.execute("INSERT INTO loan_account VALUES(00888, 645, 00024 ,33000)")
	c.execute("INSERT INTO loan_account VALUES(00999, 1000, 00030 ,33000)")
	c.execute("INSERT INTO saving_account VALUES(00011, 60001)")
	c.execute("INSERT INTO saving_account VALUES(00022, 70001)")
	c.execute("INSERT INTO saving_account VALUES(00033, 9000000001)")
	c.execute("INSERT INTO saving_account VALUES(00044, 500001)")
	c.execute("INSERT INTO saving_account VALUES(00055, 458000001)")
	c.execute("INSERT INTO saving_account VALUES(00066, 10001)")
	c.execute("INSERT INTO saving_account VALUES(00077, 695211)")
	c.execute("INSERT INTO saving_account VALUES(00088, 555681)")
	c.execute("INSERT INTO saving_account VALUES(00099, 4545471)")
	c.execute("INSERT INTO accounts VALUES(11111, 01111, 00011, 00111)")
	c.execute("INSERT INTO accounts VALUES(22222, 02222, 00022, 00222)")
	c.execute("INSERT INTO accounts VALUES(33333, 03333, 00033, 00333)")
	c.execute("INSERT INTO accounts VALUES(44444, 04444, 00044, 00444)")
	c.execute("INSERT INTO accounts VALUES(55555, 05555, 00055, 00555)")
	c.execute("INSERT INTO accounts VALUES(66666, 06666, 00066, 00666)")
	c.execute("INSERT INTO accounts VALUES(77777, 07777, 00077, 00777)")
	c.execute("INSERT INTO accounts VALUES(88888, 08888, 00088, 00888)")
	c.execute("INSERT INTO accounts VALUES(99999, 08888, 00099, 00999)")
	c.execute("INSERT INTO user_to_admin VALUES(11111, 11112)")
	c.execute("INSERT INTO user_to_admin VALUES(22222, 11112)")
	c.execute("INSERT INTO user_to_admin VALUES(33333, 11112)")
	c.execute("INSERT INTO user_to_admin VALUES(44444, 22223)")
	c.execute("INSERT INTO user_to_admin VALUES(55555, 22223)")
	c.execute("INSERT INTO user_to_admin VALUES(66666, 22223)")
	c.execute("INSERT INTO user_to_admin VALUES(77777, 33334)")
	c.execute("INSERT INTO user_to_admin VALUES(88888, 33334)")
	c.execute("INSERT INTO user_to_admin VALUES(99999, 33334)")

	
	
	
	

	
	conn.commit()
	
	c.close()
	conn.close()
	
	
creat_table()
data_entry()
