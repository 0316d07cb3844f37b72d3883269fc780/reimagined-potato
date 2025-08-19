import logging
from utility.src.string_utils import root_path, create_tag


def make_logger(name, log_file):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    path = root_path("logs\\"+log_file)
    file_handler = logging.FileHandler(path)
    file_handler.setLevel(logging.INFO)
    logger.addHandler(file_handler)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    return logger


def clear_file(file_name):
    try:
        with open(root_path("logs\\"+file_name), "w") as file:
            pass
    except FileNotFoundError:
        pass


client_networker_logger = make_logger("client_logger", "client_network_logs")
server_networker_logger = make_logger("server_logger", "server_network_logs")
client_networker_recieve_only_logger = make_logger("client_recieve_only_logger", "client_network_logs_recieve_only")
client_networker_send_only_logger = make_logger("client_send_only_logger", "client_network_logs_send_only")
server_networker_recieve_only_logger = make_logger("server_recieve_only_logger", "server_network_logs_recieve_only")
server_networker_send_only_logger = make_logger("server_send_only_logger", "server_network_logs_send_only")


def log_to_file(string: str):
    client_networker_logger.info(string)


def clear_all_files():
    clear_file("client_network_logs")
    clear_file("server_network_logs")
    clear_file("client_network_logs_recieve_only")
    clear_file("client_network_logs_send_only")
    clear_file("server_network_logs_recieve_only")
    clear_file("server_network_logs_send_only")


def main():
    clear_all_files()


if __name__ == "__main__":
    main()
