'''Centralized general configurations for the logs'''
import logging

# Logging Configuration
LOG_FORMAT = "%(asctime)-24s [%(filename)s:%(lineno)d] \
    %(levelname)-6s %(message)s"
logging.basicConfig(filename='../logs/scraper.log',
                    filemode='a',
                    format=LOG_FORMAT,
                    level=logging.DEBUG)