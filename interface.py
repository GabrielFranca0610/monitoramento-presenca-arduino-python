import serial
import time
import csv
from datetime import datetime
import tkinter as tk
from tkinter import messagebox

# CONFIGURAÇÕES
porta_serial = 'COM4'
baudrate = 9600
tempo_espera = 90  # segundos
arquivo_csv = 'registro_movimentos.csv'

# SERIAL
arduino = serial.Serial(porta_serial, baudrate, timeout=1)
time.sleep(2)

# VARIÁVEIS
tempo_ultima_detec = 0
ultima_data = "-"
ultima_hora = "-"
status_atual = "Aguardando movimento"

# CSV
with open(arquivo_csv, mode='a', newline='') as f:
    writer = csv.writer(f)
    if f.tell() == 0:
        writer.writerow(['Data', 'Hora', 'Status'])

# FUNÇÕES

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

            # Atualiza CSV
            with open(arquivo_csv, mode='a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([data, hora, 'Presença detectada'])

        elif (time.time() - tempo_ultima_detec) >= tempo_espera:
            status_atual = "Aguardando movimento"

        # Atualiza interface
        status_label.config(text=f"Status: {status_atual}")
        ultima_label.config(text=f"Última detecção: {ultima_data} às {ultima_hora}")

    except Exception as e:
        print("Erro:", e)

    janela.after(500, atualizar_interface)  # repete a cada 500ms

def resetar_tempo():
    global tempo_ultima_detec
    tempo_ultima_detec = time.time()
    messagebox.showinfo("Reset", "Temporizador de detecção foi resetado.")

# INTERFACE TKINTER
janela = tk.Tk()
janela.title("Monitor de Presença")
janela.geometry("350x180")
janela.resizable(False, False)

status_label = tk.Label(janela, text=f"Status: {status_atual}", font=("Arial", 12))
status_label.pack(pady=10)

ultima_label = tk.Label(janela, text=f"Última detecção: {ultima_data} às {ultima_hora}", font=("Arial", 11))
ultima_label.pack(pady=10)

reset_btn = tk.Button(janela, text="Resetar manualmente", command=resetar_tempo, bg="lightblue")
reset_btn.pack(pady=10)

atualizar_interface()
janela.mainloop()
