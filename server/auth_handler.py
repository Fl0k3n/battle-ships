from db_handler import DBHandler
from common.communication_handler import CommunicationHandler as CH
from common.msg_codes import UserCodes
import re
import bcrypt


class AuthHandler:
    def __init__(self, db_handler):
        self.db_handler = db_handler

    def register_user(self, socket, email, password):
        """Tries to register user with given email and password. 
           Sends SUCCESS message on success, and REGISTER_FAILED on failure. 

        Args:
            socket (socket): socket from which request came
            email (string): users email
            password (string): users password in plain text
        """
        validation_errs = self._validate_user_data(email, password)

        if len(validation_errs) > 0:
            CH.send_msg(socket, UserCodes.REGISTER_FAILED,
                        "\n".join(validation_errs))
            return

        hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

        try:
            self.db_handler.save_user(email, hashed)
            print(f'registered {email} -{password}-')
        except Exception as e:  # TODO
            print(e)
            CH.send_msg(socket, UserCodes.REGISTER_FAILED,
                        '500 Internal Server Error')
            return

        CH.send_msg(socket, UserCodes.SUCCESS, '')

    def _validate_user_data(self, email, password):
        # basic validation should also be present on client side
        err_msgs = []

        if len(password) < 6:
            err_msgs.append('password must be at least 6 characters long')

        if not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            err_msgs.append('unsupported email format')

        if self.db_handler.find_user(email) is not None:
            err_msgs.append('email is already taken')

        return err_msgs

    def login_user(self, socket, email, password):
        """Tries to login user with given email and password.
           Sends SUCCESS message on success, and LOGIN_FAILED on failure. 

        Args:
            socket (socket): socket from which request came
            email (string): users email
            password (string): users password in plain text
        """
        user = self.db_handler.find_user(email)
        err_msg = 'Wrong email or password'
        print(email, password)

        if user is None:
            CH.send_msg(socket, UserCodes.LOGIN_FAILED, err_msg)
            return

        correct_password = user['password']

        if bcrypt.checkpw(password.encode(), correct_password):
            print('match')
            CH.send_msg(socket, UserCodes.SUCCESS, '')
        else:
            print('dismatch')
            CH.send_msg(socket, UserCodes.LOGIN_FAILED, err_msg)

        # TODO notify object controlling users
