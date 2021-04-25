from handlers.network_handler import NetworkHandler

if __name__ == '__main__':
    nh = NetworkHandler()
    nh.listen_for_connections()
