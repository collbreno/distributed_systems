# Exemplo basico socket (lado ativo)

import socket

HOST = 'localhost' # maquina onde esta o par passivo
PORTA = 5000        # porta que o par passivo esta escutando
EXIT_CODE = 'bye'
ENCODING = 'utf-8'

# cria socket
sock = socket.socket() # default: socket.AF_INET, socket.SOCK_STREAM 

# conecta-se com o par passivo
sock.connect((HOST, PORTA)) 


while True:
    txt = input()
    if txt == EXIT_CODE:
        break
    sock.send(str.encode(txt, encoding=ENCODING))
    msg = sock.recv(1024) 
    print(str(msg,  encoding='utf-8'))

# encerra a conexao
sock.close() 
