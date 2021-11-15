from loguru import logger

logger.remove()
fmt = "<yellow><level>{level: <9}</level></yellow> \
<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> \
msg = <level>{message}</level>  at {time:YYYY-MM-DD HH:mm:ss.SSS}"

logger.add("logs/data/i_know_what_you_did_last_summer.log",
           retention="10 days", rotation="500 mb", format=fmt, level='TRACE')
