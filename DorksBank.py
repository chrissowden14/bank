import tkinter as tk
import sqlite3
import random


class Splash(tk.Frame):
    """
    The Splash window that will give the options for login as Admin, User, or to create
     an account.
    """

    def __init__(self, master):
        """ Initializes the opening display which allows the user to select which form
        of log in is required or to create a new account.

        :param master The master frame for the GUI"""
        # Connect to the Database.
        self.conn = sqlite3.connect('bank.db')
        self.c = self.conn.cursor()
        tk.Frame.__init__(self, master)
        self.master.title('Dork\'s Bank')
        self.master.config(menu=tk.Menu(self.master))

        # Configure GUI row and column layouts
        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_rowconfigure(4, weight=1)
        self.master.grid_columnconfigure(0, weight=1)
        self.master.grid_columnconfigure(4, weight=1)

        # Create buttons for User login, Admin login, and exit
        user_button = tk.Button(self.master, text='User Login', command=self.on_user,
                                width=25)
        user_button.grid(row=1, column=1, pady=5)

        admin_button = tk.Button(self.master, text='Admin Login', command=self.on_admin, width=25)
        admin_button.grid(row=2, column=1, pady=5)

        exit_button = tk.Button(self.master, text='Exit', command=quit, width=10)
        exit_button.grid(row=3, column=1, pady=5)

        # Create link for new users to create an account
        create_account_link = tk.Label(self.master, text='Want an Account? Click here to create one!', fg='blue',
                                       cursor='hand2')
        create_account_link.bind("<Button-1>", self.on_link)
        create_account_link.grid(row=4, column=1)

        # Set minimum window size
        self.master.minsize(800, 600)
        center(self.master.winfo_toplevel())

    def on_user(self):
        """ When the user selects to log into a user account, the widgets are destroyed
        and the user log in is displayed."""
        # Destroy current widgets
        window_cleaner(self.master)

        # Go to User Login
        LoginUser(self.master)

    def on_admin(self):
        """ When the user selects to log into an admin account, the widgets are destroyed
        and the admin log in is displayed."""
        # Destroy current widgets
        window_cleaner(self.master)

        # Go to Admin Login
        LoginAdmin(self.master)

    def on_link(self, event):
        """ When the user selects to create a new account, the widgets are destroyed and
        the create account page is displayed."""
        # Destroy current widgets
        window_cleaner(self.master)

        # Go to New user account creation
        CreateUser(self.master)


class LoginUser(tk.Frame):
    """
    The Login window for users.
    """

    def __init__(self, master):
        """Creates a link to the database and then allows the user to log into their
        account.

        :param master The master frame for the GUI."""
        # Link to the database
        self.conn = sqlite3.connect('bank.db')
        self.c = self.conn.cursor()

        # Create the Tkinter master frame
        tk.Frame.__init__(self, master)
        self.master.title('Dork\'s Bank - User Login')
        self.master.config(menu=tk.Menu(self.master))
        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_rowconfigure(4, weight=1)
        self.master.grid_columnconfigure(0, weight=1)
        self.master.grid_columnconfigure(4, weight=1)

        # Create User Name field
        user_name_l = tk.Label(self.master, text="User Name:")
        user_name_l.grid(row=1, column=1, sticky='E', pady=5)

        # Receive and display user entry
        self.user_name_text = tk.StringVar()
        user_name_entry = tk.Entry(self.master, textvariable=self.user_name_text,
                                   width=25)
        user_name_entry.grid(row=1, column=2, columnspan=2, pady=5)

        # Create User Password field
        password_l = tk.Label(self.master, text="Password:")
        password_l.grid(row=2, column=1, sticky='E', pady=5)

        # Receive and display user password
        self.password_text = tk.StringVar()
        password_entry = tk.Entry(self.master, textvariable=self.password_text,
                                  show="*", width=25)
        password_entry.grid(row=2, column=2, columnspan=2, pady=5)

        # Create Submit button, calls on_submit
        submit_button = tk.Button(self.master, text='Submit', command=self.on_submit,
                                  width=10)
        submit_button.grid(row=3, column=1, padx=3)

        # Create Exit button, calls quit
        exit_button = tk.Button(self.master, text='Exit', command=quit, width=10)
        exit_button.grid(row=3, column=2, padx=3)

        # Create go back button, calls back_to_splash
        back = tk.Button(self.master, text='Back', command=self.back_to_splash,
                         width=10)
        back.grid(row=3, column=3, padx=3)

        # Set frame layout
        self.master.minsize(800, 600)
        center(self.master.winfo_toplevel())

    def on_submit(self):
        """Checks to ensure the user name and password are valid then retreives the user
        data from the database."""
        # Loop until the correct information is entered or an error is thrown
        while True:
            try:
                # Get user name and password
                user_name = self.user_name_text.get()
                user_password = self.password_text.get()

                # Attempts to access user name and password from the data base
                self.c.execute(
                    "select * from customer where uid = " + user_name + " and password "
                                                                        "= '" + user_password + "'")
                temp = self.c.fetchall()

                # Checks if the entry exits in the data base and the password is correct
                if len(temp) == 1:
                    # Entrey exists and password is correct.  Destroy current widgets and go to the Return User Menu
                    window_cleaner(self.master)
                    ReturnUserMenu(self.master, user_name)
                    break
                else:
                    # Entry doesn't exist or password is incorrect.  Pop up error message and have user re-enter
                    # their information
                    DialogBoxes.username_password_error()
                    break
            except sqlite3.OperationalError:
                DialogBoxes.system_breach_warning()
                break

    def back_to_splash(self):
        """ Destroys current widgets and returns to the main page."""
        # Destroy current widgets
        window_cleaner(self.master)

        # Go back to the main page
        Splash(self.master)


class LoginAdmin(tk.Frame):
    """
    The Login window for Admins.
    """

    def __init__(self, master):
        """Establishes a connection to the database and then verifies the login in
        information.

        :param master The master frame for the GUI."""
        # Establish connection with the data base
        self.conn = sqlite3.connect('bank.db')
        self.c = self.conn.cursor()

        # Create the main window frame
        tk.Frame.__init__(self, master)
        self.master.title('Dork\'s Bank - Admin Login')
        self.master.config(menu=tk.Menu(self.master))
        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_rowconfigure(4, weight=1)
        self.master.grid_columnconfigure(0, weight=1)
        self.master.grid_columnconfigure(4, weight=1)

        # Create user name field
        user_name_l = tk.Label(self.master, text="User Name:")
        user_name_l.grid(row=1, column=1, sticky='E', pady=5)

        # Recieve and display users name entry
        self.user_name_text = tk.StringVar()
        user_name_entry = tk.Entry(self.master, textvariable=self.user_name_text, width=25)
        user_name_entry.grid(row=1, column=2, columnspan=2, pady=5)

        # Create user password field
        password_l = tk.Label(self.master, text="Password:")
        password_l.grid(row=2, column=1, sticky='E', pady=5)

        # Recieve and display user password
        self.password_text = tk.StringVar()
        password_entry = tk.Entry(self.master, textvariable=self.password_text, show="*", width=25)
        password_entry.grid(row=2, column=2, columnspan=2, pady=5)

        # Create submit button, calls on_submit
        submit_button = tk.Button(self.master, text='Submit', command=self.on_submit, width=10)
        submit_button.grid(row=3, column=1, padx=3)

        # Create exit button, calls quit
        exit_button = tk.Button(self.master, text='Exit', command=quit, width=10)
        exit_button.grid(row=3, column=2, padx=3)

        # Create Back button, calls back_to_splash
        back = tk.Button(self.master, text='Back', command=self.back_to_splash, width=10)
        back.grid(row=3, column=3, padx=3)

        # Set window layout
        self.master.minsize(800, 600)
        center(self.master.winfo_toplevel())

    def on_submit(self):
        """Verifies admin information then moves to the Administrators page."""
        while True:
            # Loop until the correct information is entered or an error is thrown
            try:
                # Gets administrators user name
                username = self.user_name_text.get()

                # gets administrators user password
                userpassword = self.password_text.get()

                # Attempts to access administrator in the data base
                self.c.execute(
                    "select * from admins where aid = " + username + " and password = '" + userpassword + "'")
                temp = self.c.fetchall()

                # Check to see if the data exists in the data base and the password is correct
                if len(temp) == 1:
                    # Entry exists and password is correct.  Destroy current widgets and go to Admin User menu.
                    window_cleaner(self.master)
                    AdminUserMenu(self.master, username)
                    break
                else:
                    # Entry doesn't exists or password is incorrect.  Pop up error messege and have user re enter their
                    # log in information.
                    DialogBoxes.username_password_error()
                    break
            except sqlite3.OperationalError:
                DialogBoxes.system_breach_warning()
                break

    def back_to_splash(self):
        """Sends the display back to the main menu."""
        # Destory current widgets
        window_cleaner(self.master)
        # Go to the main menu
        Splash(self.master)


