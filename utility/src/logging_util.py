import logging
from utility.src.string_utils import root_path


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


client_networker_logger = make_logger("client_logger", "client_network_logs")


def log_to_file(string: str):
    client_networker_logger.info(string)
