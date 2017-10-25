import time
import datetime
import FileStore


class ReturnCustomer:
    type = "Normal Account"

    def __init__(self):
        self.FS = FileStore.FileStore()
        self.username = input('Please enter your User Name:\n')
        self.index = self.FS.cusnames.index(self.username)
        self.userPassword = self.FS.cusspaswords[self.index]
        self.balance = float(self.FS.cusbalance[self.index])
        self.userFunc()

    # this checks for the returning customers info
    def oldcuscheck(self):

        while self.username not in self.FS.cusnames:
            self.username = input("What is your user name.\n")
            if self.username in self.FS.cusnames:
                self.userPassword = self.FS.cusspaswords[self.FS.cusnames.index(self.username)]
                self.balance = float(self.FS.cusbalance[self.FS.cusnames.index(self.username)])
                self.userFunc()
            else:
                print("Sorry %s, You may have misspelled your name or it was not in the database" % self.username)
                retype = input("Would you like to retype your name again (y/n)")

                if retype.lower() == 'y':
                    self.oldcuscheck()
                else:
                    print("Bye, thank you for using Dorks Bank.")
                    exit()

    def userFunc(self):
        print("\n\nPress any option below.")
        ans = input(":Check Balance, Press B.\n:Deposit cash, Press D.\n:Withdraw Cash, Press W.\n"
                    ":Exit Service, Press E\n:: ").lower()
        if ans == 'b':
            self.passcheck()
            self.checkbalance()
        elif ans == 'd':
            self.passcheck()
            self.depositCash()
        elif ans == 'w':
            self.passcheck()
            self.withdrawCash()
        elif ans == 'e':
            print(" Thank you for using Dork Bank")
            time.sleep(1)
            print("Goodbye %s" % self.username)
            exit()
        else:
            print("Wrong entry, try again" % self.userFunc())

    def checkbalance(self):
        date = datetime.date.today().strftime('%d-%B-%Y')
        self.working()
        print("Your account balance as of", date, 'is', self.balance, '\n')
        self.transaction()

    def withdrawCash(self):
        amount = float(input("Please the the amount that you wish to withdraw\n:: "))
        self.balance -= amount
        self.working()
        print("Your new balance is %.2f" % self.balance)
        print("::\n")
        self.balupdate()
        self.transaction()

    def depositCash(self):
        amount = float(input("Please enter amount deposited\n:: "))
        self.balance += amount
        self.working()
        self.balupdate()
        print("Your new account balance is %.2f" % self.balance)
        print("::\n")
        self.transaction()

    def transaction(self):
        ans = input("If you want another Transaction press (y/n)\n:: ")
        if ans == "y":
            self.userFunc()
        elif ans == "n":
            print("Thank you for using Dorks Bank. Goodbye.\n")
            time.sleep(1)

    # this function update the account balance after withdraw or deposit
    def balupdate(self):
        self.FS.cusbalance[self.index] = self.balance
        self.FS.filewrite(self.FS.cusbalance)

    def working(self):
        print("\nWorking")
        time.sleep(1)
        print("......")
        time.sleep(1)
        print("....\n")
        time.sleep(1)

    def passcheck(self):

        # prompts user for password with every transaction
        a = 3
        while a > 0:
            ans = input("Enter Password to continue Transaction\n")
            if ans == self.userPassword:
                return True

            else:
                print("Wrong Password")
                a -= 1
                print("%d more attempt remaining" % a)

        print("Account is frozen. Please contact a System Administrator to unlock it.")
        time.sleep(1)
        print("......")
        time.sleep(1)
        print("....")
        time.sleep(1)
        print('Goodbye.')