class CreateUser(tk.Frame):
    """
    The Create User window that will show all information needed to create an account.
    """

    def __init__(self, master):
        """Creates the connection to the database then displays the create user window.

        :param master The Master frame for the GUI."""
        # Connects to the database.
        self.conn = sqlite3.connect('bank.db')
        self.c = self.conn.cursor()

        # Create the Tkinter frame
        tk.Frame.__init__(self, master)
        self.master.title('Dork\'s Bank - Create Account')
        self.master.config(menu=tk.Menu(self.master))

        # Configure the rows and columns
        for s in range(6):
            self.master.grid_rowconfigure(s, weight=1)
            self.master.grid_columnconfigure(s, weight=1)

        # Create the user name field
        first_name_l = tk.Label(self.master, text='First Name:')
        first_name_l.grid(row=0, column=0, sticky='E')

        # Receive and display the users first name
        self.first_name_text = tk.StringVar()
        first_name_entry = tk.Entry(self.master, textvariable=self.first_name_text)
        first_name_entry.grid(row=0, column=1)

        # Create the users last name field
        last_name_l = tk.Label(self.master, text='Last Name:')
        last_name_l.grid(row=0, column=2, sticky='E')

        # Receive and display the users last name
        self.last_name_text = tk.StringVar()
        last_name_entry = tk.Entry(self.master, textvariable=self.last_name_text)
        last_name_entry.grid(row=0, column=3)

        # Create the user password field
        password_l = tk.Label(self.master, text='Password:')
        password_l.grid(row=1, column=0, sticky='E')

        # Receive and display the users password (represented as a '*')
        self.password_text = tk.StringVar()
        password_entry = tk.Entry(self.master, textvariable=self.password_text, show="*")
        password_entry.grid(row=1, column=1)

        # Create the user password check field
        password_check_l = tk.Label(self.master, text='Re-Enter Password:')
        password_check_l.grid(row=2, column=0, sticky='E')

        # Receive and display the users password again and check that it is the same as the previously entered password.
        self.password_check_text = tk.StringVar()
        password_check_entry = tk.Entry(self.master, textvariable=self.password_check_text,
                                        show="*")
        password_check_entry.grid(row=2, column=1)

        # Create the opening balance field
        opening_balance_l = tk.Label(self.master, text='Opening Balance:')
        opening_balance_l.grid(row=6, column=0, sticky='E')

        # Receive and display the users opening balance
        self.opening_balance_text = tk.IntVar()
        opening_balance_entry = tk.Entry(self.master, textvariable=self.opening_balance_text)
        opening_balance_entry.grid(row=6, column=1)

        # Create a submit button.  Calls comm
        submit = tk.Button(self.master, text='Submit', command=self.comm, width=10)
        submit.grid(row=6, column=5, sticky='SE', padx=4, pady=4)

        # Create a back button.  Calls back_to_splash
        back = tk.Button(self.master, text='Cancel', command=self.back_to_splash, width=10)
        back.grid(row=7, column=5, sticky='SE', padx=5, pady=5)

        # Set frame options
        self.master.minsize(800, 600)
        center(self.master.winfo_toplevel())

    def comm(self):
        """Checks the information and if the information is valid stores it to the
        database."""
        name_check = False
        length_check = False
        t = True

        p = 0
        # Create User id
        while p != 1:
            rando = random.randint(1, 99999)
            self.c.execute("select * from customer where uid = " + str(rando))
            temp = self.c.fetchall()
            # Checks if the user id is already in use
            if len(temp) == 1:
                p = 0
            elif len(temp) == 0:
                p = 1

        # Set user name
        while not (name_check and length_check):
            username = self.first_name_text.get()
            username2 = self.last_name_text.get()

            name_check = True
            if len(username) > 3 and len(username2) > 3:
                length_check = True

            else:
                # make into a pop up falg2 t=F
                t = False
                DialogBoxes.name_length_error()
                break

        # Set user password
        pin = ""
        while len(pin) < 4:
            if self.password_text.get() == self.password_check_text.get():
                pin = self.password_text.get()
            if len(pin) > 4:
                # make into a pop up flag1 t=T
                break
            # make into a pop up falg2 t=F
            t = False
            DialogBoxes.password_length_error()
            break



        balance = float(0)
        while True:
            try:
                while balance < float(100):
                    balance = float(self.opening_balance_text.get())
                    if balance >= 100.0:
                        break
                    # make into a pop up flag 3 t=F
                    t = False
                    DialogBoxes.opening_balance_error()
                    break
                break
            except tk.TclError:
                t = False
                DialogBoxes.input_error()
                break
        while True:
            try:
                if t:
                    self.c.execute("INSERT INTO customer VALUES(" + str(
                        rando) + ", '" + pin + "', '" + username + "', '" + username2 + "',1)")
                break
            except sqlite3.OperationalError:
                self.conn.rollback()
                # make into a pop up falg1 t=F
                DialogBoxes.system_breach_warning()
                break

        p = 0
        while p != 1:
            rando2 = random.randint(1, 99999)

            self.c.execute("select * from checking_account where cid = " + str(rando2))
            temp = self.c.fetchall()
            if len(temp) == 1:
                p = 0
            elif len(temp) == 0:
                p = 1
        p = 0
        while p != 1:
            rando3 = random.randint(1, 99999)
            self.c.execute("select * from saving_account where sid = " + str(rando3))
            temp = self.c.fetchall()
            if len(temp) == 1:
                p = 0
            elif len(temp) == 0:
                p = 1

        # Create new entry in the data base
        if t:
            self.c.execute("DROP TRIGGER add_and_link_accounts")
            self.c.execute("DROP TRIGGER link_accounts")
            self.c.execute(
                '''CREATE TRIGGER add_and_link_accounts AFTER INSERT ON checking_account 
                BEGIN INSERT INTO saving_account (sid, amount) VALUES (''' + str(
                    rando3) + ''', 0);  END;''')

            self.c.execute(
                '''CREATE TRIGGER link_accounts AFTER INSERT ON checking_account BEGIN 
                INSERT INTO accounts (uid, cid,sid,lid) VALUES (''' + str(
                    rando) + ''',''' + str(rando2) + ''',''' + str(rando3) + ''',NULL);  END;''')

        # Sets users opening balance
        

        while True:
            try:
                if t:
                    self.c.execute("INSERT INTO checking_account VALUES(" + str(rando2)
                                   + ", " + str(balance) + ")")
                break
            except sqlite3.OperationalError:
                self.conn.rollback()
                DialogBoxes.system_breach_warning()
                break

        # Assigns administrator to user
        
        self.c.execute("SELECT aid FROM admins")
        temp = self.c.fetchall()
        a = random.randint(0, len(temp) - 1)

        if t:
            self.c.execute("INSERT INTO user_to_admin VALUES(" + str(rando) + ","
                           + str(temp[a][0]) + ")")

        # Save the new information
        self.conn.commit()
        if t:
            # Destroy current widgets and display new user message
            window_cleaner(self.master)
            UserIdShow(self.master, rando)

    def back_to_splash(self):
        """Destroys current widgets and goes back to the main menu."""
        # Destroy current widgets and go to the main menu
        window_cleaner(self.master)
        Splash(self.master)


class UserIdShow(tk.Frame):
    """
    Display screen for account creation that shows the User ID
    """

    def __init__(self, master, rando):
        """Establish a tkinter frame and display the successful account creation
        information.

        :param rando The new users User ID.
        :param master The master frame of the GUI"""
        # Create the main Frame
        tk.Frame.__init__(self, master)
        self.master.title('Dork\'s Bank - Successful Account Creation')
        self.master.config(menu=tk.Menu(self.master))

        # Configure rows and columns
        for s in range(3):
            self.master.grid_rowconfigure(s, weight=1)
            self.master.grid_columnconfigure(s, weight=1)

        # Display users account number
        msg = tk.Message(self.master, text='Your Account ID is : ' + str(rando),
                         width=3000)
        msg.grid(row=0, column=1)

        # Display message
        msg_2 = tk.Message(self.master, text='Be sure to write it down and store it in '
                                             'a safe place!', width=3000)
        msg_2.grid(row=1, column=1)

        # Create okay button, calls back_to_splash
        ok_button = tk.Button(self.master, text='Okay', command=self.back_to_splash,
                              width=10)
        ok_button.grid(row=2, column=1)

        # Set frame layout
        self.master.minsize(800, 600)
        center(self.master.winfo_toplevel())

    def back_to_splash(self):
        """Destroy the current widgets and go back to the main menus."""
        # Destroy current widgets and to go main menu
        window_cleaner(self.master)
        Splash(self.master)


class ReturnUserMenu(tk.Frame):
    """
    The Return User window that will show all relevant account information.
    """

    def __init__(self, master, uid):
        """Establishes a connection to the database and then allows the user to log in
        to an existing user account

        :param uid """
        # Connect to the data base
        self.conn = sqlite3.connect('bank.db')
        self.c = self.conn.cursor()
        self.passer = uid

        # Create and configure the tkinter frame
        tk.Frame.__init__(self, master)
        self.master.title('Dork\'s Bank - Return User Menu')
        self.master.config(menu=tk.Menu(self.master))
        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_rowconfigure(6, weight=1)
        self.master.grid_columnconfigure(0, weight=1)
        self.master.grid_columnconfigure(6, weight=1)

        # Create a button to check balance, calls checkbalance
        check_balance_button = tk.Button(self.master, text='Check Balance',
                                         command=self.check_balance, width=25)
        check_balance_button.grid(row=1, column=1, pady=5)

        # Create a button to deposit cash, calls depositCash
        deposit_cash_button = tk.Button(self.master, text='Deposit Cash',
                                        command=self.deposit_cash, width=25)
        deposit_cash_button.grid(row=2, column=1, pady=5)

        # Create a button to transfer funds, calls transfer
        transfer_button = tk.Button(self.master, text='Transfer', command=self.transfer,
                                    width=25)
        transfer_button.grid(row=3, column=1, pady=5)

        # Create a button to add a loan, calls loans
        loans_button = tk.Button(self.master, text='Loans', command=self.loans, width=25)
        loans_button.grid(row=4, column=1, pady=5)

        # Create a button to withdraw cash, calls withdrawCash
        withdraw_cash_button = tk.Button(self.master, text='Withdraw Cash',
                                         command=self.withdraw_cash, width=25)
        withdraw_cash_button.grid(row=5, column=1, pady=5)

        # Create a button to exit, calls back_to_splash
        exit_button = tk.Button(self.master, text='Exit', command=self.back_to_splash,
                                width=10)
        exit_button.grid(row=6, column=1, pady=5)

        # Set frame layout
        self.master.minsize(800, 600)
        center(self.master.winfo_toplevel())

    def check_balance(self):
        """Clears the current widgets and displays the check balance page."""
        # Destroy current widgets
        window_cleaner(self.master)
        # Go to next display settings in CheckBalanceC
        CheckBalanceC(self.master, self.passer)

    def deposit_cash(self):
        """Clears the current widgets and displays the deposit page."""
        # Destroy current widgets
        window_cleaner(self.master)
        # Go to next display settings in DepositCashC
        DepositCashC(self.master, self.passer)

    def transfer(self):
        """Clears the current widgets and displays the transfer funds page."""
        # Destroy current widgets
        window_cleaner(self.master)
        # Go to the next display settings in TransferC
        TransferC(self.master, self.passer)

    def loans(self):
        """Clears the current widgets and displays the loans page."""
        # Destroy current widgets
        window_cleaner(self.master)
        # Go to the next display settings in LoansC
        LoansC(self.master, self.passer)

    def withdraw_cash(self):
        """Clears the current widgets and displays the withdraw cash page."""
        # Destroy current widgets
        window_cleaner(self.master)
        # Go to the next display settings in WithdrawCashC
        WithdrawCashC(self.master, self.passer)

    def back_to_splash(self):
        """Clears the current widgets and displays the main menu."""
        # Destroy current widgets
        window_cleaner(self.master)
        # Go back to main menu
        Splash(self.master)


class AdminUserMenu(tk.Frame):
    """
    The Admin User window that will show admin options.
    """

    def __init__(self, master, aid):
        """Creates the connection to the data base and displays the administrators
        options.

        :param master The master Tkinter frame.
        :param aid The admin ID"""

        # Connect to the database
        self.conn = sqlite3.connect('bank.db')
        self.c = self.conn.cursor()
        self.passer = aid

        # Build the TKinter frame
        tk.Frame.__init__(self, master)
        self.master.title('Dork\'s Bank - Admin Menu')
        self.master.config(menu=tk.Menu(self.master))

        # Configure rows and columns
        for s in range(8):
            self.master.grid_rowconfigure(s, weight=1)
        for s in range(3):
            self.master.grid_columnconfigure(s, weight=1)

        # Create "View Accounts" Button
        view_accounts = tk.Button(self.master, text='View Accounts', command=self.view_accounts, width=15)
        view_accounts.grid(row=0, column=1, padx=4)

        # Create "Deactivate account" Button
        deactivate_accounts = tk.Button(self.master, text='Deactivate Account', command=self.deactivate_account,
                                        width=15)
        deactivate_accounts.grid(row=1, column=1, padx=4)

        # Create "Reactivate Account" Button
        reactivate_accounts = tk.Button(self.master, text='Reactivate Account', command=self.reactivate_account,
                                        width=15)
        reactivate_accounts.grid(row=2, column=1, padx=4)

        # Create "Change" Button
        change = tk.Button(self.master, text='Change', command=self.change, width=15)
        change.grid(row=3, column=1, padx=4)

        # Create "Add Accounts" Button
        add_account = tk.Button(self.master, text='Add Account', command=self.add_account, width=15)
        add_account.grid(row=4, column=1, padx=4)

        # Create "Add Accounts" Button
        modify_account = tk.Button(self.master, text='add Loan', command=self.loans, width=15)
        modify_account.grid(row=5, column=1, padx=4)

        # Create "Reports" Button
        reports = tk.Button(self.master, text='Reports', command=self.reports, width=15)
        reports.grid(row=6, column=1, padx=4)

        # Create "Exit" Button
        close = tk.Button(self.master, text='Exit', command=self.back_to_splash, width=15)
        close.grid(row=7, column=1, padx=4)

        # set frame settings
        self.master.minsize(800, 600)
        center(self.master.winfo_toplevel())

    def view_accounts(self):
        """Destroys current widgets and displays the admin view accounts page."""
        # Destroy current widgets
        window_cleaner(self.master)
        # Go to the next display settings
        AdminViewAccounts(self.master, self.passer)

    def deactivate_account(self):
        """Destroys the current widgets and displays the deactivate accounts page."""
        # Destroy current widgets
        window_cleaner(self.master)
        # Go to the next display settings
        AdminDeactivateAccount(self.master, self.passer)

    def reactivate_account(self):
        """Destroys the current widgets and displays the reactivate accounts page."""
        # Destroy current widgets
        window_cleaner(self.master)
        # Go to the next display settings
        AdminReactivateAccount(self.master, self.passer)

    def change(self):
        """Destroys the current widgets and displays the change accounts page."""
        # Destroy current widgets
        window_cleaner(self.master)
        # Go to the next display settings
        AdminChangeAccounts(self.master, self.passer)

    def add_account(self):
        """Destroys the current widgets and displays the add account page."""
        # Destroy current widgets
        window_cleaner(self.master)
        # Go to the next display settings
        CreateUser1(self.master, self.passer)

    def loans(self):
        """Destroys the current widgets and displays the loans page."""
        # Destroy current widgets
        window_cleaner(self.master)
        # Go to the next display settings
        AddLoans(self.master, self.passer)

    def reports(self):
        """Destroys the current widgets and displays the reports page."""
        # Destroy current widgets
        window_cleaner(self.master)
        # Go to the next display settings
        AdminReports(self.master, self.passer)

    def back_to_splash(self):
        """Destroys the current widgets and displays the main menu page."""
        # Destroy current widgets
        window_cleaner(self.master)
        # Go to the next display settings
        Splash(self.master)


