# This file contains information on the client
import helper_functions


class Client:
    """To Represent User Side of Communication"""

    def __init__(self, username, service, method):
        self._username = username
        self._service = service
        self._method = method

        pk_info = helper_functions.get_info("client_private_key")
        self._private_key = int(pk_info['private_key'])

    def send_keyID(self):
        """This method sends keyID information to the server"""

        return self._username

    def decrypt(self,encrypt_message):
        """ Decrypts server encrypted server message and generates a hash value of it

            :param encrypt_message:

            :return: hash value of the server message

        """
        decrypt_message = encrypt_message ^ self._private_key
        return hash(decrypt_message)

    def send_user_id(self):
        """This method sends Username information to the server"""

        return self._username
