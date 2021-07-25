# Exemplo basico socket (lado passivo)

import socket

HOST = ''   
PORTA = 5000

# cria um socket para comunicacao
sock = socket.socket()

# vincula a interface e porta para comunicacao
sock.bind((HOST, PORTA))

# define o limite maximo de conexoes pendentes e coloca-se em modo de espera por conexao
sock.listen(5) 

# aceita a primeira conexao da fila (chamada pode ser BLOQUEANTE)
print('Aguardando conexão...')
new_sock, address = sock.accept() 
print ('Conectado com: ', address)

while True:
    # depois de conectar-se, espera uma mensagem (chamada pode ser BLOQUEANTE))
    msg = new_sock.recv(1024) # argumento indica a qtde maxima de dados
    if not msg:
        break
    new_sock.send(msg) 

# fecha o socket da conexao
new_sock.close() 

# fecha o socket principal
sock.close() 
