import os
import re
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from flask import Flask, render_template, request, flash
import cx_Oracle
from config import Config

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta_aqui'
app.config.from_object(Config)

# Configuração do Oracle
ORACLE_CONN_STR = f"{Config.ORACLE_USER}/{Config.ORACLE_PASSWORD}@{Config.ORACLE_HOST}:{Config.ORACLE_PORT}/{Config.ORACLE_SERVICE}"

def get_representantes_from_db():
    """Obtém a lista de representantes e emails do banco Oracle"""
    try:
        connection = cx_Oracle.connect(ORACLE_CONN_STR)
        cursor = connection.cursor()
        
        cursor.execute("SELECT nrorepresentante, email, nome FROM git_rca_relatorio ORDER BY nrorepresentante")
        results = cursor.fetchall()
        
        representantes = []
        for row in results:
            representantes.append({
                'codigo': str(row[0]),
                'email': row[1],
                'nome': row[2] if len(row) > 2 else f"Representante {row[0]}"
            })
        
        cursor.close()
        connection.close()
        
        return representantes
    except cx_Oracle.DatabaseError as e:
        print(f"Erro ao conectar ao Oracle: {e}")
        return []

def find_pdf_files(directory):
    """Encontra todos os arquivos PDF no diretório especificado e mapeia códigos"""
    pdf_codes = set()
    for filename in os.listdir(directory):
        if filename.lower().endswith('.pdf'):
            code = extract_representante_code(filename)
            if code:
                pdf_codes.add(code)
    return pdf_codes

def extract_representante_code(filename):
    """Extrai o código do representante do nome do arquivo"""
    match = re.search(r'\((\d+)\)\.pdf$', filename, re.IGNORECASE)
    if match:
        return match.group(1)
    return None

def send_email(to_email, subject, body, attachment_path):
    """Envia email com anexo via SMTP"""
    msg = MIMEMultipart()
    msg['From'] = app.config['SMTP_USER']
    msg['To'] = to_email
    msg['Subject'] = subject
    
    msg.attach(MIMEText(body, 'plain'))
    
    with open(attachment_path, 'rb') as f:
        attach = MIMEApplication(f.read(), _subtype="pdf")
        attach.add_header('Content-Disposition', 'attachment', filename=os.path.basename(attachment_path))
        msg.attach(attach)
    
    try:
        with smtplib.SMTP(app.config['SMTP_SERVER'], app.config['SMTP_PORT']) as server:
            server.starttls()
            server.login(app.config['SMTP_USER'], app.config['SMTP_PASSWORD'])
            server.send_message(msg)
        return True
    except Exception as e:
        print(f"Erro ao enviar email: {e}")
        return False

@app.route('/', methods=['GET', 'POST'])
def index():
    # Obter representantes do banco de dados
    representantes = get_representantes_from_db()
    
    # Obter códigos de PDFs disponíveis
    reports_dir = app.config['REPORTS_DIR']
    pdf_codes = set()
    if os.path.exists(reports_dir):
        pdf_codes = find_pdf_files(reports_dir)
    
    # Preparar dados para a tabela
    table_data = []
    for rep in representantes:
        has_pdf = rep['codigo'] in pdf_codes
        table_data.append({
            'codigo': rep['codigo'],
            'nome': rep['nome'],
            'email': rep['email'],
            'has_pdf': has_pdf,
            'pdf_status': '✔' if has_pdf else '✖',
            'status_class': 'success' if has_pdf else 'error'
        })
    
    if request.method == 'POST':
        if not representantes:
            flash("Nenhum representante encontrado no banco de dados!", 'error')
            return render_template('index.html', table_data=table_data)
        
        if not os.path.exists(reports_dir):
            flash(f"Diretório de relatórios não encontrado: {reports_dir}", 'error')
            return render_template('index.html', table_data=table_data)
        
        success_count = 0
        fail_count = 0
        
        for rep in representantes:
            if not rep['has_pdf']:
                print(f"PDF não encontrado para o representante {rep['codigo']}")
                fail_count += 1
                continue
            
            if not rep['email']:
                print(f"Email não encontrado para o representante {rep['codigo']}")
                fail_count += 1
                continue
            
            # Preparar email
            subject = "Relatório Gerencial - Atacados"
            body = f"Prezado {rep['nome']},\n\nSegue em anexo seu relatório gerencial.\n\nAtenciosamente,\nEquipe de Relatórios"
            pdf_filename = f"Painel Gerencial Atacados ({rep['codigo']}).pdf"
            file_path = os.path.join(reports_dir, pdf_filename)
            
            # Enviar email
            if send_email(rep['email'], subject, body, file_path):
                print(f"Email enviado com sucesso para {rep['email']} (Representante {rep['codigo']})")
                success_count += 1
            else:
                print(f"Falha ao enviar email para {rep['email']} (Representante {rep['codigo']})")
                fail_count += 1
        
        flash(f"Processo concluído! Sucessos: {success_count}, Falhas: {fail_count}", 'info')
    
    return render_template('index.html', table_data=table_data)

if __name__ == '__main__':
    app.run(debug=True)