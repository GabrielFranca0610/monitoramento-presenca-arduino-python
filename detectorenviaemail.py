import serial                 # Importa biblioteca para comunicação serial (com Arduino)
import time                   # Biblioteca para funções de tempo (sleep, time)
import csv                    # Biblioteca para manipulação de arquivos CSV
from datetime import datetime # Para pegar data e hora atuais formatadas
import smtplib                # Biblioteca para envio de e-mails via SMTP
from email.mime.text import MIMEText           # Para criar corpo do e-mail em texto simples
from email.mime.multipart import MIMEMultipart # Para criar e-mails com múltiplas partes (assunto, texto etc.)

# Configurações da porta serial onde o Arduino está conectado
porta_serial = 'COM4'       # Porta serial (ajuste para a porta correta do seu PC)
baudrate = 9600             # Taxa de transmissão de dados, deve ser igual ao do Arduino
tempo_espera = 90           # Tempo mínimo entre detecções para evitar múltiplos alertas (em segundos)
arquivo_csv = 'registro_movimentos.csv'  # Nome do arquivo CSV onde serão salvos os registros

# Dados do e-mail para envio do alerta
email_origem = 'grupoarduino9879@gmail.com'     # E-mail que envia o alerta (remetente)
senha_email = 'ytpihskplwelvqmj'                # Senha do e-mail (ou app password)
email_destino = 'sensorarduino9879@gmail.com'   # E-mail que vai receber o alerta (destinatário)

# Função para enviar o e-mail de alerta com data e hora da detecção
def enviar_email(data, hora):
    assunto = "Alerta de Presença Detectada"  # Assunto do e-mail
    corpo = f"Uma presença foi detectada no ambiente monitorado em {data} às {hora}."  # Corpo da mensagem

    msg = MIMEMultipart()                      # Cria mensagem multi-partes para o e-mail
    msg['From'] = email_origem                 # Remetente
    msg['To'] = email_destino                   # Destinatário
    msg['Subject'] = assunto                    # Assunto

    msg.attach(MIMEText(corpo, 'plain'))       # Anexa o corpo do e-mail em texto plano

    try:
        servidor = smtplib.SMTP('smtp.gmail.com', 587)  # Conecta ao servidor SMTP do Gmail na porta 587
        servidor.starttls()                              # Inicia TLS para conexão segura
        servidor.login(email_origem, senha_email)       # Faz login com o e-mail e senha
        servidor.send_message(msg)                       # Envia a mensagem
        servidor.quit()                                  # Encerra conexão com o servidor
        print("E-mail enviado com sucesso!")             # Mensagem de sucesso no terminal
    except Exception as e:
        print("Erro ao enviar e-mail:", e)               # Mostra erro se falhar ao enviar e-mail

# Configura conexão serial com Arduino
arduino = serial.Serial(porta_serial, baudrate, timeout=1)  # Abre a porta serial com timeout de 1 segundo
time.sleep(2)                                               # Aguarda 2 segundos para estabilizar a conexão
print("Sistema de monitoramento iniciado...")              # Indica no terminal que o sistema começou

# Abre (ou cria) arquivo CSV para registrar os eventos
with open(arquivo_csv, mode='a', newline='') as f:
    writer = csv.writer(f)
    if f.tell() == 0:                   # Se o arquivo está vazio (posição zero)
        writer.writerow(['Data', 'Hora', 'Status'])  # Escreve cabeçalho das colunas

tempo_ultima_detec = 0                  # Guarda o timestamp da última detecção para controle de tempo

# Loop infinito para ficar lendo dados do Arduino
while True:
    try:
        leitura = arduino.readline().decode('utf-8').strip()  # Lê uma linha da serial, decodifica e limpa espaços
        agora = time.time()                                    # Pega o timestamp atual em segundos desde epoch

        # Se na mensagem lida existe "Movimento detectado" e já passou o tempo de espera
        if "Movimento detectado" in leitura and (agora - tempo_ultima_detec >= tempo_espera):
            data = datetime.now().strftime('%d/%m/%Y')        # Pega data atual formatada dia/mes/ano
            hora = datetime.now().strftime('%H:%M:%S')        # Pega hora atual formatada hora:minuto:segundo

            print(f"[{hora}] Presença detectada!")             # Mostra no terminal o alerta com hora

            # Abre o arquivo CSV no modo append para adicionar nova linha de registro
            with open(arquivo_csv, mode='a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([data, hora, 'Presença detectada'])  # Escreve data, hora e status no CSV

            enviar_email(data, hora)                           # Chama a função para enviar e-mail
            tempo_ultima_detec = agora                          # Atualiza o timestamp da última detecção

    except Exception as e:
        print("Erro:", e)                                     # Caso haja erro na leitura ou no processo, exibe
        break                                                # Encerra o loop e o programa