class CreateUser1(tk.Frame):
    """
    The Create User window for Admins that will show all information needed to create
    an account.
    """

    def __init__(self, master, eid):
        """Connects to the database and guides the user through a new account
        creatation process

        :param master The master GUI frame
        :param eid The employee ID
        """

        #  Connect to the data base
        self.conn = sqlite3.connect('bank.db')
        self.c = self.conn.cursor()
        self.passer = eid

        # Build the TKinter frame
        tk.Frame.__init__(self, master)
        self.master.title('Dork\'s Bank - Create Account')
        self.master.config(menu=tk.Menu(self.master))

        # Configure the rows and columns
        for s in range(6):
            self.master.grid_rowconfigure(s, weight=1)
            self.master.grid_columnconfigure(s, weight=1)

        # Create Buttons and their associated actions for the frame.
        first_name_l = tk.Label(self.master, text='First Name:')
        first_name_l.grid(row=0, column=0, sticky='E')

        self.first_name_text = tk.StringVar()
        first_name_entry = tk.Entry(self.master, textvariable=self.first_name_text)
        first_name_entry.grid(row=0, column=1)

        last_name_l = tk.Label(self.master, text='Last Name:')
        last_name_l.grid(row=0, column=2, sticky='E')

        self.last_name_text = tk.StringVar()
        last_name_entry = tk.Entry(self.master, textvariable=self.last_name_text)
        last_name_entry.grid(row=0, column=3)

        password_l = tk.Label(self.master, text='Password:')
        password_l.grid(row=1, column=0, sticky='E')

        self.password_text = tk.StringVar()
        password_entry = tk.Entry(self.master, textvariable=self.password_text, show="*")
        password_entry.grid(row=1, column=1)

        password_check_l = tk.Label(self.master, text='Re-Enter Password:')
        password_check_l.grid(row=2, column=0, sticky='E')

        self.password_check_text = tk.StringVar()
        password_check_entry = tk.Entry(self.master,
                                        textvariable=self.password_check_text,
                                        show="*")
        password_check_entry.grid(row=2, column=1)

        opening_balance_l = tk.Label(self.master, text='Opening Balance:')
        opening_balance_l.grid(row=6, column=0, sticky='E')

        self.opening_balance_text = tk.IntVar()
        opening_balance_entry = tk.Entry(self.master,
                                         textvariable=self.opening_balance_text)
        opening_balance_entry.grid(row=6, column=1)

        submit = tk.Button(self.master, text='Submit', command=self.comm, width=10)
        submit.grid(row=6, column=5, sticky='SE', padx=4, pady=4)

        back = tk.Button(self.master, text='Cancel', command=self.back_to_splash, width=10)
        back.grid(row=7, column=5, sticky='SE', padx=5, pady=5)

        self.master.minsize(800, 600)
        center(self.master.winfo_toplevel())

    def comm(self):
        """Submits users data to the database."""
        namecheck = False
        lengthcheck = False
        t = True

        p = 0
        while p != 1:
            rando = random.randint(1, 99999)
            self.c.execute("select * from customer where uid = " + str(rando))
            temp = self.c.fetchall()
            if len(temp) == 1:
                p = 0
            elif len(temp) == 0:
                p = 1

        # Check for valid name conditions
        while not (namecheck and lengthcheck):
            username = self.first_name_text.get()
            username2 = self.last_name_text.get()

            namecheck = True
            if len(username) > 3 and len(username2) > 3:
                lengthcheck = True

            else:
                lengthcheck = False
                # make into a pop up falg2 t=F
                t = False
                DialogBoxes.name_length_error()
                break

        # Check for a valid password
        pin = ""
        while len(pin) < 4:
            if self.password_text.get() == self.password_check_text.get():
                pin = self.password_text.get()
            if len(pin) > 4:
                # make into a pop up flag1 t=T
                break
            # make into a pop up falg2 t=F
            t = False
            DialogBoxes.password_length_error()
            break


        # Get and check balance information
        while True:
            try:
                while balance < float(100):
                    balance = float(self.opening_balance_text.get())
                    if balance >= 100.0:
                        break
                    # make into a pop up flag 3 t=F
                    t = False

                    DialogBoxes.opening_balance_error()
                    break
                break
            except tk.TclError:
                t = False
                DialogBoxes.input_error()
                break
        # Insert data into the database
        while True:
            try:
                if t:
                    self.c.execute("INSERT INTO customer VALUES("
                                   + str(rando) + ", '" + pin + "', '" + username
                                   + "', '" + username2 + "',1)")
                break
            except sqlite3.OperationalError:
                self.conn.rollback()
                # make into a pop up falg1 t=F
                DialogBoxes.system_breach_warning()
                break

        p = 0
        while p != 1:
            rando2 = random.randint(1, 99999)

            self.c.execute("select * from checking_account where cid = "
                           + str(rando2))
            temp = self.c.fetchall()
            if len(temp) == 1:
                p = 0
            if len(temp) == 0:
                p = 1
        p = 0
        while p != 1:
            rando3 = random.randint(1, 99999)
            self.c.execute("select * from saving_account where sid = " + str(rando3))
            temp = self.c.fetchall()
            if len(temp) == 1:
                p = 0
            if len(temp) == 0:
                p = 1

        # Update the database information
        if t :
            self.c.execute("DROP TRIGGER add_and_link_accounts")
            self.c.execute("DROP TRIGGER link_accounts")
            self.c.execute(
                '''CREATE TRIGGER add_and_link_accounts AFTER INSERT ON checking_account 
                BEGIN INSERT INTO saving_account (sid, amount) VALUES (''' + str(rando3)
                + ''', 0);  END;''')

            self.c.execute(
                '''CREATE TRIGGER link_accounts AFTER INSERT ON checking_account BEGIN 
                INSERT INTO accounts (uid, cid,sid,lid) VALUES (''' + str(rando)
                + ''',''' + str(rando2) + ''',''' + str(rando3) + ''',NULL);  END;''')
            balance = 0

        

        # update account balance information in the database
        while True:
            try:
                if t:
                    self.c.execute("INSERT INTO checking_account VALUES("
                                   + str(rando2) + ", " + str(balance) + ")")
                break
            except sqlite3.OperationalError:
                self.conn.rollback()
                DialogBoxes.system_breach_warning()
                break

        # Assign an administrator
        self.c.execute("SELECT aid FROM admins")
        temp = self.c.fetchall()
        a = random.randint(0, len(temp) - 1)

        if t:
            self.c.execute("INSERT INTO user_to_admin VALUES(" + str(rando)
                           + "," + str(temp[a][0]) + ")")

        self.conn.commit()
        if t:
            window_cleaner(self.master)
            UserIdShow1(self.master, rando, self.passer)

    def back_to_splash(self):
        """Destroys the current widgets and displays the administrators menu."""
        window_cleaner(self.master)
        AdminUserMenu(self.master, self.passer)


class UserIdShow1(tk.Frame):
    """
    The window displayed to Admins after they create an account
    """

    def __init__(self, master, rando, eid):
        """Creates a window to show the administrator the account they created.

        :param master The master GUI
        :param rando The user's ID
        :param eid The employee ID"""

        # Connect to the database
        tk.Frame.__init__(self, master)
        self.passer = eid

        # Build and display frame
        self.master.title('Dork\'s Bank - Successful Account Creation')
        self.master.config(menu=tk.Menu(self.master))

        # Configure rows and columns
        for s in range(3):
            self.master.grid_rowconfigure(s, weight=1)
            self.master.grid_columnconfigure(s, weight=1)

        # Set frame message
        msg = tk.Message(self.master, text='The Account ID is : ' + str(rando),
                         width=3000)
        msg.grid(row=0, column=1)
        msg_2 = tk.Message(self.master, text='Be sure to tell the user to write it down'
                                             ' and store it in a safe place!',
                           width=3000)
        msg_2.grid(row=1, column=1)
        ok_button = tk.Button(self.master, text='Okay', command=self.back_to_splash,
                              width=10)
        ok_button.grid(row=2, column=1)

        # Set frame
        self.master.minsize(800, 600)
        center(self.master.winfo_toplevel())

    def back_to_splash(self):
        """Destroys current widgets and displays the administrator menu."""
        window_cleaner(self.master)
        AdminUserMenu(self.master, self.passer)


class AdminViewAccounts(tk.Frame):
    """
    The window for Admins to view Account Information
    """

    def __init__(self, master, aid):
        """Connects to the database and displays the user accounts to an administrator.

        :param master The master frame GUI
        :param aid The admin ID"""

        # Connect to the data base
        self.conn = sqlite3.connect('bank.db')
        self.c = self.conn.cursor()
        self.passer = aid

        # Build the tkinter frame
        tk.Frame.__init__(self, master)
        self.master.title('Dork\'s Bank - Admin - View Accounts')
        self.master.config(menu=tk.Menu(self.master))

        # Pull account information
        self.c.execute("DROP VIEW T_accounts")

        self.c.execute(
            "CREATE VIEW T_accounts AS SELECT customer.uid,customer.first,customer.last,"
            "checking_account.amount AS checking_amount, saving_account.amount AS "
            "savings_amount,customer.active FROM customer NATURAL JOIN accounts JOIN "
            "checking_account, saving_account WHERE accounts.cid=checking_account.cid "
            "AND accounts.sid=saving_account.sid ")
        self.c.execute("SELECT * FROM T_accounts")
        temp = self.c.fetchall()

        # Display account information
        a = ''
        for row in temp:
            a = a + str(row) + '\n'

        password_l = tk.Label(self.master, text="Checking account:\n " + a)
        password_l.grid(row=2, column=1, sticky='W', pady=5)

        back = tk.Button(self.master, text='Back', command=self.back_to_admin_menu,
                         width=10)
        back.grid(row=3, column=3, padx=3)

        self.master.minsize(800, 600)
        center(self.master.winfo_toplevel())

    def back_to_admin_menu(self):
        """Destroys current widgets and displays the administrator page."""
        window_cleaner(self.master)
        AdminUserMenu(self.master, self.passer)


class AdminDeactivateAccount(tk.Frame):
    """
    The window where Admins will Deactivate an active Account
    """

    def __init__(self, master, aid):
        """Initialize the AdminDeactiveAccount frame and connection to the database"""
        # Connect to the database
        self.conn = sqlite3.connect('bank.db')
        self.c = self.conn.cursor()
        self.passer = aid

        # Build the frame
        tk.Frame.__init__(self, master)
        self.master.title('Dork\'s Bank - Admin - Deactivate Account')
        self.master.config(menu=tk.Menu(self.master))

        # Build labels and their listeners
        user_name_l = tk.Label(self.master, text="User: ")
        user_name_l.grid(row=1, column=1, sticky='E', pady=5)

        self.opening_balance_text = tk.IntVar()
        opening_balance_entry = tk.Entry(self.master,
                                         textvariable=self.opening_balance_text)
        opening_balance_entry.grid(row=1, column=2)

        back = tk.Button(self.master, text='Back', command=self.back_to_admin_menu,
                         width=10)
        back.grid(row=3, column=3, padx=3)
        submit = tk.Button(self.master, text='Submit', command=self.on_submit1,
                           width=10)
        submit.grid(row=2, column=3, padx=3)

        self.master.minsize(800, 600)
        center(self.master.winfo_toplevel())

    def on_submit1(self):
        """Submits changes made while deactivating an account."""
        while True:
            try:
                # Pull data from the database... like Ron Holmes
                self.c.execute(
                    "select t.uid,t.first,t.last from (select customer.uid,"
                    "customer.first,customer.last,checking_account.amount as checking_"
                    "amount, saving_account.amount as savings_amount,customer.active "
                    "from customer natural join accounts join checking_account, saving"
                    "_account where accounts.cid=checking_account.cid and "
                    "accounts.sid=saving_account.sid) as t  join user_to_admin where "
                    "t.uid =user_to_admin.uid and user_to_admin.aid=" + self.passer)
                temp = self.c.fetchall()
                if len(temp) == 0:
                    DialogBoxes.no_active_user_error()
                    break
                else:

                    # update the database and go to the admin display
                    theuser = int(self.opening_balance_text.get())
                    self.c.execute("UPDATE customer set active = 0 where uid="
                                   + str(theuser))
                    self.conn.commit()
                    window_cleaner(self.master)
                    AdminUserMenu(self.master, self.passer)
                    break
            except tk.TclError:
                DialogBoxes.input_error()
                break
            except sqlite3.OperationalError:
                DialogBoxes.try_again_error()
                break
            except ValueError:
                DialogBoxes.try_again_error()
                break

    def back_to_admin_menu(self):
        """Destroys current widgets and goes back to the administrator menu."""
        window_cleaner(self.master)
        AdminUserMenu(self.master, self.passer)


