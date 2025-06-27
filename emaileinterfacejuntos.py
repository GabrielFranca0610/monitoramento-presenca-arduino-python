# === BIBLIOTECAS NECESSÁRIAS ===
import serial                              # Permite comunicação com o Arduino pela porta serial
import time                                # Usado para controle de tempo (delays e marcações de tempo)
import csv                                 # Para salvar os registros de detecção em um arquivo CSV
from datetime import datetime              # Para obter data e hora atual formatadas
import tkinter as tk                       # Biblioteca para criar interface gráfica com o usuário
from tkinter import messagebox             # Para exibir janelas de alerta e confirmação
import smtplib                             # Para enviar e-mails usando o protocolo SMTP
from email.mime.text import MIMEText       # Para criar o corpo do e-mail em texto simples
from email.mime.multipart import MIMEMultipart  # Para montar o e-mail com assunto e corpo

# === CONFIGURAÇÕES DE HARDWARE E ARQUIVOS ===
porta_serial = 'COM4'                      # Porta serial onde o Arduino está conectado (ajuste conforme necessário)
baudrate = 9600                            # Velocidade de comunicação entre Arduino e computador
tempo_espera = 90                          # Tempo de espera entre detecções, em segundos (90s = 1min30s)
arquivo_csv = 'registro_movimentos.csv'    # Nome do arquivo CSV onde serão salvos os registros

# === CONFIGURAÇÕES DO E-MAIL ===
email_origem = 'grupoarduino9879@gmail.com'        # E-mail remetente (de onde será enviado o alerta)
senha_email = 'ytpihskplwelvqmj'                   # Senha de aplicativo gerada no Gmail (não é a senha comum)
email_destino = 'sensorarduino9879@gmail.com'      # E-mail que vai receber o alerta

# === INICIALIZA COMUNICAÇÃO COM O ARDUINO ===
arduino = serial.Serial(porta_serial, baudrate, timeout=1)  # Abre a porta serial com taxa de transmissão e timeout
time.sleep(2)                                                # Aguarda 2 segundos para estabilizar a conexão

# === VARIÁVEIS GLOBAIS PARA INTERFACE E LÓGICA ===
tempo_ultima_detec = 0         # Armazena o tempo da última detecção para controle do tempo_espera
ultima_data = "-"              # Data da última detecção (inicialmente vazio)
ultima_hora = "-"              # Hora da última detecção (inicialmente vazio)
status_atual = "Aguardando movimento"  # Status inicial do sistema mostrado na interface

# === VERIFICA SE O ARQUIVO CSV EXISTE E CRIA O CABEÇALHO SE ESTIVER VAZIO ===
with open(arquivo_csv, mode='a', newline='') as f:
    writer = csv.writer(f)               # Cria o escritor CSV
    if f.tell() == 0:                    # Se o arquivo estiver vazio (posição 0)
        writer.writerow(['Data', 'Hora', 'Status'])  # Escreve o cabeçalho no CSV

# === FUNÇÃO: ENVIAR E-MAIL DE ALERTA ===
def enviar_email(data, hora):
    assunto = "Alerta de Presença Detectada"  # Assunto do e-mail
    corpo = f"Uma presença foi detectada no ambiente monitorado em {data} às {hora}."  # Texto do alerta

    msg = MIMEMultipart()             # Cria um objeto de e-mail multipart
    msg['From'] = email_origem       # Define o remetente
    msg['To'] = email_destino        # Define o destinatário
    msg['Subject'] = assunto         # Define o assunto
    msg.attach(MIMEText(corpo, 'plain'))  # Anexa o corpo de texto como texto plano

    try:
        servidor = smtplib.SMTP('smtp.gmail.com', 587)  # Conecta ao servidor SMTP do Gmail
        servidor.starttls()                             # Inicia uma conexão segura (TLS)
        servidor.login(email_origem, senha_email)       # Faz login na conta de e-mail
        servidor.send_message(msg)                      # Envia o e-mail
        servidor.quit()                                 # Encerra a conexão com o servidor
        print("E-mail enviado com sucesso!")             # Mostra mensagem no terminal
    except Exception as e:
        print("Erro ao enviar e-mail:", e)               # Mostra erro caso ocorra

# === FUNÇÃO PRINCIPAL: VERIFICA O SENSOR E ATUALIZA A INTERFACE ===
def atualizar_interface():
    global tempo_ultima_detec, ultima_data, ultima_hora, status_atual

    try:
        leitura = arduino.readline().decode('utf-8').strip()  # Lê uma linha da serial, decodifica e remove espaços
        agora = time.time()                                   # Captura o tempo atual em segundos

        # Se houver detecção e o tempo de espera já passou
        if "Movimento detectado" in leitura and (agora - tempo_ultima_detec >= tempo_espera):
            tempo_ultima_detec = agora                           # Atualiza o tempo da última detecção
            data = datetime.now().strftime('%d/%m/%Y')           # Pega a data atual formatada
            hora = datetime.now().strftime('%H:%M:%S')           # Pega a hora atual formatada
            ultima_data = data                                   # Salva a data para exibir na interface
            ultima_hora = hora                                   # Salva a hora para exibir na interface
            status_atual = "Movimento detectado!"                # Atualiza o status

            print(f"[{data} {hora}] Presença detectada!")        # Exibe no terminal

            # Grava o evento no arquivo CSV
            with open(arquivo_csv, mode='a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([data, hora, 'Presença detectada'])

            enviar_email(data, hora)  # Envia o e-mail de alerta

        # Se o tempo de espera já passou sem nova detecção
        elif (time.time() - tempo_ultima_detec) >= tempo_espera:
            status_atual = "Aguardando movimento"

        # Atualiza os elementos da interface com os dados atuais
        status_label.config(text=f"Status: {status_atual}")
        ultima_label.config(text=f"Última detecção: {ultima_data} às {ultima_hora}")

    except Exception as e:
        print("Erro:", e)  # Exibe qualquer erro ocorrido

    janela.after(500, atualizar_interface)  # Chama esta função novamente após 500ms (meio segundo)

# === FUNÇÃO: RESET MANUAL DO TEMPORIZADOR ===
def resetar_tempo():
    global tempo_ultima_detec
    tempo_ultima_detec = time.time()  # Reinicia o temporizador
    messagebox.showinfo("Reset", "Temporizador de detecção foi resetado.")  # Mostra confirmação na tela

# === INTERFACE GRÁFICA COM TKINTER ===
janela = tk.Tk()                                  # Cria a janela principal
janela.title("Monitor de Presença com E-mail")    # Define o título da janela
janela.geometry("380x200")                        # Define o tamanho fixo da janela
janela.resizable(False, False)                    # Impede que a janela seja redimensionada

# Rótulo que mostra o status do sistema (aguardando ou detectado)
status_label = tk.Label(janela, text=f"Status: {status_atual}", font=("Arial", 12))
status_label.pack(pady=10)  # Adiciona espaço vertical

# Rótulo que mostra a última detecção registrada
ultima_label = tk.Label(janela, text=f"Última detecção: {ultima_data} às {ultima_hora}", font=("Arial", 11))
ultima_label.pack(pady=10)

# Botão para resetar manualmente o temporizador
reset_btn = tk.Button(janela, text="Resetar manualmente", command=resetar_tempo, bg="lightblue")
reset_btn.pack(pady=10)

# Inicia a função de atualização contínua
atualizar_interface()

# Inicia o loop principal da interface (janela aberta e ativa)
janela.mainloop()
