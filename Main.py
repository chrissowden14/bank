import NewCustomer
import ReturnCustomer

############################################
# Main file for bank account

WELCOME_MESSAGE = "Welcome to Dorks Bank, We care about you!" + "\n"


def main():
    print(WELCOME_MESSAGE)
    prompts = {
        1: NewCustomer.NewCustomer,  # Creates a new customer profile
        2: ReturnCustomer.ReturnCustomer,  # Checks for existing customer
        3: exit
    }
    while True:
        prompt = int(input("To open a new bank account - Press 1:" + "\n"
                           "To access your existing account - Press 2:\n"
                           "To Exit - Press 3:\n"))
        if prompt in prompts:
            prompts[prompt]()
        else:
            print("You have pressed the wrong key, please try again\n")


main()
