import threading
import socket
import json
import labasededonne
import time

HOST = socket.gethostbyname(socket.gethostname())
PORT = 54569

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()
Format = 'utf-8'
nickname = None
clients = []
nicknames = []


def broadcast(message, client):
    for client_1 in clients:
        if client_1 != client:
            client_1.sendall((message + "#" + "Groupe").encode(Format))


def private_message(message, index, client, receiver):
    client_1 = clients[index]
    if client != client_1:
        client_1.sendall((message + "#" + receiver).encode(Format))


def room_messages(k, l_00, nk, receiver, cliii):
    l_0 = [item for sublist in l_00 for item in sublist]
    for i in l_0:
        if i in nk:
            ond = nicknames.index(i)
            if clients[ond] != cliii:
                clients[ond].send((k + '#' + receiver).encode(Format))


def handle(client):
    global nickname
    while True:
        try:
            message_full = client.recv(1024).decode(Format)
            if "its comming" in message_full:
                json_data = client.recv(1024).decode('utf-8')
                received_data = json.loads(json_data)
                j = labasededonne.verification(received_data[0])
                if j == 1:
                    labasededonne.addto_data(received_data[0], received_data[1], received_data[2])
                    client.send('pass'.encode(Format))
                else:
                    client.send("can't".encode(Format))
            elif "list" in message_full:
                client.send('name'.encode('utf-8'))
                time.sleep(0.1)
                json_data = json.dumps(nicknames)
                client.send(json_data.encode('utf-8'))
                time.sleep(0.1)
                data_1 = labasededonne.offline()
                json_data_1 = json.dumps(data_1)
                client.send(json_data_1.encode(Format))
            elif 'torique' in message_full:
                client.send('sift'.encode(Format))
                sdrc = client.recv(1024).decode('utf-8')
                hs = sdrc.split(sep='#')
                rc = hs[0].strip()
                sd = hs[1].strip()
                jjj = labasededonne.verf_histo()
                jjj = [item for sublist in jjj for item in sublist]
                if rc in jjj:
                    historique = labasededonne.recuperer_groupe(rc)
                    historique_2 = labasededonne.recupere_timegr(rc)
                    historique_1 = json.dumps(historique)
                    client.send(historique_1.encode(Format))
                    time.sleep(0.1)
                    historique_3 = json.dumps(historique_2)
                    client.send(historique_3.encode(Format))
                else:
                    historique = labasededonne.recuperer_historique(sd, rc)
                    historique_2 = labasededonne.recupere_timepr(sd, rc)
                    historique_1 = json.dumps(historique)
                    client.send(historique_1.encode(Format))
                    time.sleep(0.1)
                    historique_3 = json.dumps(historique_2)
                    client.send(historique_3.encode(Format))

            elif "verf" in message_full:
                myinfos = client.recv(1024).decode(Format)
                myinfos_1 = myinfos.split(sep='#')
                nickname = myinfos_1[0]
                coode = myinfos_1[1]
                x = labasededonne.serch(nickname, coode)
                if x == 1:
                    client.send("didn't found it".encode('utf-8'))
                else:
                    client.send("found it".encode('utf-8'))
                    time.sleep(0.1)
                    print("Nickname is {}".format(nickname))
                    nicknames.append(nickname)
                    clients.append(client)
                    touslessalon = labasededonne.allrooms()
                    for cl in clients:
                        cl.send('name'.encode(Format))
                        time.sleep(0.3)
                        json_data = json.dumps(nicknames)
                        cl.send(json_data.encode(Format))
                        time.sleep(0.1)
                        data_1 = labasededonne.offline()
                        json_data_1 = json.dumps(data_1)
                        cl.send(json_data_1.encode(Format))
                        time.sleep(0.1)
                    for cli in clients:
                        cli.send('touslesroom'.encode(Format))
                        time.sleep(0.2)
                        toussalon = json.dumps(touslessalon)
                        cli.send(toussalon.encode(Format))

            elif message_full == "change":
                oldname = client.recv(1024).decode(Format)
                newname = client.recv(1024).decode(Format)
                labasededonne.change_name(newname, oldname)
                ind = nicknames.index(oldname)
                nicknames[ind] = newname
                for cl in clients:
                    cl.send('name'.encode(Format))
                    time.sleep(0.1)
                    json_data = json.dumps(nicknames)
                    cl.send(json_data.encode(Format))
                    time.sleep(0.1)
                    data_1 = labasededonne.offline()
                    json_data_1 = json.dumps(data_1)
                    cl.send(json_data_1.encode(Format))
                broadcast(f"{oldname} has changed his name to {newname}", client)
            elif message_full == 'creergrp':
                groupname = client.recv(1024).decode(Format)
                time.sleep(0.1)
                groupadmn = client.recv(1024).decode(Format)

                try:
                    labasededonne.creerroom(groupadmn, groupname)
                    print("Group added to the database successfully")
                except Exception as e:
                    print("Error adding group to the database:", str(e))
                touslessalon = labasededonne.allrooms()
                for cli in clients:
                    cli.send('touslesroom'.encode(Format))
                    time.sleep(0.1)
                    toussalon = json.dumps(touslessalon)
                    cli.send(toussalon.encode(Format))
            elif message_full == 'jo2in':
                joindeddroup = client.recv(1024).decode('utf-8')
                time.sleep(0.1)
                whojoined = client.recv(1024).decode('utf-8')
                l_1 = labasededonne.verf_room(joindeddroup)
                l_0 = [item[0] for item in l_1]
                whojoined = whojoined.replace('torique', '')
                if whojoined not in l_0:
                    labasededonne.add_to_rooms(whojoined, joindeddroup)
                    room_messages(f"{whojoined} joined the room {joindeddroup}", l_1, nicknames, joindeddroup, client)
            else:
                parts = message_full.split(sep='@')
                if len(parts) == 3:
                    nooooooooom = parts[0]
                    message = parts[1]
                    receiver = parts[2].strip()
                    labasededonne.ajouter_message(nooooooooom.strip(), receiver.strip(), message.strip())
                    if receiver not in nicknames:
                        continue
                    index = nicknames.index(receiver)
                    private_message(nooooooooom + " : " + message + " ", index, client, nooooooooom)
                elif len(parts) == 2:
                    message__9 = parts[1].split(sep='$')
                    message = message__9[0]
                    roomnaaaame = message__9[1]
                    nooooooooom = parts[0]
                    l_1234 = labasededonne.verf_room(roomnaaaame)
                    room_messages(nooooooooom + ":" + message, l_1234, nicknames, roomnaaaame, client)
                    labasededonne.ajouter_message(nooooooooom.strip(), roomnaaaame, message)
                else:
                    client.close()
                    break

        except:
            index = clients.index(client)
            clients.remove(client)
            nickname = nicknames[index]
            nicknames.remove(nickname)
            for cl in clients:
                try:
                    cl.send('name'.encode(Format))
                    time.sleep(0.1)
                    json_data = json.dumps(nicknames)
                    cl.send(json_data.encode(Format))
                    time.sleep(0.1)
                    data_1 = labasededonne.offline()
                    json_data_1 = json.dumps(data_1)
                    cl.send(json_data_1.encode(Format))
                except Exception as inner_exception:
                    print(
                        f"An exception occurred while notifying clients: {type(inner_exception).__name__} - {inner_exception}")
            client.close()
            break


def receive():
    global nickname
    while True:
        client, address = server.accept()
        print(f"Connected with {str(address)}!")
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


print("server running .....")
receive()
