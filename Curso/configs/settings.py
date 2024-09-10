import os

USER = os.getenv('DB_USER', 'sa')
PASSWORD = os.getenv('DB_PASSWORD', 'Abc*123')
HOST = os.getenv('DB_HOST', '192.168.254.1')
DATABASE = os.getenv('DB_NAME', 'ALTERDATA')

# Configuração da conexão
connection_string = f'mssql+pymssql://{USER}:{PASSWORD}@{HOST}/{DATABASE}'
