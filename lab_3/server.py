import socket

HOST = ''   
PORTA = 5000
ENCODING = 'utf-8'

# Tenta ler o conteúdo do arquivo. 
# Caso o arquivo não exista, retorna None.
def get_file_data_or_none(file_name: str):
    try:
        with open(file_name, 'r') as file:
            data = file.read()
            return data
    except:
        return None

# cria um socket para comunicacao
sock = socket.socket()

# vincula a interface e porta para comunicacao
sock.bind((HOST, PORTA))

# define o limite maximo de conexoes pendentes e coloca-se em modo de espera por conexao
sock.listen(5) 

# Fica em loop infinito, esperando novas conexões
while True:
    # aceita a primeira conexao da fila (chamada pode ser BLOQUEANTE)
    print('Aguardando conexão...')
    new_sock, address = sock.accept() 
    print ('Conectado com: ', address)

    while True:
        # depois de conectar-se, espera uma mensagem (chamada pode ser BLOQUEANTE))
        file_name = str(new_sock.recv(1024), encoding=ENCODING)
        search_query = str(new_sock.recv(1024), encoding=ENCODING)
        if not file_name or not search_query:
            break

        file_data = get_file_data_or_none(file_name)

        if file_data is None:                               # Se o arquivo não existe,
            txt = f'O arquivo {file_name} não existe.\n'    # monta a mensagem de erro.
        else:                                               # Se o arquivo existe, conta
            count = file_data.count(search_query)           # a quantidade de aparições
            txt = f'Número de aparições: {count}\n'         # e monta a mensagem

        new_sock.send(str.encode(txt, encoding=ENCODING))
    
    # fecha o socket da conexao
    new_sock.close() 

# fecha o socket principal
sock.close() 
