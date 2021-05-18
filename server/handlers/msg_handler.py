import threading
from observers.connection_observer import ConnectionObserver
from common.communication_handler import CommunicationHandler as CH
from common.msg_codes import ServerCodes, UserCodes
from common.msg_received_observer import MsgReceivedObserver


class MsgHandler(ConnectionObserver, MsgReceivedObserver):
    def __init__(self, auth_handler, room_handler, login_observers):
        self.auth_handler = auth_handler
        self.room_handler = room_handler
        self.login_observers = login_observers

        self.handlers = {
            ServerCodes.REGISTER: self.on_register,
            ServerCodes.LOGIN: self.on_login,
            ServerCodes.CREATE_ROOM: self.on_create_room,
            ServerCodes.GET_ROOMS: self.on_get_rooms,
            ServerCodes.JOIN_ROOM: self.on_join_room,
        }

    def on_connected(self, socket):
        threading.Thread(target=CH.listen_for_messages,
                         args=(socket, self)).start()

    def on_disconnected(self, socket):
        print('disconnected!')
        for login_observer in self.login_observers:
            login_observer.on_logout(socket)

        socket.close()

    def on_msg_received(self, socket, msg):
        code = msg['code']
        data = msg['data']

        # should be handled differently
        if code == ServerCodes.DISCONNECTED:
            self.on_disconnected(socket)
        else:
            self.handlers[code](socket, data)

    def on_register(self, socket, data):
        """Sends REGISTER_SUCCESS message on success and REGISTER_FAILED on failure.
        """
        self.auth_handler.register_user(
            socket, data['email'], data['password'], data)

    def on_login(self, socket, data):
        """Sends LOGIN_SUCCESS message on success and LOGIN_FAILED on failure.
        """
        self.auth_handler.login_user(
            socket, data['email'], data['password'], data)

    def on_create_room(self, socket, data):
        """Sends ROOM_CREATED on success and ERROR on failure.
        """
        try:
            idx = self.room_handler.create_room(socket)
            CH.send_msg(socket, UserCodes.ROOM_CREATED, {'room_id': idx})
        except AttributeError as ae:
            print(ae)
            CH.send_msg(socket, UserCodes.ERROR, str(ae))

    def on_get_rooms(self, socket, data):
        """Sends ROOMS_FETCHED on success.
        """
        rooms = self.room_handler.get_rooms()
        response = [room.get_formatted_data() for room in rooms]
        CH.send_msg(socket, UserCodes.ROOMS_FETCHED, response)

    def on_join_room(self, socket, data):
        """Sends JOINED_ROOM to guest and GUEST_JOINED_ROOM to owner on success
           and ERROR to guest on failure.
        """
        room_id = data['room_id']
        try:
            owner_socket, guest_email = self.room_handler.join_room(
                socket, room_id)
            CH.send_msg(socket, UserCodes.JOINED_ROOM,
                        {'email': guest_email})
            CH.send_msg(owner_socket, UserCodes.GUEST_JOINED_ROOM,
                        {'room_id': room_id})
        except AttributeError as ae:
            print(ae)
            CH.send_msg(socket, UserCodes.ERROR, str(ae))