class AdminReactivateAccount(tk.Frame):
    """
    The window where an Admin will Reactivate a Deactivated Account
    """

    def __init__(self, master, aid):
        """Creates a connection to the database and displays the administrators
        reactivate an account page.

        :param master The master frame for the GUI
        :param aid The admin ID
        """

        # Connect to the database
        self.conn = sqlite3.connect('bank.db')
        self.c = self.conn.cursor()
        self.passer = aid

        # Build the frame
        tk.Frame.__init__(self, master)
        self.master.title('Dork\'s Bank - Admin - Deactivate Account')
        self.master.config(menu=tk.Menu(self.master))

        # Create labels and their listeners
        user_name_l = tk.Label(self.master, text="User: ")
        user_name_l.grid(row=1, column=1, sticky='E', pady=5)

        self.opening_balance_text = tk.IntVar()
        opening_balance_entry = tk.Entry(self.master,
                                         textvariable=self.opening_balance_text)
        opening_balance_entry.grid(row=1, column=2)

        # Create buttons and their actions
        back = tk.Button(self.master, text='Back', command=self.back_to_admin_menu,
                         width=10)
        back.grid(row=3, column=3, padx=3)
        submit = tk.Button(self.master, text='Submit', command=self.on_submit1,
                           width=10)
        submit.grid(row=2, column=3, padx=3)

        self.master.minsize(800, 600)
        center(self.master.winfo_toplevel())

    def on_submit1(self):
        """Submits changes made during reactivate account to the database"""
        while True:
            try:
                # Pulls the data from the database
                self.c.execute(
                    "select T_accounts.uid,T_accounts.first,T_accounts.last from T_"
                    "accounts join user_to_admin where T_accounts.uid=user_to_admin.uid"
                    " and T_accounts.active=1 and user_to_admin.aid=" + self.passer)
                temp = self.c.fetchall()

                # questions my choice to become a CS major then prints data
                for row in temp:
                    print(row)
                if len(temp) == 0:
                    DialogBoxes.no_active_user_error()
                    break
                else:
                    # Gets balance and commits the changes to the database
                    theuser = int(self.opening_balance_text.get())
                    self.c.execute("UPDATE customer set active = 1 where uid="
                                   + str(theuser))
                    self.conn.commit()
                    window_cleaner(self.master)
                    AdminUserMenu(self.master, self.passer)
                    break
            except tk.TclError:
                DialogBoxes.input_error()
                break
            except sqlite3.OperationalError:
                DialogBoxes.try_again_error()
                break
            except ValueError:
                DialogBoxes.try_again_error()
                break

    def back_to_admin_menu(self):
        """Destroys current widgets and goes back to the Administrators menu."""
        window_cleaner(self.master)
        AdminUserMenu(self.master, self.passer)


class AdminChangeAccounts(tk.Frame):
    """
    The window where an Admin will be able to edit account information
    """

    def __init__(self, master, aid):
        """
        Initializes the connection with the database and builds the Tkinter
        frame to allow Aministrators to change account information
        """

        # Connect to the database
        self.conn = sqlite3.connect('bank.db')
        self.c = self.conn.cursor()
        self.passer = aid

        # Build the Tkinter frame, label, and buttons.
        tk.Frame.__init__(self, master)
        self.master.title('Dork\'s Bank - Admin - Change')
        self.master.config(menu=tk.Menu(self.master))

        user_name_l = tk.Label(self.master, text="User: ")
        user_name_l.grid(row=1, column=1, sticky='E', pady=5)

        self.opening_balance_text = tk.IntVar()
        opening_balance_entry = tk.Entry(self.master,
                                         textvariable=self.opening_balance_text)
        opening_balance_entry.grid(row=1, column=2)

        submit = tk.Button(self.master, text='Submit', command=self.on_submit1, width=10)
        submit.grid(row=2, column=3, padx=3)

        back = tk.Button(self.master, text='Back', command=self.back_to_admin_menu,
                         width=10)
        back.grid(row=3, column=3, padx=3)

        self.master.minsize(800, 600)
        center(self.master.winfo_toplevel())

    def back_to_admin_menu(self):
        """Destroys current widgets and goes back to the administrators menu."""
        window_cleaner(self.master)
        AdminUserMenu(self.master, self.passer)

    def on_submit1(self):
        """Verifies information and commits changes to the database."""
        while True:
            try:
                # Pulls information from the data base
                self.c.execute(
                    "select T_accounts.uid,T_accounts.first,T_accounts.last from T_"
                    "accounts join user_to_admin where T_accounts.uid=user_to_admin.uid"
                    " and user_to_admin.aid=" + self.passer)
                temp = self.c.fetchall()

                # Displays the data
                for row in temp:
                    print(row)

                # Changes the account information
                theuser = int(self.opening_balance_text.get())
                self.c.execute("select * from customer where uid=" + str(theuser))
                window_cleaner(self.master)
                AdminChangeAccounts1(self.master, self.passer, theuser)
                break
            except tk.TclError:
                DialogBoxes.input_error()
                break
            except sqlite3.OperationalError:
                DialogBoxes.try_again_error()
                break


class AdminChangeAccounts1(tk.Frame):
    """
    The window where an Admin will be able to edit account information
    """

    def __init__(self, master, aid, uid):
        """Initializes the AdminChangeAccouts1 Frame.

        :param master The master GUI frame
        :param aid The admin ID
        :param uid The user ID
        """

        # Connect to the data base
        self.conn = sqlite3.connect('bank.db')
        self.c = self.conn.cursor()
        self.passer = aid
        self.passer1 = uid

        # Build the TKinter frame, labels, and buttons
        tk.Frame.__init__(self, master)
        self.master.title('Dork\'s Bank - Admin - Change')
        self.master.config(menu=tk.Menu(self.master))

        user_name_l = tk.Label(self.master, text="password: ")
        user_name_l.grid(row=1, column=1, sticky='E', pady=5)

        user_name_2 = tk.Label(self.master, text="First Name: ")
        user_name_2.grid(row=2, column=1, sticky='E', pady=5)

        user_name_3 = tk.Label(self.master, text="Last Name: ")
        user_name_3.grid(row=3, column=1, sticky='E', pady=5)
        self.c.execute("select * from customer where uid=" + str(self.passer1))

        # Get data from database
        temp = self.c.fetchall()
        part2 = temp[0][1]
        part3 = temp[0][2]
        part4 = temp[0][3]

        self.opening_balance_text = tk.StringVar()
        opening_balance_entry = tk.Entry(self.master,
                                         textvariable=self.opening_balance_text,
                                         show="*")
        opening_balance_entry.grid(row=1, column=2)
        opening_balance_entry.insert(0, str(part2))
        self.opening_balance_text1 = tk.StringVar()
        opening_balance_entry1 = tk.Entry(self.master,
                                          textvariable=self.opening_balance_text1)
        opening_balance_entry1.grid(row=2, column=2)
        opening_balance_entry1.insert(0, str(part3))
        self.opening_balance_text2 = tk.StringVar()
        opening_balance_entry2 = tk.Entry(self.master,
                                          textvariable=self.opening_balance_text2)
        opening_balance_entry2.grid(row=3, column=2)
        opening_balance_entry2.insert(0, str(part4))

        submit = tk.Button(self.master, text='Submit', command=self.on_submit1,
                           width=10)
        submit.grid(row=2, column=3, padx=3)

        back = tk.Button(self.master, text='Back', command=self.back_to_admin_menu,
                         width=10)
        back.grid(row=3, column=3, padx=3)

        self.master.minsize(800, 600)
        center(self.master.winfo_toplevel())

    def back_to_admin_menu(self):
        """Destroys current widgets and displays the Admin user menu."""
        window_cleaner(self.master)
        AdminUserMenu(self.master, self.passer)

    def on_submit1(self):
        """Commits the changes made to a users account by an administrator."""
        while True:
            try:
                part2 = self.opening_balance_text.get()
                part3 = self.opening_balance_text1.get()
                part4 = self.opening_balance_text2.get()

                self.c.execute(
                    "UPDATE customer set password='" + part2 + "', first='" + part3
                    + "', last='" + part4 + "' where uid=" + str(self.passer1))
                self.conn.commit()
                window_cleaner(self.master)
                AdminUserMenu(self.master, self.passer)
                break
            except tk.TclError:
                DialogBoxes.input_error()
                break
            except sqlite3.OperationalError:
                DialogBoxes.try_again_error()
                break


class AddLoans(tk.Frame):
    """
    The window where Admins will be able to work with Account Loans
    """

    def __init__(self, master, aid):
        """Initializes the connection to the database and the add loans frame.

        :param master The master GUI frame
        :param aid The admin ID
        """

        # Connect to the database
        self.conn = sqlite3.connect('bank.db')
        self.c = self.conn.cursor()
        self.passer = aid

        # Build the Frame
        tk.Frame.__init__(self, master)
        self.master.title('Dork\'s Bank - Modify Accounts')
        self.master.config(menu=tk.Menu(self.master))

        user_name_l = tk.Label(self.master, text="User: ")
        user_name_l.grid(row=1, column=1, sticky='E', pady=5)

        self.opening_balance_text = tk.IntVar()
        opening_balance_entry = tk.Entry(self.master,
                                         textvariable=self.opening_balance_text)
        opening_balance_entry.grid(row=1, column=2)

        back = tk.Button(self.master, text='Back', command=self.back_to_admin_menu,
                         width=10)
        back.grid(row=3, column=3, padx=3)

        submit = tk.Button(self.master, text='Submit', command=self.on_submit1,
                           width=10)
        submit.grid(row=2, column=3, padx=3)

        self.master.minsize(800, 600)
        center(self.master.winfo_toplevel())

    def back_to_admin_menu(self):
        """Destroy current widgets and display the Administrators menu."""
        window_cleaner(self.master)
        AdminUserMenu(self.master, self.passer)

    def on_submit1(self):
        """Commits the changes to the users loans by an administrator to the database."""
        while True:
            try:
                self.c.execute(
                    "select T_accounts.uid,T_accounts.first,T_accounts.last from T_"
                    "accounts join user_to_admin where T_accounts.uid=user_to_admin.uid"
                    " and  T_accounts.active=1 and user_to_admin.aid=" + self.passer)
                temp = self.c.fetchall()

                aplha = int(self.opening_balance_text.get())
                self.c.execute("select lid from accounts where uid=" + str(aplha))
                tmp = self.c.fetchall()
                if tmp[0][0] is None:
                    window_cleaner(self.master)
                    Loans1(self.master, self.passer, aplha)
                    break
                else:
                    window_cleaner(self.master)
                    Loans2(self.master, self.passer, aplha)
                    break
            except tk.TclError:
                DialogBoxes.input_error()
                break
            except sqlite3.OperationalError:
                DialogBoxes.try_again_error()
                break


