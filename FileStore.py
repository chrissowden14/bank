class FileStore:
    def __init__(self):
        # This creates an open list everytime the program is opened
        self.cusnames = []
        self.cusspaswords = []
        self.cusbalance = []

        # opening the stored file that collects the old data from customer
        self.namefile = open("cusnamesfile.txt", "r")
        self.passfile = open("cuspassfile.txt", "r")
        self.balancefile = open("cusbalancefile.txt", "r")

        # this will input the date into the empty list from the stored FileExistsError
        for line in self.namefile:
            self.cusnames.append(line[:-1])
        self.namefile.close()

        # check the list of customers passwords
        for line in self.passfile:
            self.cusspaswords.append(line[:-1])
        self.passfile.close()

        # checks customer balance
        for line in self.balancefile:
            self.cusbalance.append(line[:-1])
        self.balancefile.close()

    # this function will write new date into stored files when its called up
    def filewrite(self, item):
        if item == self.cusnames:
            text = open("cusnamesfile.txt", "w")
            for i in item:
                text.write(i + "\n")
            text.close()

        elif item == self.cusspaswords:
            text = open("cuspassfile.txt", "w")
            for i in item:
                text.write(i + "\n")
            text.close()

        elif item == self.cusbalance:
            text = open("cusbalancefile.txt", "w")
            for i in item:
                text.write(str(i) + "\n")
            text.close()
