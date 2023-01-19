# this module contains information for authentication by server
import random
import helper_functions

_new_message = None


class Server:
    """To Represent Server Side of Communication"""
    def __init__(self,method):
        if method == '1':
            self._keyID = helper_functions.get_info("info_keys")
            self._keyID = {key: int(value) for key, value in self._keyID.items()}
        else:
            self._password = helper_functions.get_info("info_passwords")

    def verify_keyID(self,key_message):
        """ Verifies where the user entered keyID exists or not
        :param
            str obj: Contains information on keyID
        :return:
            Bool obj: Whether KeyID exists or not
            int obj : Contains encrypted message from server side
        """
        global _new_message
        if key_message not in self._keyID.keys():
            return False, -1
        _new_message = random.randint(10000,10000000)
        encrypt_message = _new_message ^ self._keyID[key_message]
        return True, encrypt_message

    def hash_verify(self,hash_value):
        """ Verifies hash value sent by the user
        :param
            int obj: Accepts a hash value from the client
        :return:
            bool obj : Where user is allowed access or not
        """
        global _new_message
        return hash_value == hash(_new_message)

    def verify_user_id(self,user_id):
        """ Verifies where the client entered userID exists or not
            :param
                str obj: Contains userID
            :return:
                bool obj: Whether KeyID exists or not
                int obj : Contains encrypted message from server side
        """
        return user_id in self._password.keys()

    def verify_password(self,user_id, password):
        """ Verifies hash value sent by the user
            :param
                str obj: Accepts username from the client
                str obj: Accepts password from the client
            :return:
                bool obj : Where user is allowed access or not
        """
        return self._password[user_id] == password