class Loans1(tk.Frame):
    """
    The window where Admins will be able to work with Account Loans
    """

    def __init__(self, master, aid, uid):
        """Initializes the connection with the database and the graphical user interface
        for Account Loans.

        :param master The master Frame for the GUI
        :param aid  The admin ID
        :param uid The user ID"""

        # Connect to the database
        self.conn = sqlite3.connect('bank.db')
        self.c = self.conn.cursor()
        self.passer = aid
        self.passer1 = uid

        # Establish the Frames.
        tk.Frame.__init__(self, master)
        self.master.title('Dork\'s Bank - Modify Accounts')
        self.master.config(menu=tk.Menu(self.master))

        # Fetch and display loan information
        self.c.execute("SELECT ltid FROM loans")
        temp1 = self.c.fetchall()
        a = ''
        for row in temp1:
            a = a + str(row) + '\n'

        # Create Labels, buttons, and listeners for the frame.
        password_l = tk.Label(self.master, text="Checking account:\n " + a)
        password_l.grid(row=1, column=1, sticky='W', pady=5)

        user_name_l = tk.Label(self.master, text="Loan type ID: ")
        user_name_l.grid(row=4, column=1, sticky='E', pady=5)

        self.opening_balance_text = tk.IntVar()
        opening_balance_entry = tk.Entry(self.master,
                                         textvariable=self.opening_balance_text)
        opening_balance_entry.grid(row=5, column=2)

        user_name_2 = tk.Label(self.master, text="Amount: ")
        user_name_2.grid(row=4, column=2, sticky='E', pady=5)

        self.opening_balance_text1 = tk.IntVar()
        opening_balance_entry1 = tk.Entry(self.master,
                                          textvariable=self.opening_balance_text1)
        opening_balance_entry1.grid(row=5, column=2)

        back = tk.Button(self.master, text='Back', command=self.back_to_admin_menu,
                         width=10)
        back.grid(row=3, column=3, padx=3)

        submit = tk.Button(self.master, text='Submit', command=self.on_submit1,width=10)
        submit.grid(row=2, column=3, padx=3)

        self.master.minsize(800, 600)
        center(self.master.winfo_toplevel())

    def back_to_admin_menu(self):
        """Destroys the current widgets and goes back to the Administrator user menu."""
        window_cleaner(self.master)
        AdminUserMenu(self.master, self.passer)

    def on_submit1(self):
        """Commits the changes to the user loan by an administrator to the data base."""
        while True:
            try:
                bravo = int(self.opening_balance_text.get())
                rando = random.randint(0, 99999)
                charly = int(self.opening_balance_text1.get())
                self.c.execute("select aid from user_to_admin where uid="
                               + str(self.passer1))
                temo = self.c.fetchall()
                self.c.execute("select llid from admins where aid=" + str(temo[0][0]))
                him = self.c.fetchall()
                him = him[0][0]
                self.c.execute("select cid from accounts where uid=" + str(self.passer1))
                cid = self.c.fetchall()
                cid = cid[0][0]
                self.c.execute("select amount from checking_account where cid="
                               + str(cid))
                total = self.c.fetchall()
                total = int(total[0][0]) + charly
                self.c.execute(
                    "INSERT INTO loan_account VALUES(" + str(rando) + "," + str(charly) + "," + str(bravo) + "," + str(
                        him) + ")")
                self.c.execute("UPDATE accounts set lid=" + str(rando) + " where uid="
                               + str(self.passer1))
                self.c.execute("UPDATE checking_account set amount=" + str(total)
                               + " where cid=" + str(cid))
                self.conn.commit()
                window_cleaner(self.master)
                AdminUserMenu(self.master, self.passer)
                break
            except tk.TclError:
                DialogBoxes.input_error()
                break
            except sqlite3.OperationalError:
                DialogBoxes.try_again_error()
                break


class Loans2(tk.Frame):
    """
    The window where Admins will be able to work with Account Loans
    """

    def __init__(self, master, aid, uid):
        """Initializes the connection with the database and builds the Loans2 Frame."""
        # Connect to the data base
        self.conn = sqlite3.connect('bank.db')
        self.c = self.conn.cursor()
        self.passer = aid
        self.passer1 = uid

        # Builds the Frame
        tk.Frame.__init__(self, master)
        self.master.title('Dork\'s Bank - Modify Accounts')
        self.master.config(menu=tk.Menu(self.master))

        # Add the widgets
        user_name_2 = tk.Label(self.master, text="Amount: ")
        user_name_2.grid(row=4, column=2, sticky='E', pady=5)

        self.opening_balance_text1 = tk.IntVar()
        opening_balance_entry1 = tk.Entry(self.master,
                                          textvariable=self.opening_balance_text1)
        opening_balance_entry1.grid(row=5, column=2)

        back = tk.Button(self.master, text='Back', command=self.back_to_admin_menu,
                         width=10)
        back.grid(row=3, column=3, padx=3)

        submit = tk.Button(self.master, text='Submit', command=self.on_submit1,
                           width=10)
        submit.grid(row=2, column=3, padx=3)

        self.master.minsize(800, 600)
        center(self.master.winfo_toplevel())

    def back_to_admin_menu(self):
        """Destroys the current widgets and goes back to the Administrator user menu page."""
        window_cleaner(self.master)
        AdminUserMenu(self.master, self.passer)

    def on_submit1(self):
        """Commits the changes made by the administrator to the database."""
        while True:
            try:
                charly = int(self.opening_balance_text1.get())
                self.c.execute("select cid from accounts where uid=" + str(self.passer1))
                cid = self.c.fetchall()
                cid = cid[0][0]
                self.c.execute("select lid from accounts where uid=" + str(self.passer1))
                lid = self.c.fetchall()
                lid = lid[0][0]
                self.c.execute("select amount from loan_account where lid=" + str(lid))
                t2 = self.c.fetchall()
                t2 = int(t2[0][0]) + charly

                self.c.execute("select amount from checking_account where cid="
                               + str(cid))
                total = self.c.fetchall()
                total = int(total[0][0]) + charly

                self.c.execute("UPDATE loan_account set amount=" + str(t2)
                               + " where lid=" + str(lid))

                self.c.execute("UPDATE checking_account set amount=" + str(total)
                               + " where cid=" + str(cid))
                self.conn.commit()
                window_cleaner(self.master)
                AdminUserMenu(self.master, self.passer)
                break
            except tk.TclError:
                DialogBoxes.input_error()
                break
            except sqlite3.OperationalError:
                DialogBoxes.try_again_error()
                break


class AdminReports(tk.Frame):
    """
    The window where Admins will be able to display Reports
    """

    def __init__(self, master, aid):
        """Initializes the connection with the database and builds the frame for admin
        reports.

        :param master The master frame for the GUI
        :param aid The admin ID
        """

        # Connects to the database
        self.conn = sqlite3.connect('bank.db')
        self.c = self.conn.cursor()
        self.passer = aid

        # Build the frame
        tk.Frame.__init__(self, master)
        self.master.title('Dork\'s Bank - Reports')
        self.master.config(menu=tk.Menu(self.master))

        # Make Buttons for the various reports
        view_accounts = tk.Button(self.master, text='View total bank assests',
                                  command=self.view_total_bank_asssests, width=35)
        view_accounts.grid(row=0, column=1, padx=4)

        deactivate_accounts = tk.Button(self.master, text='view most valuable customer',
                                        command=self.view_most_valuable_customer,
                                        width=35)
        deactivate_accounts.grid(row=1, column=1, padx=4)

        reactivate_accounts = tk.Button(self.master, text='view avg Account',
                                        command=self.view_avg_savings_and_avg_checking_accounts,
                                        width=35)
        reactivate_accounts.grid(row=2, column=1, padx=4)

        back = tk.Button(self.master, text='Back',
                         command=self.back_to_admin_menu, width=10)
        back.grid(row=3, column=3, padx=3)

        self.master.minsize(800, 600)
        center(self.master.winfo_toplevel())

    def back_to_admin_menu(self):
        """Destroys current widgets and goes back to the administrator user page."""
        window_cleaner(self.master)
        AdminUserMenu(self.master, self.passer)

    def view_total_bank_asssests(self):
        """Destroys the current widgets and goes to the Statistics page."""
        window_cleaner(self.master)
        Stats(self.master, self.passer)

    def view_most_valuable_customer(self):
        """Gives a shout out to the customer making us the most money."""
        window_cleaner(self.master)
        Stats1(self.master, self.passer)

    def view_avg_savings_and_avg_checking_accounts(self):
        """Destroys the current widgets and goes to the average account holdings page."""
        window_cleaner(self.master)
        Stats2(self.master, self.passer)


class Stats(tk.Frame):
    """
    The window where Admins will be able to display Account Statistics
    """

    def __init__(self, master, aid):
        """Initializes the connection with the database and displays the total assets.

        :param master The master frame for the GUI
        :param aid The admin ID"""

        # Connect to the database
        self.conn = sqlite3.connect('bank.db')
        self.c = self.conn.cursor()
        self.passer = aid

        # Build the frame for the gui.
        tk.Frame.__init__(self, master)
        self.master.title('Dork\'s Bank - Reports')
        self.master.config(menu=tk.Menu(self.master))

        # Get the sum of each account
        self.c.execute(
            "SELECT sum (checking_account.amount + saving_account.amount) FROM checking_account, saving_account")
        temp1 = self.c.fetchall()
        a = ''
        for row in temp1:
            a = a + str(row) + '\n'

        # Display the total bank assets.
        password_l = tk.Label(self.master, text="Total assests:\n " + a)
        password_l.grid(row=1, column=1, sticky='W', pady=5)

        back = tk.Button(self.master, text='Back', command=self.back_to_admin_menu, width=10)
        back.grid(row=3, column=3, padx=3)

    def back_to_admin_menu(self):
        """Destroy all current widgets and go back to the administrator reports page."""
        window_cleaner(self.master)
        AdminReports(self.master, self.passer)


class Stats1(tk.Frame):
    """
    The window where Admins will be able to display Account Statistics
    """

    def __init__(self, master, aid):
        """Initializes the connection with the database and builds the GUI frame.

        :param master The master frame for the GUI.
        :param aid The admin ID"""

        # Connects to the database
        self.conn = sqlite3.connect('bank.db')
        self.c = self.conn.cursor()
        self.passer = aid

        # Builds the gui's frame
        tk.Frame.__init__(self, master)
        self.master.title('Dork\'s Bank - Reports')
        self.master.config(menu=tk.Menu(self.master))

        # Finds the most valuable customer
        self.c.execute(
            "SELECT T_accounts.first, T_accounts.last, sum (T_accounts.checking_amount "
            "+ T_accounts.savings_amount ) AS Total_Assets FROM T_accounts GROUP BY T_"
            "accounts.first, T_accounts.last ORDER BY Total_Assets DESC")
        temp1 = self.c.fetchall()
        a = ''
        for row in temp1:
            a = a + str(row) + '\n'

        # Displays the most valuable customer
        password_l = tk.Label(self.master, text="Most valuable customer:\n " + a)
        password_l.grid(row=1, column=1, sticky='W', pady=5)

        back = tk.Button(self.master, text='Back', command=self.back_to_admin_menu,
                         width=10)
        back.grid(row=3, column=3, padx=3)

    def back_to_admin_menu(self):
        """Destroys all current widgets and goes back to the administrator reports page."""
        window_cleaner(self.master)
        AdminReports(self.master, self.passer)


class Stats2(tk.Frame):
    """
    The window where Admins will be able to display Account Statistics
    """

    def __init__(self, master, aid):
        """Initializes the connection with the database and builds the frame for
           the average account holdings.

           :param master The main GUI frame.
           :param aid The admin ID
           """

        # Connects to the database
        self.conn = sqlite3.connect('bank.db')
        self.c = self.conn.cursor()
        self.passer = aid

        # builds the frame
        tk.Frame.__init__(self, master)
        self.master.title('Dork\'s Bank - Reports')
        self.master.config(menu=tk.Menu(self.master))

        # calculates and display's the average account value
        self.c.execute(
            "SELECT avg(checking_account.amount) AS Bank_AVG_Assets FROM checking_"
            "account UNION SELECT avg(saving_account.amount) FROM saving_account")
        temp1 = self.c.fetchall()
        a = ''
        for row in temp1:
            a = a + str(row) + '\n'

        password_l = tk.Label(self.master, text="AVG account:\n " + a)
        password_l.grid(row=1, column=1, sticky='W', pady=5)

        back = tk.Button(self.master, text='Back', command=self.back_to_admin_menu,
                         width=10)
        back.grid(row=3, column=3, padx=3)

    def back_to_admin_menu(self):
        """Destroys current widgets and goes back to the administrator reports page."""
        window_cleaner(self.master)
        AdminReports(self.master, self.passer)


