import serial
import time
import csv
from datetime import datetime
import tkinter as tk
from tkinter import messagebox
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# CONFIGURAÇÕES GERAIS
porta_serial = 'COM4'  
baudrate = 9600
tempo_espera = 90
arquivo_csv = 'registro_movimentos.csv'

# CONFIGURAÇÕES DE EMAIL
email_origem = 'grupoarduino9879@gmail.com'            
senha_email = 'ytpihskplwelvqmj'                
email_destino = 'sensorarduino9879@gmail.com'           

# CONECTA COM ARDUINO
arduino = serial.Serial(porta_serial, baudrate, timeout=1)
time.sleep(2)

# VARIÁVEIS GLOBAIS
tempo_ultima_detec = 0
ultima_data = "-"
ultima_hora = "-"
status_atual = "Aguardando movimento"

# INICIALIZAÇÃO DO CSV
with open(arquivo_csv, mode='a', newline='') as f:
    writer = csv.writer(f)
    if f.tell() == 0:
        writer.writerow(['Data', 'Hora', 'Status'])

# FUNÇÃO: Enviar E-mail
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

# FUNÇÃO PRINCIPAL: Atualizar interface e checar sensor
def atualizar_interface():
    global tempo_ultima_detec, ultima_data, ultima_hora, status_atual

    try:
        leitura = arduino.readline().decode('utf-8').strip()
        agora = time.time()

        if "Movimento detectado" in leitura and (agora - tempo_ultima_detec >= tempo_espera):
            tempo_ultima_detec = agora
            data = datetime.now().strftime('%d/%m/%Y')
            hora = datetime.now().strftime('%H:%M:%S')
            ultima_data = data
            ultima_hora = hora
            status_atual = "Movimento detectado!"

            # Mostra no terminal
            print(f"[{data} {hora}] Presença detectada!")

            # Atualiza CSV
            with open(arquivo_csv, mode='a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([data, hora, 'Presença detectada'])

            # Envia e-mail
            enviar_email(data, hora)

        elif (time.time() - tempo_ultima_detec) >= tempo_espera:
            status_atual = "Aguardando movimento"

        # Atualiza Interface
        status_label.config(text=f"Status: {status_atual}")
        ultima_label.config(text=f"Última detecção: {ultima_data} às {ultima_hora}")

    except Exception as e:
        print("Erro:", e)

    janela.after(500, atualizar_interface)

# FUNÇÃO RESET
def resetar_tempo():
    global tempo_ultima_detec
    tempo_ultima_detec = time.time()
    messagebox.showinfo("Reset", "Temporizador de detecção foi resetado.")

# INTERFACE TKINTER
janela = tk.Tk()
janela.title("Monitor de Presença com E-mail")
janela.geometry("380x200")
janela.resizable(False, False)

status_label = tk.Label(janela, text=f"Status: {status_atual}", font=("Arial", 12))
status_label.pack(pady=10)

ultima_label = tk.Label(janela, text=f"Última detecção: {ultima_data} às {ultima_hora}", font=("Arial", 11))
ultima_label.pack(pady=10)

reset_btn = tk.Button(janela, text="Resetar manualmente", command=resetar_tempo, bg="lightblue")
reset_btn.pack(pady=10)

atualizar_interface()
janela.mainloop()
