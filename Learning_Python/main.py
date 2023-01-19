# This is the main file which will be the interface for SSH communication

import random
import helper_functions

from user import *
from server import *

auth_tries = 3  # number of tries for authentication


def new_user():
    """ Description:
            This method finds where it is a user who is logging in

        Returns:
            It returns a bool value for the user choice
    """
    print("Welcome!!\n"
          "Are you a new User?\n"
          "1. Yes\n"
          "Enter any key for No")
    answer = input()
    return answer == '1'


def register_private_key():
    """ Description:
            This method generates and registers user keyID and private key for login
    """
    keys = helper_functions.get_info("info_keys").keys()
    print("Enter User Details: ")
    while True:
        print("Please enter a new keyID")
        keyID = input()
        if keyID in keys:
            print("KeyID already exists. Try again with a different one\n")
        else:
            break
    new_private_key = random.randint(1000000, 9999999)
    helper_functions.add_info("info_keys", keyID, new_private_key,'a')
    helper_functions.add_info("client_private_key", keyID, new_private_key,'wt')
    print("Successfully registered New User!")
    return


def register_password():
    """ Description:
            This method registers username and password of the new user
    """
    usernames = helper_functions.get_info("info_passwords").keys()
    print("Enter User Details: ")
    while True:
        print("Please enter a new Username")
        userID = input()
        if userID in usernames:
            print("UserID already exists. Try again with a different one\n")
        else:
            break
    print("Please Enter your new password")
    new_password = input()
    helper_functions.add_info("info_passwords", userID, new_password, 'a')
    print("Successfully Registered New User")
    return


def user_login_choice():
    """ Description:
            This method takes input of the user login choice

        Return:
             str object of user login choice
    """
    while True:
        print("Please select your method of user login:\n"
              "1. Using public key\n"
              "2. Using password")
        login_choice = input()
        if login_choice not in ('1','2'):
            print("Incorrect User Login Method\n"
                  "Try again")
        else:
            break

    return login_choice


def fetch_user_details():
    """ Description:
            This method takes input of the username, service and login method choice of the user

            Return:
                 str objects of username, service and login methods
    """
    print("Please enter Key ID or Username")
    username = input()

    print("Which service do you want to use: Enter 'A' or 'B' ")
    while True:
        service = input()
        if service in ("A", "B"):
            break
        else:
            print("Incorrect service code\n"
                  "Please re-enter either 'A' or 'B'")

    print("Please mention the login method\n"
          "1. Login using Public Key\n"
          "2. Login using Password")
    while True:
        method = input()
        if method in ("1", "2"):
            break
        else:
            print("Incorrect method \n"
                  "Please re-enter either '1' or '2'")

    return username, service, method


def create_session(username, service, method):
    """ Description:
            This method creates a new session of user/server interaction

        Args:
            username : str object - UserID / KeyID
            service : str object - 'A' / 'B'
            method : str object - '1' /'2'

        Return:
            Objects of client class and server class

    """
    new_client = Client(username, service, method)
    new_server = Server(method)
    return new_client, new_server


def pka_login(client, server):
    """ Description:
            This method stimulates the interaction between client and server during PKA login

        Args:
            client : Client object
            server : Server object

        Return:
            Bool value for successful authentication
    """
    keyID_message = client.send_keyID()
    keyID_verification, encrypt_message = server.verify_keyID(keyID_message)
    if not keyID_verification:
        print("The KeyID does not exists")
        return False
    hash_value = client.decrypt(encrypt_message)
    return server.hash_verify(hash_value)


def password_login(client, server):
    """ Description:
            This method stimulates the interaction between client and server during Password login

        Args:
            client : Client object
            server : Server object

        Return:
            Bool value for successful authentication
    """
    user_id = client.send_user_id()
    user_id_verification = server.verify_user_id(user_id)
    if not user_id_verification:
        print("Username does not exists")
        return False
    print("Please Enter Your Password")
    password = input()
    return server.verify_password(user_id, password)


def main():
    """ Description:
            This function controls flow of the entire SSH_Protocol simulation

    """
    global auth_tries

    if new_user():
        login_choice = user_login_choice()
        if login_choice == '1':
            register_private_key()
        else:
            register_password()
        return

    while auth_tries > 0:
        username, service, method = fetch_user_details()

        client, server = create_session(username, service, method)

        if method == '1':
            log_method = pka_login(client, server)
        else:
            log_method = password_login(client, server)

        if log_method:
            break
        else:
            auth_tries -= 1
            if auth_tries != 0:
                print("Authentication Failed. Incorrect information. Please try again")

    if auth_tries > 0:
        print("Now you can access service {}".format(service))
    else:
        print("You have reached the maximum tries to log into the service. Try again later")

    return


if __name__ == "__main__":
    main()