class WithdrawCashC(tk.Frame):
    """
    The window where Users will be able to Withdraw funds from their Accounts.
    Both Checking and Savings
    """

    def __init__(self, master, uid):
        """
        Initializes connection with the database and builds the frame for the user
        to withdraw funds from their accounts."""
        # Connects with the database
        self.conn = sqlite3.connect('bank.db')
        self.c = self.conn.cursor()
        self.passer = uid

        # Builds the frame for the gui.
        tk.Frame.__init__(self, master)
        self.master.title('Dork\'s Bank - Withdraw')
        self.master.config(menu=tk.Menu(self.master))

        # Configure the rows and columns
        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_rowconfigure(6, weight=1)
        self.master.grid_columnconfigure(0, weight=1)
        self.master.grid_columnconfigure(6, weight=1)

        # Make an amount label
        user_name_l = tk.Label(self.master, text="Amount: ")
        user_name_l.grid(row=1, column=1, sticky='E', pady=5)

        # Get the intial account balance
        self.opening_balance_text = tk.IntVar()
        opening_balance_entry = tk.Entry(self.master,
                                         textvariable=self.opening_balance_text)
        opening_balance_entry.grid(row=1, column=2)

        # Create buttons for the checking or savigns account.
        submit_button = tk.Button(self.master, text='From Checking',
                                  command=self.on_submit, width=15)
        submit_button.grid(row=1, column=3, padx=4)
        submit_button1 = tk.Button(self.master, text='From Savings',
                                   command=self.on_submit1, width=15)
        submit_button1.grid(row=2, column=3, padx=4)

        back = tk.Button(self.master, text='Back', command=self.back_to_splash, width=10)
        back.grid(row=3, column=3, padx=4)

        self.master.minsize(800, 600)
        center(self.master.winfo_toplevel())

    def on_submit(self):
        """Executed when the user selects to withdraw from the checking account.  It
           performs error checking and allows the money to be withdrawn if available."""
        # Get amounts available to the user
        self.c.execute(
            "select amount from customer join accounts join checking_account where "
            "customer.uid=accounts.uid and accounts.cid=checking_account.cid and "
            "customer.uid = " + self.passer)
        temp = self.c.fetchall()
        temp = int(temp[0][0])
        self.c.execute(
            "select accounts.cid from customer join accounts join checking_account where "
            "customer.uid=accounts.uid and accounts.cid=checking_account.cid and "
            "customer.uid = " + self.passer)
        temp2 = self.c.fetchall()
        temp2 = int(temp2[0][0])

        # If the amount to be withdrawn is available, deduct it from the account and
        # update the database.
        valid = False
        while not valid:
            
            try:
                amount = self.opening_balance_text.get()
                if (temp<float(amount)):
                    if ((temp-float(amount))>-200):
                        amount=amount+45
                    else:
                        DialogBoxes.Over_draft_error()
                        break 
                    
                temp -= float(amount)
                valid = True
                self.c.execute("update checking_account set amount = " + str(temp)
                               + " where cid=" + str(temp2))
                self.conn.commit()
                window_cleaner(self.master)
                ReturnUserMenu(self.master, self.passer)
                DialogBoxes.account_balance_mgs(temp)
            except tk.TclError:
                DialogBoxes.input_error()
                break
            except ValueError:
                DialogBoxes.input_error()
                break

    def on_submit1(self):
        """Executes when the user selects to remove funds from their savings account.
           It performs error checking to ensure the funds are available."""
        # Get the users account data from the database
        self.c.execute("select amount from customer join accounts join saving_account "
                       "where customer.uid=accounts.uid and accounts.sid="
                       "saving_account.sid and customer.uid = " + self.passer)
        temp = self.c.fetchall()
        temp = int(temp[0][0])
        self.c.execute("select accounts.sid from customer join accounts join "
                       "saving_account where customer.uid=accounts.uid and accounts.sid"
                       "=saving_account.sid and customer.uid = " + self.passer)
        temp2 = self.c.fetchall()
        temp2 = int(temp2[0][0])

        # If the amount to be withdrawn is less then the amount available, withdraw it and update
        # the database.
        valid = False
        while not valid:
            
            try:
                amount = self.opening_balance_text.get()
                if (temp<float(amount)):
                    if ((temp-float(amount))>-200):
                        amount=amount+45
                    else:
                        DialogBoxes.Over_draft_error()
                        break 
                temp -= float(amount)
                valid = True
                self.c.execute("update saving_account set amount = " + str(temp)
                               + " where sid=" + str(temp2))
                self.conn.commit()
                window_cleaner(self.master)
                ReturnUserMenu(self.master, self.passer)
                DialogBoxes.account_balance_mgs(temp)
            except tk.TclError:
                DialogBoxes.input_error()
                break
            except ValueError:
                DialogBoxes.input_error()
                break

    def back_to_splash(self):
        """Destroy current widgets and go back to the Return User Menu."""
        window_cleaner(self.master)
        ReturnUserMenu(self.master, self.passer)


class LoansC(tk.Frame):
    """
    The window where users will be able to get loans
    """

    def __init__(self, master, uid):
        """Initialize the connection with the database and build the TKinter frame.

        :param master The master frame for the GUI
        :param uid The user ID
        """

        # Connect to the database
        self.conn = sqlite3.connect('bank.db')
        self.c = self.conn.cursor()
        self.passer = uid

        # build the frame
        tk.Frame.__init__(self, master)
        self.master.title('Dork\'s Bank - Loans')
        self.master.config(menu=tk.Menu(self.master))

        # Configure the rows and columns
        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_rowconfigure(6, weight=1)
        self.master.grid_columnconfigure(0, weight=1)
        self.master.grid_columnconfigure(6, weight=1)

        # Create the label to get the amount for the loan.
        user_name_l = tk.Label(self.master, text="Amount: ")
        user_name_l.grid(row=1, column=1, sticky='E', pady=5)

        self.opening_balance_text = tk.IntVar()
        opening_balance_entry = tk.Entry(self.master,
                                         textvariable=self.opening_balance_text)
        opening_balance_entry.grid(row=1, column=2)

        # Create the buttons to select from where the money will be taken to pay for the loan.
        submit_button = tk.Button(self.master, text='Pay from Checking',
                                  command=self.on_submit_checking, width=15)
        submit_button.grid(row=1, column=3, padx=4)
        submit_button1 = tk.Button(self.master, text='Pay from Savings',
                                   command=self.on_submit_savings, width=15)
        submit_button1.grid(row=2, column=3, padx=4)

        # Create the back button
        back = tk.Button(self.master, text='Back', command=self.back_to_splash,
                         width=10)
        back.grid(row=3, column=3, padx=4)

        self.master.minsize(800, 600)
        center(self.master.winfo_toplevel())

    def on_submit_checking(self):
        """Executed when the User gets a loan and selects to pay with it from their checking
           account."""
        # TODO comment more here
        p = 1
        t = True
        while p != 0:
            self.c.execute("select lid from accounts where uid = " + self.passer)
            temp = self.c.fetchall()
            temp = (temp[0][0])

            if temp is None:
                DialogBoxes.loan_account_error()
                p = 0
            else:
                self.c.execute("select amount from loan_account where lid=" + str(temp))
                temp1 = self.c.fetchall()
                temp1 = float((temp1[0][0]))

                self.c.execute(
                    "select saving_account.amount from saving_account join accounts where"
                    " accounts.uid=" + self.passer + " and "
                                                     "accounts.sid=saving_account.sid")
                temp2 = self.c.fetchall()
                temp2 = float((temp2[0][0]))

                self.c.execute(
                    "select checking_account.amount from checking_account join accounts where accounts.uid=" +
                    self.passer + " and accounts.cid=checking_account.cid")
                temp3 = self.c.fetchall()
                temp3 = float((temp3[0][0]))

                self.c.execute(
                    "select saving_account.sid from saving_account join accounts where accounts.uid=" +
                    self.passer + " and accounts.sid=saving_account.sid")
                temp22 = self.c.fetchall()
                temp22 = int((temp22[0][0]))

                self.c.execute(
                    "select checking_account.cid from checking_account join accounts where accounts.uid=" +
                    self.passer + " and accounts.cid=checking_account.cid")
                temp33 = self.c.fetchall()
                temp33 = int((temp33[0][0]))
                a = 1
                b = 1

                while a != 0:
                    try:
                        amount = float(self.opening_balance_text.get())
                        if amount > temp1:
                            t = False
                            DialogBoxes.loan_amount_error()
                            a = 0
                        elif amount > temp3:
                            t = False
                            DialogBoxes.loan_checking_error()
                            a = 0
                        else:
                            a = 0
                    except tk.TclError:
                        DialogBoxes.input_error()
                        t=False
                        break

                

                if t:
                    temp1 -= amount
                    temp2 -= amount
                    temp3 -= amount
                    self.c.execute("update checking_account set amount = " + str(temp3)
                                   + " where cid=" + str(temp33))
                    self.c.execute("update loan_account set amount = " + str(temp1)
                                   + " where lid=" + str(temp))
                    self.conn.commit()
                    window_cleaner(self.master)
                    ReturnUserMenu(self.master, self.passer)
                p = 0

    def on_submit_savings(self):
        """Executes when the user selects to pay for a loan with their savings account"""
        # TODO more comments here
        p = 1
        t = True
        while p != 0:
            self.c.execute("select lid from accounts where uid = " + self.username)
            temp = self.c.fetchall()
            temp = (temp[0][0])

            if temp is None:
                DialogBoxes.loan_account_error()
                p = 0
            else:
                self.c.execute("select amount from loan_account where lid=" + str(temp))
                temp1 = self.c.fetchall()
                temp1 = float((temp1[0][0]))

                self.c.execute(
                    "select saving_account.amount from saving_account join accounts "
                    "where accounts.uid=" + self.passer
                    + " and accounts.sid=saving_account.sid")
                temp2 = self.c.fetchall()
                temp2 = float((temp2[0][0]))

                self.c.execute(
                    "select checking_account.amount from checking_account join accounts"
                    " where accounts.uid=" + self.passer + " and "
                                                           "accounts.cid=checking_account.cid")
                temp3 = self.c.fetchall()
                temp3 = float((temp3[0][0]))

                self.c.execute(
                    "select saving_account.sid from saving_account join accounts where "
                    "accounts.uid=" + self.passer
                    + " and accounts.sid=saving_account.sid")
                temp22 = self.c.fetchall()
                temp22 = int((temp22[0][0]))

                self.c.execute(
                    "select checking_account.cid from checking_account join accounts "
                    "where accounts.uid=" + self.passer + " and "
                                                          "accounts.cid=checking_account.cid")
                temp33 = self.c.fetchall()
                temp33 = int((temp33[0][0]))
                a = 1

                while a != 0:
                    try:
                        amount = float(self.opening_balance_text.get())
                        if amount > temp1:
                            t = False
                            DialogBoxes.loan_amount_error()
                            a = 0
                        elif amount > temp3:
                            t = False
                            DialogBoxes.loan_account_error()
                            a = 0
                        else:
                            a = 0
                    except tk.TclError:
                        DialogBoxes.input_error()
                        break

               
                
                if t:
                    temp1 -= amount
                    temp2 -= amount
                    temp3 -= amount
                    self.c.execute("update saving_account set amount = " + str(temp2)
                                   + " where sid=" + str(temp22))
                    self.c.execute("update loan_account set amount = " + str(temp1)
                                   + " where lid=" + str(temp))

                    self.conn.commit()
                    window_cleaner(self.master)
                    ReturnUserMenu(self.master, self.passer)
                p = 0

    def back_to_splash(self):
        """Destroy current widgets and go back to the Return User Menu."""
        window_cleaner(self.master)
        ReturnUserMenu(self.master, self.passer)


