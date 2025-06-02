import os
from dotenv import load_dotenv

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()

class Config:
    # Configurações SMTP
    SMTP_SERVER = os.getenv('SMTP_SERVER', 'smtpenvio.combrmail.com.br')
    SMTP_PORT = int(os.getenv('SMTP_PORT', 587))
    SMTP_USER = os.getenv('SMTP_USER', 'naoresponda@envio.grupovaldirsaraiva.com.br')
    SMTP_PASSWORD = os.getenv('SMTP_PASSWORD', 's8Bv7Mh6Jz5Fm@t')
    
    # Configurações Oracle
    ORACLE_HOST = os.getenv('ORACLE_HOST', '10.0.0.243')
    ORACLE_PORT = os.getenv('ORACLE_PORT', '1521')
    ORACLE_SERVICE = os.getenv('ORACLE_SERVICE', 'ORCL')
    ORACLE_USER = os.getenv('ORACLE_USER', 'consinco')
    ORACLE_PASSWORD = os.getenv('ORACLE_PASSWORD', 'c5_4425')
    
    # Diretório de relatórios
    REPORTS_DIR = os.getenv('REPORTS_DIR', os.path.join(os.path.dirname(__file__), 'relatorios'))
    
