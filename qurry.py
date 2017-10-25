import sqlite3

conn = sqlite3.connect('bank.db')
c = conn.cursor()


def qurry1():
    c.execute('select customer.first, admins.name from customer natural join user_to_admin  join admins where user_to_admin.aid=admins.aid')
    for row in c.fetchall():
        print(row)


def qurry2():
    c.execute('select customer.first, checking_account.amount from customer natural join accounts natural join checking_account')
    for row in c.fetchall():
        print(row)

def qurry3():
    c.execute('select admins.name, apr, TIM from admins join loan_account natural join loans where admins.llid=loan_account.llid')
    for row in c.fetchall():
        print(row)
def qurry4():
    c.execute('select amount+amount * TIM * APR as total_cost  from loan_account join loans where loan_account.ltid= loans.ltid')
    for row in c.fetchall():
        print(row)
def qurry5():
    c.execute('select amount + amount * 12* .02 as estimated_svaings_projection from saving_account')
    for row in c.fetchall():
        print(row)

qurry1()
print(" ")
qurry2()
print(" ")
qurry3()
print(" ")
qurry4()
print(" ")
qurry5()
print(" ")
c.close()
conn.close()