class TransferC(tk.Frame):
    """
    The window where Users will be able to transfer funds
    """

    def __init__(self, master, uid):
        """Initializes the connection to the database and builds the Tkinter frame."""
        # Connects to the database
        self.conn = sqlite3.connect('bank.db')
        self.c = self.conn.cursor()
        self.passer = uid

        # Builds the Frame
        tk.Frame.__init__(self, master)
        self.master.title('Dork\'s Bank - Transfers')
        self.master.config(menu=tk.Menu(self.master))

        # Configure the rows and columns
        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_rowconfigure(6, weight=1)
        self.master.grid_columnconfigure(0, weight=1)
        self.master.grid_columnconfigure(6, weight=1)

        # Make the label for the user to enter an amount.
        user_name_l = tk.Label(self.master, text="Amount: ")
        user_name_l.grid(row=1, column=1, sticky='E', pady=5)

        self.opening_balance_text = tk.IntVar()
        opening_balance_entry = tk.Entry(self.master,
                                         textvariable=self.opening_balance_text)
        opening_balance_entry.grid(row=1, column=2)

        # Make a label for the account selection
        user_name_2 = tk.Label(self.master, text="To Account: ")
        user_name_2.grid(row=2, column=1, sticky='E', pady=5)

        self.opening_balance_text2 = tk.IntVar()
        opening_balance_entry = tk.Entry(self.master,
                                         textvariable=self.opening_balance_text2)
        opening_balance_entry.grid(row=2, column=2)

        # Make the buttons to submit for checking and savings.
        submit_button = tk.Button(self.master, text='Submit for Checking',
                                  command=self.on_submit_checking, width=15)
        submit_button.grid(row=1, column=3, padx=4)
        submit_button1 = tk.Button(self.master, text='Submit for Savings',
                                   command=self.on_submit_savings, width=15)
        submit_button1.grid(row=2, column=3, padx=4)

        back = tk.Button(self.master, text='Back', command=self.back_to_splash, width=10)
        back.grid(row=3, column=3, padx=4)

        self.master.minsize(800, 600)
        center(self.master.winfo_toplevel())

    def on_submit_checking(self):
        """Executed when the uses selects to transfer for checking"""
        # TODO Holy snot balls batman, WTF is going on with this one?
        p = 1
        temp = 0
        temp1 = 0

        alpha = 'c'

        self.c.execute(
            "select amount from customer join accounts join checking_account "
            "where customer.uid=accounts.uid and accounts.cid=checking_account.cid "
            "and customer.uid = " + self.passer)
        temp = self.c.fetchall()
        temp = int(temp[0][0])
        self.c.execute(
            "select accounts.cid from customer join accounts join checking_account"
            " where customer.uid=accounts.uid and accounts.cid=checking_account.cid"
            " and customer.uid = " + self.passer)
        temp2 = self.c.fetchall()
        temp2 = int(temp2[0][0])
        p = 0

        t = True
        valid = False
        while not valid:
            try:
                checker = ""
                amount = int(self.opening_balance_text.get())
                n = 0
                l = 0
                while checker == "":
                    accounts = int(self.opening_balance_text2.get())
                    self.c.execute("select * from saving_account where sid="
                                   + str(accounts))
                    q = self.c.fetchall()
                    if len(q) == 1:
                        self.c.execute("select amount from saving_account where sid="
                                       + str(accounts))
                        tempp = self.c.fetchall()
                        tempp = float(tempp[0][0])
                        # print(tempp)
                        checker = 's'
                        l = 0
                    else:
                        l = 1
                    self.c.execute("select * from checking_account where cid="
                                   + str(accounts))
                    p = self.c.fetchall()
                    if len(p) == 1:
                        self.c.execute("select amount from checking_account where cid="
                                       + str(accounts))
                        tempp = self.c.fetchall()
                        tempp = float(tempp[0][0])
                        #print(tempp)
                        checker = 'c'
                        n = 0
                    else:
                        n = 1
                    m = n + l
                    if m == 2:
                        t = False
                        DialogBoxes.no_account_error()
                        break

                valid = True
                if (temp<float(amount)):
                    if ((temp-float(amount))>-200):
                        amount=amount+45
                    else:
                        DialogBoxes.Over_draft_error()
                        break 
                
                temp -= amount

                if t:
                    if checker == 's':
                        self.c.execute("update checking_account set amount = "
                                       + str(temp) + " where cid=" + str(temp2))
                        tempp = amount + tempp
                        self.c.execute(
                            "update saving_account set amount = " + str(tempp)
                            + " where sid=" + str(accounts))

                    if checker == 'c':
                        self.c.execute("update checking_account set amount = "
                                       + str(temp) + " where cid=" + str(temp2))
                        tempp = amount + tempp
                        self.c.execute(
                            "update checking_account set amount = " + str(tempp)
                            + " where cid=" + str(accounts))
                DialogBoxes.account_balance_mgs(temp)
                # self.balupdate()
                if t:
                    self.conn.commit()
                    window_cleaner(self.master)
                    ReturnUserMenu(self.master, self.passer)
                break
            except tk.TclError:
                DialogBoxes.input_error()
                break
            except ValueError:
                DialogBoxes.input_error()
                break

    def on_submit_savings(self):
        """Executes when the user selects the savings account."""
        # TODO yup got nothin.
        p = 1
        temp = 0
        temp1 = 0
        t = True

        alpha = 's'

        self.c.execute(
            "select amount from customer join accounts join saving_account where "
            "customer.uid=accounts.uid and accounts.sid=saving_account.sid and "
            "customer.uid = " + self.passer)
        temp = self.c.fetchall()
        temp = int(temp[0][0])
        self.c.execute(
            "select accounts.sid from customer join accounts join saving_account "
            "where customer.uid=accounts.uid and accounts.sid=saving_account.sid and "
            "customer.uid = " + self.passer)
        temp2 = self.c.fetchall()
        temp2 = int(temp2[0][0])
        p = 0

        valid = False
        while not valid:
            try:
                checker = ""
                amount = float(self.opening_balance_text.get())
                while checker == "":
                    accounts = int(self.opening_balance_text2.get())
                    self.c.execute("select * from saving_account where sid="
                                   + str(accounts))
                    q = self.c.fetchall()
                    if len(q) == 1:
                        self.c.execute("select amount from saving_account where sid="
                                       + str(accounts))
                        tempp = self.c.fetchall()

                        tempp = float(tempp[0][0])
                        print(tempp)
                        checker = 's'
                        l = 0
                    else:
                        l = 1
                    self.c.execute("select * from checking_account where cid="
                                   + str(accounts))
                    p = self.c.fetchall()
                    if len(p) == 1:
                        self.c.execute("select amount from checking_account where cid="
                                       + str(accounts))
                        tempp = self.c.fetchall()
                        tempp = float(tempp[0][0])

                        checker = 'c'
                        n = 0
                    else:
                        n = 1
                    m = n + l
                    if m == 2:
                        t = False
                        print("no account in database")
                        break

                valid = True
                if (temp<float(amount)):
                    if ((temp-float(amount))>-200):
                        amount=amount+45
                    else:
                        DialogBoxes.Over_draft_error()
                        break 
                
                temp -= amount
                if t:
                    if checker == 's':
                        self.c.execute("update saving_account set amount = " + str(temp)
                                       + " where sid=" + str(temp2))
                        tempp = amount + tempp
                        self.c.execute(
                            "update saving_account set amount = " + str(tempp)
                            + " where sid=" + str(accounts))
                    if checker == 'c':
                        self.c.execute("update saving_account set amount = "
                                       + str(temp) + " where sid=" + str(temp2))
                        tempp = amount + tempp
                        self.c.execute(
                            "update checking_account set amount = " + str(tempp)
                            + " where cid=" + str(accounts))
                DialogBoxes.account_balance_mgs(temp)

                if t:
                    self.conn.commit()
                    window_cleaner(self.master)
                    ReturnUserMenu(self.master, self.passer)
            except tk.TclError:
                DialogBoxes.input_error()
                break
            except ValueError:
                DialogBoxes.input_error()
                break

    def back_to_splash(self):
        """Destroy current widgets and reset the display to the Return User Menu."""
        window_cleaner(self.master)
        ReturnUserMenu(self.master, self.passer)


class DepositCashC(tk.Frame):
    """
    The window where Users will be able to deposit funds
    """

    def __init__(self, master, uid):
        """Initialize the connection with the database and build the TKinter Frame."""
        # Connect to the database.
        self.conn = sqlite3.connect('bank.db')
        self.c = self.conn.cursor()
        self.passer = uid

        # Build the frame
        tk.Frame.__init__(self, master)
        self.master.title('Dork\'s Bank - Deposit')
        self.master.config(menu=tk.Menu(self.master))

        # Configure the rows and columns
        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_rowconfigure(6, weight=1)
        self.master.grid_columnconfigure(0, weight=1)
        self.master.grid_columnconfigure(6, weight=1)

        # Create label for the user to enter an amount.
        user_name_l = tk.Label(self.master, text="Amount: ")
        user_name_l.grid(row=1, column=1, sticky='E', pady=5)

        self.opening_balance_text = tk.IntVar()
        opening_balance_entry = tk.Entry(self.master,
                                         textvariable=self.opening_balance_text)
        opening_balance_entry.grid(row=1, column=2)

        # Create buttons for selecting checking account and savings account.
        submit_button = tk.Button(self.master, text='Submit for Checking',
                                  command=self.on_submit_checking, width=15)
        submit_button.grid(row=1, column=3, padx=4)
        submit_button1 = tk.Button(self.master, text='Submit for Savings',
                                   command=self.on_submit_savings, width=15)
        submit_button1.grid(row=2, column=3, padx=4)

        # Create a back button
        back = tk.Button(self.master, text='Back', command=self.back_to_splash, width=10)
        back.grid(row=3, column=3, padx=4)

        self.master.minsize(800, 600)
        center(self.master.winfo_toplevel())

    def on_submit_checking(self):
        """Executed when the user selects to deposit funds into the checking account."""
        # TODO yup more Comments needed
        self.c.execute(
            "select amount from customer join accounts join checking_account where "
            "customer.uid=accounts.uid and accounts.cid=checking_account.cid and "
            "customer.uid = " + self.passer)
        temp = self.c.fetchall()
        temp = int(temp[0][0])
        self.c.execute(
            "select accounts.cid from customer join accounts join checking_account "
            "where customer.uid=accounts.uid and accounts.cid=checking_account.cid and"
            " customer.uid = " + self.passer)
        temp2 = self.c.fetchall()
        temp2 = int(temp2[0][0])
        valid = False
        while not valid:
            try:
                amount = self.opening_balance_text.get()
                temp += float(amount)
                valid = True
                self.c.execute("update checking_account set amount = " + str(temp)
                               + " where cid=" + str(temp2))
                self.conn.commit()
                window_cleaner(self.master)
                ReturnUserMenu(self.master, self.passer)
                DialogBoxes.account_balance_mgs(temp)

            except tk.TclError:
                DialogBoxes.input_error()
                break
            except ValueError:
                DialogBoxes.input_error()
                break

    def on_submit_savings(self):
        """Executed when the user selects to deposit money into a savings account."""
        # TODO more
        self.c.execute(
            "select amount from customer join accounts join saving_account where "
            "customer.uid=accounts.uid and accounts.sid=saving_account.sid and "
            "customer.uid = " + self.passer)
        temp = self.c.fetchall()
        temp = int(temp[0][0])
        self.c.execute(
            "select accounts.sid from customer join accounts join saving_account where"
            " customer.uid=accounts.uid and accounts.sid=saving_account.sid and "
            "customer.uid = " + self.passer)
        temp2 = self.c.fetchall()
        temp2 = int(temp2[0][0])
        valid = False
        while not valid:
            
            try:
                amount = self.opening_balance_text.get()
                temp += float(amount)
                valid = True
                self.c.execute("update saving_account set amount = " + str(temp)
                               + " where sid=" + str(temp2))
                self.conn.commit()
                window_cleaner(self.master)
                ReturnUserMenu(self.master, self.passer)
                DialogBoxes.account_balance_mgs(temp)
            except tk.TclError:
                DialogBoxes.input_error()
                break
            except ValueError:
                DialogBoxes.input_error()
                break

    def back_to_splash(self):
        """Destroys current widgets and returns to the Return user menu."""
        window_cleaner(self.master)
        ReturnUserMenu(self.master, self.passer)


class CheckBalanceC(tk.Frame):
    """
    The window where Users will be able to check their Account balance
    """

    def __init__(self, master, uid):
        """Initializes the connection to the database and builds the TKinter frame.

        :param master THe master GUI frame.
        :param uid The user ID
        """

        # Connect to the database
        self.conn = sqlite3.connect('bank.db')
        self.c = self.conn.cursor()
        self.passer = uid

        # Build the frame
        tk.Frame.__init__(self, master)
        self.master.title('Dork\'s Bank - Balance')
        self.master.config(menu=tk.Menu(self.master))

        # Configure the rows and columns
        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_rowconfigure(6, weight=1)
        self.master.grid_columnconfigure(0, weight=1)
        self.master.grid_columnconfigure(6, weight=1)

        # Get the users account information from the database
        self.c.execute(
            "select amount from customer join accounts join saving_account where "
            "customer.uid=accounts.uid and accounts.sid=saving_account.sid and "
            "customer.uid = " + self.passer)
        temp = self.c.fetchall()

        self.c.execute(
            "select amount from customer join accounts join checking_account where "
            "customer.uid=accounts.uid and accounts.cid=checking_account.cid and "
            "customer.uid = " + self.passer)
        temp1 = self.c.fetchall()

        # Display the users funds in their respective labels.
        password_l = tk.Label(self.master, text="Checking Account: " + str(temp1[0][0]))
        password_l.grid(row=2, column=1, sticky='E', pady=5)
        password_2 = tk.Label(self.master, text="Savings Account: " + str(temp[0][0]))
        password_2.grid(row=3, column=1, sticky='E', pady=5)

        # Create a back button
        back_button = tk.Button(self.master, text='Back', command=self.back_to_splash,
                                width=10)
        back_button.grid(row=6, column=1, pady=5)

        self.master.minsize(800, 600)
        center(self.master.winfo_toplevel())

    def back_to_splash(self):
        """Destroy current widgets and go back to the Return user menu."""
        window_cleaner(self.master)
        ReturnUserMenu(self.master, self.passer)


