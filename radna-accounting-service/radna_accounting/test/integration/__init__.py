import logging
from ...configs.initialize import initialize
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

initialize()