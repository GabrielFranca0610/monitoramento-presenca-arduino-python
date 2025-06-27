import serial
import time
import csv
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


porta_serial = 'COM4'
baudrate = 9600
tempo_espera = 90
arquivo_csv = 'registro_movimentos.csv'


email_origem = 'grupoarduino9879@gmail.com'          
senha_email = 'ytpihskplwelvqmj'              
email_destino = 'sensorarduino9879@gmail.com'      

def enviar_email(data, hora):
    assunto = "Alerta de Presença Detectada"
    corpo = f"Uma presença foi detectada no ambiente monitorado em {data} às {hora}."

    msg = MIMEMultipart()
    msg['From'] = email_origem
    msg['To'] = email_destino
    msg['Subject'] = assunto

    msg.attach(MIMEText(corpo, 'plain'))

    try:
        servidor = smtplib.SMTP('smtp.gmail.com', 587)
        servidor.starttls()
        servidor.login(email_origem, senha_email)
        servidor.send_message(msg)
        servidor.quit()
        print("E-mail enviado com sucesso!")
    except Exception as e:
        print("Erro ao enviar e-mail:", e)


arduino = serial.Serial(porta_serial, baudrate, timeout=1)
time.sleep(2)
print("Sistema de monitoramento iniciado...")


with open(arquivo_csv, mode='a', newline='') as f:
    writer = csv.writer(f)
    if f.tell() == 0:
        writer.writerow(['Data', 'Hora', 'Status'])

tempo_ultima_detec = 0


while True:
    try:
        leitura = arduino.readline().decode('utf-8').strip()
        agora = time.time()

        if "Movimento detectado" in leitura and (agora - tempo_ultima_detec >= tempo_espera):
            data = datetime.now().strftime('%d/%m/%Y')
            hora = datetime.now().strftime('%H:%M:%S')

            print(f"[{hora}] Presença detectada!")

            with open(arquivo_csv, mode='a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([data, hora, 'Presença detectada'])

            enviar_email(data, hora)
            tempo_ultima_detec = agora

    except Exception as e:
        print("Erro:", e)
        break
