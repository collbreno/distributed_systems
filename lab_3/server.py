#servidor de echo: lado servidor
#com finalizacao do lado do servidor
#com multiprocesso
import socket
import select
import sys
import threading

CMD_EXIT = 'exit'
CMD_HIST = 'hist'
CMD_LIST = 'list'
CMD_HELP = '?'
ENCODING = 'utf-8'

# define a localizacao do servidor
HOST = '' # vazio indica que podera receber requisicoes a partir de qq interface de rede da maquina
PORT = 5000 # porta de acesso

#define a lista de I/O de interesse (jah inclui a entrada padrao)
inputs = [sys.stdin]
#armazena lista de conexoes ativas
connections = dict()
#armazena historico de conexoes
history = dict()
#lock para acesso do dicionario 'connections'
lock = threading.Lock()

def get_file_data_or_none(file_name: str):
    ''' Tenta ler o conteúdo do arquivo. 
    Entrada: o nome do arquivo.
    Saida: o texto do arquivo (ou None, caso o arquivo nao exista).'''
    try:
        with open(file_name, 'r') as file:
            data = file.read()
            return data
    except:
        return None

def init_server():
    '''Cria um socket de servidor e o coloca em modo de espera por conexoes
    Saida: o socket criado'''
    # cria o socket 
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Internet( IPv4 + TCP) 

    # vincula a localizacao do servidor
    sock.bind((HOST, PORT))

    # coloca-se em modo de espera por conexoes
    sock.listen(5) 

    # configura o socket para o modo nao-bloqueante
    sock.setblocking(False)

    # inclui o socket principal na lista de entradas de interesse
    inputs.append(sock)

    return sock

def accept_connection(sock):
    '''Aceita o pedido de conexao de um cliente
    Entrada: o socket do servidor
    Saida: o novo socket da conexao e o endereco do cliente'''

    # estabelece conexao com o proximo cliente
    clisock, address = sock.accept()

    # registra a nova conexao
    lock.acquire()
    connections[clisock] = address
    history[clisock] = address
    lock.release()

    return clisock, address

def accept_request(clisock, address):
    '''Recebe o nome do arquivo e palavra a ser pesquisada e
    envia a quantidade de aparições dessa palavra dentro do arquivo.
    Entrada: socket da conexao e endereco do cliente'''
    while True:
        #recebe dados do cliente
        msg = clisock.recv(1024)
        if not msg: # dados vazios: cliente encerrou
            print(f'{address}: Conexão encerrada!')
            lock.acquire()
            del connections[clisock] #retira o cliente da lista de conexoes ativas
            lock.release()
            clisock.close() # encerra a conexao com o cliente
            return 
        # A mensagem vem do cliente com o nome do arquivo e 
        # palavra separados por uma quebra de linha.
        msg = str(msg, encoding=ENCODING).split('\n')
        file_name = msg[0]                                  
        search_query = msg[1]                               
        print(f'{address}: {file_name}, {search_query}')
        file_data = get_file_data_or_none(file_name)

        if file_data is None:                               # Se o arquivo não existe,
            txt = f'O arquivo {file_name} não existe.\n'    # monta a mensagem de erro.
        else:                                               # Se o arquivo existe, conta
            count = file_data.count(search_query)           # a quantidade de aparições
            txt = f'Número de aparições: {count}\n'         # e monta a mensagem

        clisock.send(str.encode(txt, encoding=ENCODING))

def main():
    '''Inicializa e implementa o loop principal (infinito) do servidor'''
    sock = init_server()
    print("Pronto para receber conexoes...")
    while True:
        #espera por qualquer entrada de interesse
        reading, writing, exceptions = select.select(inputs, [], [])
        #tratar todas as entradas prontas
        for current in reading:
            if current == sock:  #pedido novo de conexao
                clisock, address = accept_connection(sock)
                print ('Conectado com: ', address)
                #cria novo processo para atender o cliente
                client = threading.Thread(target=accept_request, args=(clisock,address))
                client.start()
            elif current == sys.stdin: #entrada padrao
                cmd = input()
                if cmd == CMD_EXIT: #solicitacao de finalizacao do servidor
                    if not connections: #somente termina quando nao houver clientes ativos
                        sock.close()
                        sys.exit()
                    else: print(f"Impossível encerrar. Há {len(connections)} conexoes ativas.")
                elif cmd == CMD_HELP:
                    print(f'{CMD_HELP} - Listar comandos válidos\n'+
                        f'{CMD_HIST} - Listar histórico de conexões\n' +
                        f'{CMD_LIST} - Listar conexões ativas\n' +
                        f'{CMD_EXIT} - Encerrar conexão')
                elif cmd == CMD_LIST: 
                    print(str(list(connections.values())))
                elif cmd == CMD_HIST: 
                    print(str(list(history.values())))
                else:
                    print('Comando inválido.')

if __name__ == '__main__':
    main()