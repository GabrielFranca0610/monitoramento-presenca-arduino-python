# === BIBLIOTECAS NECESSÁRIAS ===
import serial                        # Para comunicação com o Arduino via porta serial
import time                          # Para manipulação de tempo (delays e marcação)
import csv                           # Para criar e escrever em arquivos CSV
from datetime import datetime        # Para capturar data e hora atual
import tkinter as tk                 # Para criar interface gráfica
from tkinter import messagebox       # Para exibir janelas de alerta (pop-up)

# === CONFIGURAÇÕES DE COMUNICAÇÃO E ARQUIVOS ===
porta_serial = 'COM4'                # Porta onde o Arduino está conectado (verifique no Gerenciador de Dispositivos)
baudrate = 9600                      # Velocidade de transmissão (deve ser igual ao definido no código do Arduino)
tempo_espera = 90                    # Tempo mínimo entre detecções (em segundos)
arquivo_csv = 'registro_movimentos.csv'  # Nome do arquivo onde será salvo o histórico

# === INICIALIZA A COMUNICAÇÃO COM O ARDUINO ===
arduino = serial.Serial(porta_serial, baudrate, timeout=1)  # Abre conexão serial com o Arduino
time.sleep(2)                                                # Aguarda 2 segundos para estabilizar

# === VARIÁVEIS GLOBAIS DO SISTEMA ===
tempo_ultima_detec = 0               # Armazena o tempo da última detecção
ultima_data = "-"                    # Data da última detecção
ultima_hora = "-"                    # Hora da última detecção
status_atual = "Aguardando movimento"  # Status inicial mostrado na interface

# === CRIA O ARQUIVO CSV (SE NÃO EXISTIR) E ESCREVE CABEÇALHO ===
with open(arquivo_csv, mode='a', newline='') as f:
    writer = csv.writer(f)           # Cria um objeto para escrever no CSV
    if f.tell() == 0:                # Se o arquivo estiver vazio...
        writer.writerow(['Data', 'Hora', 'Status'])  # Escreve o cabeçalho

# === FUNÇÃO PRINCIPAL: LÊ O SENSOR E ATUALIZA INTERFACE ===
def atualizar_interface():
    global tempo_ultima_detec, ultima_data, ultima_hora, status_atual

    try:
        leitura = arduino.readline().decode('utf-8').strip()  # Lê linha da serial, decodifica e remove espaços
        agora = time.time()                                   # Tempo atual em segundos

        # Se detectou movimento e passou o tempo de espera desde a última detecção
        if "Movimento detectado" in leitura and (agora - tempo_ultima_detec >= tempo_espera):
            tempo_ultima_detec = agora                          # Atualiza o tempo da última detecção
            data = datetime.now().strftime('%d/%m/%Y')          # Data atual formatada
            hora = datetime.now().strftime('%H:%M:%S')          # Hora atual formatada
            ultima_data = data                                  # Atualiza variável global com a nova data
            ultima_hora = hora                                  # Atualiza variável global com a nova hora
            status_atual = "Movimento detectado!"               # Atualiza o status

            # Grava o evento no CSV
            with open(arquivo_csv, mode='a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([data, hora, 'Presença detectada'])

        # Se passou o tempo de espera sem nova detecção, volta a aguardar
        elif (time.time() - tempo_ultima_detec) >= tempo_espera:
            status_atual = "Aguardando movimento"

        # Atualiza os elementos da interface gráfica
        status_label.config(text=f"Status: {status_atual}")
        ultima_label.config(text=f"Última detecção: {ultima_data} às {ultima_hora}")

    except Exception as e:
        print("Erro:", e)  # Em caso de erro, imprime a mensagem no terminal

    janela.after(500, atualizar_interface)  # Agenda nova verificação a cada 500 milissegundos (0,5 segundos)

# === FUNÇÃO PARA RESETAR MANUALMENTE O TEMPORIZADOR ===
def resetar_tempo():
    global tempo_ultima_detec
    tempo_ultima_detec = time.time()  # Reinicia o contador
    messagebox.showinfo("Reset", "Temporizador de detecção foi resetado.")  # Mostra janela de confirmação

# === CRIAÇÃO DA INTERFACE COM TKINTER ===
janela = tk.Tk()                           # Cria a janela principal
janela.title("Monitor de Presença")        # Define o título da janela
janela.geometry("350x180")                 # Define o tamanho da janela (largura x altura)
janela.resizable(False, False)             # Impede redimensionamento da janela

# Cria o rótulo de status do sistema
status_label = tk.Label(janela, text=f"Status: {status_atual}", font=("Arial", 12))
status_label.pack(pady=10)  # Adiciona espaçamento vertical

# Cria o rótulo com a última data e hora de detecção
ultima_label = tk.Label(janela, text=f"Última detecção: {ultima_data} às {ultima_hora}", font=("Arial", 11))
ultima_label.pack(pady=10)

# Cria botão para resetar o temporizador
reset_btn = tk.Button(janela, text="Resetar manualmente", command=resetar_tempo, bg="lightblue")
reset_btn.pack(pady=10)

# Inicia a função de atualização automática da interface
atualizar_interface()

# Mantém a janela em execução
janela.mainloop()
