import time
import datetime
import FileStore


class NewCustomer:
    type = "Normal Account"

    def __init__(self):
        self.FS = FileStore.FileStore()
        self.username = ''
        self.pin = ''
        self.balance = 0.0
        self.cusAccountCheck()

        # creates new user

    def cusAccountCheck(self):
        namecheck = False
        lengthcheck = False

        while not (namecheck and lengthcheck):
            self.username = input("Please type in your name for the new account:\n")

            if self.username not in self.FS.cusnames:
                namecheck = True
                if len(self.username) > 3:
                    lengthcheck = True
                    self.FS.cusnames.append(self.username)
                    self.FS.filewrite(self.FS.cusnames)
                else:
                    lengthcheck = False
                    print("That name is too short. Try again.\n")
            else:
                namecheck = False
                print("That name is already in use. Try again.\n")

        while len(self.pin) < 4:
            self.pin = input("Please assign a password to this account, password should be at least 5 characters:\n")
            if len(self.pin) > 4:
                print("Your password is now saved.")
                print("Keep your password safe and do not disclose this information to anyone.")
                self.FS.cusspaswords.append(self.pin)
                self.FS.filewrite(self.FS.cusspaswords)
                break
            print("Sorry, password is too short. Try again.\n")

        while self.balance <= 100.0:
            self.balance = float(input('Enter your Opening Balance (Must be 100.00 or more):\n'))
            if self.balance >= 100.0:
                self.FS.cusbalance.append(self.balance)
                self.FS.filewrite(self.FS.cusbalance)
                break
            print('Opening Balance not valid. Try again.\n')

        self.working()
        date = datetime.date.today().strftime('%d-%B-%Y')
        print("Thank you %s, your account was activated" % self.username, "with an opening balance of %s"
              % self.balance, "on %s.\n" % date)

    def working(self):
        print("\nWorking")
        time.sleep(1)
        print("......")
        time.sleep(1)
        print("....\n")
        time.sleep(1)
