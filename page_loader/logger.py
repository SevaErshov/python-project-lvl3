import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class InternalError(Exception):
    pass
