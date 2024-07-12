from configs.settings import USER, PASSWORD, HOST, DATABASE, connection_string

import flet as ft
import pandas as pd
from pandas import to_datetime
from datetime import datetime
import json
from urllib.parse import quote
import os
import shutil

# Definir a localização como "Português do Brasil"
import locale
locale.setlocale(locale.LC_ALL, 'pt_BR.utf8')

from sqlalchemy import create_engine, text, Column, update, insert, select, and_, distinct, func
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm import Session


# Conecta a máquina para consultar minhas queries.
engine = create_engine(connection_string)

# Criar uma sessão
Session = sessionmaker(bind=engine)
session = Session()

# Função para formatar a data atual
def format_current_date():
    data = datetime.now()
    return data.strftime('%Y-%m-%d 00:00:00.000')

# Data formatada
data_formatada = format_current_date()
