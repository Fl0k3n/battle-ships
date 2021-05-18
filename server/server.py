from handlers.network_handler import NetworkHandler
from common.communication_handler import CommunicationHandler as CH
from common.msg_codes import ServerCodes


if __name__ == '__main__':
    CH.set_code_wrapper(ServerCodes)
    nh = NetworkHandler()
    nh.listen_for_connections()
