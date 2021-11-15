import sys
from loguru import logger

logger.remove()
fmt = "<yellow><level>{level: <9}</level></yellow>\
       <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan>  \
       msg = <level>{message}</level>  at {time:YYYY-MM-DD HH:mm:ss.SSS}"
logger.add(sys.stderr, format=fmt, level='TRACE')
