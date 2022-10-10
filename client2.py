import socket
import argparse 
import os
parser = argparse.ArgumentParser(description='A test program.')

parser.add_argument("-p", "--port_number", help="Specify the port number.", type=int)
parser.add_argument("-s", "--server_ip", help="Specify the Server ip address.", type=str, required=True)
parser.add_argument('file', help="Adds the readable text file such as .txt file", type=str, nargs='+')

args = parser.parse_args()

if args.port_number == None:
    #Set Default port number 4000
    port = 4000
else:
    port = args.port_number

try:
    for i in args.file:
        if os.path.exists(i):
            continue
        else:
            exit()
except:
    print("Os path does not look correct!")
    exit()


IP = args.server_ip
PORT = port
ADDR = (IP, PORT)
FORMAT = "utf-8"
SIZE = 1024

file_list = args.file

file_length = len(file_list)

def main():
    """ Staring a TCP socket. """
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    """ Connecting to the server. """
    client.connect(ADDR)
    client.send(str(file_length).encode(FORMAT))


    for filename in file_list:

        """ Opening and reading the file data. """
        filename = filename.split("/")[-1]
        print(filename)
        file = open(filename, "r")
        data = file.read()

        """ Sending the filename to the server. """
        client.send(filename.encode(FORMAT))
        msg = client.recv(SIZE).decode(FORMAT)
        print(f"[SERVER]: {msg}")

        """ Sending the file data to the server. """
        client.send(data.encode(FORMAT))
        msg = client.recv(SIZE).decode(FORMAT)
        print(f"[SERVER]: {msg}")

        """ Closing the file. """
        file.close()

        """ Closing the connection from the server. """
    client.close()


if __name__ == "__main__":
    main()