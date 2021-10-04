import logging
import logging as lg

def getLog(name):
    logger = lg.getLogger(name)
    f = open('properties.txt','r')
    if f.mode == 'r':
        loglevel = f.read()
    if loglevel == "ERROR":
        logger.setLevel(logging.ERROR)
    elif loglevel == 'DEBUG':
        logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(name)s:%(message)s')
    file_handler = logging.FileHandler('test.log')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    return logger

def StreamHandler(logger):

    stream_handler = lg.StreamHandler()
    return logger.addHandler(stream_handler)
