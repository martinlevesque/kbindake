import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,  # Or DEBUG for more detail
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


def info(message: str):
    logging.getLogger(__name__).info(message)


def error(message: str):
    logging.getLogger(__name__).error(message)

def warning(message: str):
    logging.getLogger(__name__).warning(message)
