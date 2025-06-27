💡 Sistema de Monitoramento de Presença com Arduino e Python

Este repositório contém os códigos-fonte e artefatos do projeto de extensão desenvolvido para a disciplina **Aplicações de Cloud, IoT e Indústria 4.0 em Python**, do curso de **Sistemas de Informação** da **Universidade Estácio de Sá**.

📌 Objetivo

Desenvolver um sistema de baixo custo capaz de monitorar áreas restritas de um ambiente profissional, utilizando um **sensor PIR**, LEDs e um script em **Python** para registrar, alertar e exibir informações via interface gráfica.

🏢 Parte Interessada

Empresa colaboradora: TOC – Técnica e Organização Contábil Ltda
Endereço: Rua Darke de Mattos, 92 – Higienópolis, Rio de Janeiro – RJ  


🔧 Componentes Utilizados
- Arduino UNO R3 (ATmega328P)
- Sensor PIR (HC-SR501)
- LEDs (vermelho, amarelo, verde)
- Buzzer ativo 5V
- Cabos jumper, protoboard, resistores
- Interface via Python + Tkinter
- Comunicação serial (Arduino ↔ Python)

📂 Estrutura do Projeto
| Arquivo                          | Descrição |
| `CodigoArduinoSensor_22.ino`     | Código do Arduino para detecção de presença com acionamento de LED e buzzer. |
| `enviaemail.py`                  | Script em Python para envio automático de e-mail ao detectar presença. |
| `interface.py`                   | Interface gráfica Tkinter para exibição de status e controle. |
| `emailinterfacejuntos.py`       | Código final unificado: envia e-mail + exibe interface. |
| `registro.csv`                   | Arquivo de registro de eventos de presença detectada. |

✅ Como Executar

1. Conecte o Arduino e carregue o código `.ino` usando a IDE do Arduino.
2. Execute o script `emailinterfacejuntos.py` com Python 3 instalado.
3. Certifique-se de ter configurado a porta COM corretamente no código Python.
4. Será aberta uma interface exibindo o status atual, última detecção e botão de reset.

📧 Requisitos Python

- `tkinter` (GUI)
- `serial` (`pyserial`)
- `smtplib` e `email` (nativos no Python)
- `csv`, `datetime` (nativos)

Use este comando para instalar o necessário, se faltar algo:
```bash
pip install pyserial
