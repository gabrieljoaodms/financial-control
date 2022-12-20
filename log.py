"""Inicializa um logger.

Args:

Returns:
"""

from logging.handlers import TimedRotatingFileHandler
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
from datetime import datetime
from pathlib import Path
import pandas as pd
import logging
import os

## DEFINE DIRETORIO/ARQUIVO
dir = os.path.join('data', 'logs')
filename = 'main.log'
Path(dir).mkdir(parents=True, exist_ok=True)
logfile = open(os.path.join(dir, filename), 'a')
logfile.close()

## INSTANCIA OBJETO LOGGER
logger = logging.getLogger(__name__)
handler = TimedRotatingFileHandler(filename=os.path.join(dir, filename), when='h', interval=1)
f_format = logging.Formatter('%(asctime)s %(levelname)s %(filename)s %(funcName)s %(lineno)d %(message)s ')
handler.setFormatter(f_format)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