# noinspection PyClassHasNoInit
class DialogBoxes(tk.Toplevel):
    """
    All needed Error and Help Dialog Boxes will be created in this class.
    """

    @staticmethod
    def password_match_error():
        """Error raised when the two user passwords entered do not match."""
        pme = tk.Toplevel()
        pme.title('Password Error')

        for s in range(3):
            pme.grid_rowconfigure(s, weight=1)
            pme.grid_columnconfigure(s, weight=1)

        msg = tk.Message(pme, text='Passwords do not match.', width=3000)
        msg.grid(row=0, column=0, columnspan=3)
        button = tk.Button(pme, text="Dismiss", command=pme.destroy)
        button.grid(row=1, column=1)
        pme.minsize(300, 150)
        center(pme.winfo_toplevel())

    @staticmethod
    def password_length_error():
        """Error raised when the password is of insufficient length."""
        ple = tk.Toplevel()
        ple.title('Password Length Error')

        for s in range(3):
            ple.grid_rowconfigure(s, weight=1)
            ple.grid_columnconfigure(s, weight=1)

        msg = tk.Message(ple, text='Password must be more than four (4) characters.',
                         width=3000)
        msg.grid(row=0, column=0, columnspan=3)
        button = tk.Button(ple, text="Dismiss", command=ple.destroy)
        button.grid(row=1, column=1)
        ple.minsize(300, 150)
        center(ple.winfo_toplevel())

    def Over_draft_error():
        """Error raised when the password is of insufficient length."""
        ple = tk.Toplevel()
        ple.title('Insufficient funds')

        for s in range(3):
            ple.grid_rowconfigure(s, weight=1)
            ple.grid_columnconfigure(s, weight=1)

        msg = tk.Message(ple, text='Insufficient funds',
                         width=3000)
        msg.grid(row=0, column=0, columnspan=3)
        button = tk.Button(ple, text="Dismiss", command=ple.destroy)
        button.grid(row=1, column=1)
        ple.minsize(300, 150)
        center(ple.winfo_toplevel())

    @staticmethod
    def name_length_error():
        """Error raised when the first or last name of the user is less than 3
        characters."""
        nle = tk.Toplevel()
        nle.title('Name Length Error')

        for s in range(3):
            nle.grid_rowconfigure(s, weight=1)
            nle.grid_columnconfigure(s, weight=1)

        msg = tk.Message(nle, text='First Name and Last Name fields must be longer '
                                   'than three (3) letters.',
                         width=3000)
        msg.grid(row=0, column=0, columnspan=3)
        button = tk.Button(nle, text="Dismiss", command=nle.destroy)
        button.grid(row=1, column=1)
        nle.minsize(300, 150)
        center(nle.winfo_toplevel())

    @staticmethod
    def system_breach_warning():
        """Error raised when Mr. Anderson escapes the Matrix."""
        sbw = tk.Toplevel()
        sbw.title('System Breach')

        for s in range(3):
            sbw.grid_rowconfigure(s, weight=1)
            sbw.grid_columnconfigure(s, weight=1)

        msg = tk.Message(sbw, text='Warning system breach detected system shutting '
                                   'down.', width=3000)
        msg.grid(row=0, column=0, columnspan=3)
        button = tk.Button(sbw, text="Dismiss", command=exit)
        button.grid(row=1, column=1)
        sbw.minsize(300, 150)
        center(sbw.winfo_toplevel())

    @staticmethod
    def empty_field_error():
        """Error raised when a field is left empty."""
        efe = tk.Toplevel()
        efe.title('Empty Field Error')

        for s in range(3):
            efe.grid_rowconfigure(s, weight=1)
            efe.grid_columnconfigure(s, weight=1)

        msg = tk.Message(efe, text='One of the required fields is empty. Check all '
                                   'fields and try again.',
                         width=3000)
        msg.grid(row=0, column=0, columnspan=3)
        button = tk.Button(efe, text="Dismiss", command=efe.destroy)
        button.grid(row=1, column=1)
        efe.minsize(300, 150)
        center(efe.winfo_toplevel())

    @staticmethod
    def opening_balance_error():
        """Error raised when less than $100.00 is attempted to be used to open an
           account."""
        obe = tk.Toplevel()
        obe.title('Opening Balance Error')

        for s in range(3):
            obe.grid_rowconfigure(s, weight=1)
            obe.grid_columnconfigure(s, weight=1)

        msg = tk.Message(obe, text='Opening Balance must be greater than 100.0.',
                         width=3000)
        msg.grid(row=0, column=0, columnspan=3)
        button = tk.Button(obe, text="Dismiss", command=obe.destroy)
        button.grid(row=1, column=1)
        obe.minsize(300, 150)
        center(obe.winfo_toplevel())

    @staticmethod
    def username_password_error():
        """Pop up created when there is a problem with the user name or password being
           entered."""
        obe = tk.Toplevel()
        obe.title('Username/Password Error')

        for s in range(3):
            obe.grid_rowconfigure(s, weight=1)
            obe.grid_columnconfigure(s, weight=1)

        msg = tk.Message(obe, text='Username/Password is not in our system.', width=3000)
        msg.grid(row=0, column=0, columnspan=3)
        button = tk.Button(obe, text="Dismiss", command=obe.destroy)
        button.grid(row=1, column=1)
        obe.minsize(300, 150)
        center(obe.winfo_toplevel())

    @staticmethod
    def account_balance_mgs(temp):
        """Pop up created to display an account balance."""
        abm = tk.Toplevel()
        abm.title('Balance Message')

        for s in range(3):
            abm.grid_rowconfigure(s, weight=1)
            abm.grid_columnconfigure(s, weight=1)

        msg = tk.Message(abm, text='Your new account balance is %.2f' % temp, width=3000)
        msg.grid(row=0, column=0, columnspan=3)
        button = tk.Button(abm, text="Dismiss", command=abm.destroy)
        button.grid(row=1, column=1)
        abm.minsize(300, 150)
        center(abm.winfo_toplevel())

    @staticmethod
    def input_error():
        """Pop up created to warn the user of incorrect data being entered into the
           system."""
        pme = tk.Toplevel()
        pme.title('Input Error')

        for s in range(3):
            pme.grid_rowconfigure(s, weight=1)
            pme.grid_columnconfigure(s, weight=1)

        msg = tk.Message(pme, text='The value/text input into this box is not correct',
                         width=3000)
        msg.grid(row=0, column=0, columnspan=3)
        button = tk.Button(pme, text="Dismiss", command=pme.destroy)
        button.grid(row=1, column=1)
        pme.minsize(300, 150)
        center(pme.winfo_toplevel())

    @staticmethod
    def loan_account_error():
        """Pop up created when a user attempts to access a loan that does not exist."""
        lae = tk.Toplevel()
        lae.title('Loan Account Error')

        for s in range(3):
            lae.grid_rowconfigure(s, weight=1)
            lae.grid_columnconfigure(s, weight=1)

        msg = tk.Message(lae, text='You do not have a Loan Account.', width=3000)
        msg.grid(row=0, column=0, columnspan=3)
        button = tk.Button(lae, text="Dismiss", command=lae.destroy)
        button.grid(row=1, column=1)
        lae.minsize(300, 150)
        center(lae.winfo_toplevel())

    @staticmethod
    def loan_amount_error():
        """Pop up created when a user attempts to enter too large of a value."""
        lam = tk.Toplevel()
        lam.title('Loan Amount Error')

        for s in range(3):
            lam.grid_rowconfigure(s, weight=1)
            lam.grid_columnconfigure(s, weight=1)

        msg = tk.Message(lam, text='Please lower the amount to less than or equal to the'
                                   ' loan amount.', width=3000)
        msg.grid(row=0, column=0, columnspan=3)
        button = tk.Button(lam, text="Dismiss", command=lam.destroy)
        button.grid(row=1, column=1)
        lam.minsize(300, 150)
        center(lam.winfo_toplevel())

    @staticmethod
    def loan_checking_error():
        """Pop up created when a user attempts to pay off a loan from an account with
           insufficient funds."""
        lce = tk.Toplevel()
        lce.title('Loan Checking Error')

        for s in range(3):
            lce.grid_rowconfigure(s, weight=1)
            lce.grid_columnconfigure(s, weight=1)

        msg = tk.Message(lce, text='Please lower the amount to the amount you have in '
                                   'your checking account.',
                         width=3000)
        msg.grid(row=0, column=0, columnspan=3)
        button = tk.Button(lce, text="Dismiss", command=lce.destroy)
        button.grid(row=1, column=1)
        lce.minsize(300, 150)
        center(lce.winfo_toplevel())

    @staticmethod
    def no_account_error():
        """Pop up created when a specified account can not be found in the system."""
        nae = tk.Toplevel()
        nae.title('No Account Error')

        for s in range(3):
            nae.grid_rowconfigure(s, weight=1)
            nae.grid_columnconfigure(s, weight=1)

        msg = tk.Message(nae, text='That Account does not exist in our system.',
                         width=3000)
        msg.grid(row=0, column=0, columnspan=3)
        button = tk.Button(nae, text="Dismiss", command=nae.destroy)
        button.grid(row=1, column=1)
        nae.minsize(300, 150)
        center(nae.winfo_toplevel())

    @staticmethod
    def insufficient_funds_error():
        """Pop up created when a user overdrafts their account."""
        ife = tk.Toplevel()
        ife.title('Insufficient Funds Error')

        for s in range(3):
            ife.grid_rowconfigure(s, weight=1)
            ife.grid_columnconfigure(s, weight=1)

        msg = tk.Message(ife, text='Insufficient funds. Your account has been charged a'
                                   ' $45.00 overdraft fee.',
                         width=3000)
        msg.grid(row=0, column=0, columnspan=3)
        button = tk.Button(ife, text="Dismiss", command=ife.destroy)
        button.grid(row=1, column=1)
        ife.minsize(300, 150)
        center(ife.winfo_toplevel())

    @staticmethod
    def no_active_user_error():
        """Pop up created when there are no active users."""
        naue = tk.Toplevel()
        naue.title('No Active User Error')

        for s in range(3):
            naue.grid_rowconfigure(s, weight=1)
            naue.grid_columnconfigure(s, weight=1)

        msg = tk.Message(naue, text='No Users are active.', width=3000)
        msg.grid(row=0, column=0, columnspan=3)
        button = tk.Button(naue, text="Dismiss", command=naue.destroy)
        button.grid(row=1, column=1)
        naue.minsize(300, 150)
        center(naue.winfo_toplevel())

    @staticmethod
    def try_again_error():
        """Pop up created when the user needs to try again."""
        pme = tk.Toplevel()
        pme.title('Try Again Error')

        for s in range(3):
            pme.grid_rowconfigure(s, weight=1)
            pme.grid_columnconfigure(s, weight=1)

        msg = tk.Message(pme, text='Please try again.', width=3000)
        msg.grid(row=0, column=0, columnspan=3)
        button = tk.Button(pme, text="Dismiss", command=pme.destroy)
        button.grid(row=1, column=1)
        pme.minsize(300, 150)
        center(pme.winfo_toplevel())


def window_cleaner(window):
    """
    Window cleaner function for clearing all widgets and resetting the grid during a
    window change.
    :param window: The master window
    :return: None
    """
    # Destroy all children
    for child in window.winfo_children():
        child.destroy()
    # reset rows and columns
    for x in range(20):
        window.grid_rowconfigure(x, weight=0)
        window.grid_columnconfigure(x, weight=0)


def center(top_level_info):
    """
    Center function for centering the window on screen.
    :param top_level_info: The master window
    :return: None
    """

    top_level_info.update_idletasks()
    w = top_level_info.winfo_screenwidth()
    h = top_level_info.winfo_screenheight()
    size = tuple(int(_) for _ in top_level_info.geometry().split('+')[0].split('x'))
    x = w / 2 - size[0] / 2
    y = h / 2 - size[1] / 2
    top_level_info.geometry("%dx%d+%d+%d" % (size + (x, y)))


if __name__ == '__main__':
    root = tk.Tk()
    app = Splash(root)
    app.mainloop()
