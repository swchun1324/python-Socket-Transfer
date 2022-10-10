
import socket
import argparse
import os
import sys

def parameters():

    global dir_path,port

    parser = argparse.ArgumentParser(description='A test program.')

    parser.add_argument("-p", "--port_number", help="Specify the port number.", type=int)
    parser.add_argument("-d", "--dir_path", help="Specify the directory path.", type=str)

    args = parser.parse_args()

    if args.port_number == None:
        port = 4000
    else:
        port = args.port_number

    home_dir = os.path.expanduser('~')
    file_dir = "/servers/downloads"

    if args.dir_path == None:
        dir_path = home_dir + file_dir
    else:
        dir_path = args.dir_path

    isExist = os.path.exists(dir_path)
    
    if isExist == False:
        print("Not exist")
        os.makedirs(dir_path)

parameters()

host_name = socket.gethostname()
IP = socket.gethostbyname(host_name + ".local")
ADDR = (IP, port)
SIZE = 1024
FORMAT = "utf-8"

def main():
    print("[STARTING] Server is starting.")
    """ Staring a TCP socket. """
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    """ Bind the IP and PORT to the server. """
    server.bind(ADDR)

    """ Server is listening, i.e., server is now waiting for the client to connected. """
    server.listen()
    print("[LISTENING] Server is listening.")

    while True:
        """ Server has accepted the connection from the client. """
        conn, addr = server.accept()
        print(f"[NEW CONNECTION] {addr} connected.")

        conn_dir = dir_path + "/" + addr[0]
        print(conn_dir)

        isexist = os.path.exists(conn_dir)
    
        if isexist == False:
            print("Not exist")
            os.makedirs(conn_dir)

        """Receiving the file length"""
        file_length = conn.recv(SIZE).decode(FORMAT)
        print(file_length)

        for i in range(int(file_length)):

            """ Receiving the filename from the client. """
            filename = conn.recv(SIZE).decode(FORMAT)
            file_location = conn_dir + "/" + filename

            filename_list = filename.split(".")

            t = 1

            while os.path.exists(file_location):
                file_location = conn_dir + "/" + filename_list[0] + "-v" + str(t) + ".txt"
                t += 1

            print(f"[RECV] Receiving the filename.")
            file = open(file_location, "w")
            conn.send("Filename received.".encode(FORMAT))

            """ Receiving the file data from the client. """
            data = conn.recv(SIZE).decode(FORMAT)
            print(f"[RECV] Receiving the file data.")
            file.write(data)
            conn.send("File data received".encode(FORMAT))

            """ Closing the file. """
            file.close()

        """ Closing the connection from the client. """
        conn.close()

        print(f"[DISCONNECTED] {addr} disconnected.")

if __name__ == "__main__":
    main()