import socket

HOST = 'localhost' # maquina onde esta o par passivo
PORTA = 5000        # porta que o par passivo esta escutando
EXIT_CODE = 'exit'
ENCODING = 'utf-8'

# Trata o input para não aceitar palavra vazia
def read_input(label: str = None):
    while True:
        txt = input() if label is None else input(label)
        if len(txt) != 0:
            return txt


sock = socket.socket() # default: socket.AF_INET, socket.SOCK_STREAM 
sock.connect((HOST, PORTA)) 

while True:
    # Solicita o input do usuário
    file_name = read_input(f'Digite o nome do arquivo (ou "{EXIT_CODE}" para encerrar): ')
    if file_name == EXIT_CODE:
        break
    search_query = read_input('Digite a palavra a ser buscada: ')

    # Envia apenas uma mensagem para o servidor, contendo as duas entradas
    sock.send(str.encode(f'{file_name}\n{search_query}', encoding=ENCODING))
    print('Enviado')
    # Imprime a resposta
    msg = sock.recv(1024)
    print(str(msg,  encoding=ENCODING))

# encerra a conexao
sock.close() 
