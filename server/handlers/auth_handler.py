from handlers.db_handler import DBHandler
from common.communication_handler import CommunicationHandler as CH
from common.msg_codes import UserCodes
import re
import bcrypt
from mongoengine.errors import ValidationError


class AuthHandler:
    def __init__(self, db_handler, user_handler, login_observers):
        self.db_handler = db_handler
        self.user_handler = user_handler
        self.login_observers = login_observers

    def register_user(self, socket, email, password, request_msg):
        """Tries to register user with given email and password.
           Sends REGISTER_SUCCESS message on success, and REGISTER_FAILED on failure.

        Args:
            socket (socket): socket from which request came
            email (string): users email
            password (string): users password in plain text
            request_msg (any): original request message
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
            CH.send_msg(socket, UserCodes.REGISTER_SUCCESS, request_msg)
        except ValidationError as ve:
            print(ve)
            CH.send_msg(socket, UserCodes.REGISTER_FAILED,
                        'unsupported email format')
        except Exception as e:
            print(e)
            CH.send_msg(socket, UserCodes.REGISTER_FAILED,
                        '500 Internal Server Error')

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

    def login_user(self, socket, email, password, request_msg):
        """Tries to login user with given email and password.
           Sends LOGIN_SUCCESS message on success, and LOGIN_FAILED on failure.

        Args:
            socket (socket): socket from which request came
            email (string): users email
            password (string): users password in plain text
        """

        if self.user_handler.is_logged_in(email):
            CH.send_msg(socket, UserCodes.LOGIN_FAILED,
                        f'User {email} is already logged in.')
            return

        user = self.db_handler.find_user(email)
        err_msg = 'Wrong email or password'

        if user is None:
            CH.send_msg(socket, UserCodes.LOGIN_FAILED, err_msg)
            return

        if bcrypt.checkpw(password.encode(), user.password):
            # logged in
            for login_observer in self.login_observers:
                login_observer.on_login(socket, user)

            CH.send_msg(socket, UserCodes.LOGIN_SUCCESS, request_msg)
        else:
            CH.send_msg(socket, UserCodes.LOGIN_FAILED, err_msg)
