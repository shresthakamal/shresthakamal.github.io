import ssl, socket, time, os, click


TIME_DELAY = 2


class bcol:
    SERVER_col = "\033[95m"  # LightMagenta
    CLIENT_col = "\033[94m"  # LightYellow
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    FAIL = "\033[91m"  # LigntRed
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


# Eg Implementation
# print(bcol.OKBLUE + "SAMPLE TEXT" + bcol.ENDC)
# print(f"{bcol.OKBLUE}SAMPLE TEXT{bcol.ENDC}")


def create_socket() -> socket:
    """Creating SOCK_STREAM Sockets

    Returns:
        socket: Returns sockets
    """
    return socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def get_context(certificate: str, private_key: str, root: str = "/usr/local/share/ca-certificates/root.crt"):
    """Function to return the context from certificate verification from OpenSSL

    Args:
        certificate (str): Certificate of the client
        private_key (str): Private key of the client
        root (str, optional): Location to the root certificate. Defaults to "/usr/local/share/ca-certificates/root.crt".

    Returns:
        SSLContext: Returns an OpenSSL context
    """
    # Getting an OpenSSL context
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    context.load_verify_locations(root)
    context.load_cert_chain(certificate, private_key)
    context.verify_mode = ssl.CERT_REQUIRED
    context.check_hostname = False
    return context


def clean() -> None:
    """Clean the Terminal"""
    os.system("cls" if os.name == "nt" else "clear")


def runserver(PORT: int = 6060):
    """Function to Run the Server

    Args:
        PORT (int, optional): Server Port. Defaults to 6060.

    Raises:
        SystemExit: Invoked by chat_close
    """

    # Creating a server socket that listens to a defined PORT (default = 6060)
    serversocket = create_socket()
    serversocket.bind(("", PORT))

    # Create an infinitialize_chate loop until a client connects to the server
    serversocket.listen(1)

    # Formatted Terminal Output
    print(bcol.OKCYAN + "[INFO]: Server Up ... " + bcol.ENDC)
    print(bcol.OKCYAN + "[INFO]: Listening to Clients ... \n" + bcol.ENDC)

    # When the client connects to the server via the same port in which the server is connected to then
    # The values of the client socket and client address is recived
    clientsocket, clientIP = serversocket.accept()

    print(f"{bcol.OKCYAN}[INFO]: Connection request from {clientIP[0]}{bcol.ENDC}")
    time.sleep(TIME_DELAY - 1.5)
    print(f"{bcol.OKCYAN}[SUCCESS]: Client, {clientIP[0]} accepted.{bcol.ENDC} \n")

    print(bcol.OKCYAN + "Creating a TCP Communication Channel..." + bcol.ENDC)
    time.sleep(TIME_DELAY)
    clean()

    print(bcol.OKGREEN + "[SUCCESS]: TCP Communication Channel established !!\n" + bcol.ENDC)

    while True:

        # Receiving data from the connected client
        recv_data = clientsocket.recv(1024)
        print(f"\n{bcol.CLIENT_col}Client({clientIP[0]}){bcol.ENDC}: {recv_data.decode()}\n")

        # Standard Communiation exchange
        # If chat_hello is received automatically send "chat_reply"
        if recv_data.decode() == "chat_hello":
            clientsocket.sendall("chat_reply".encode())

        # If "chat_STARTTLS" is received by server, start OpenSSL Protocols for encrypted channel
        elif recv_data.decode() == "chat_STARTTLS":
            clientsocket.sendall("chat_STARTTLS_ACK".encode())

            # Loading Keys and Certificates to get the context
            context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
            context.load_verify_locations("/usr/local/share/ca-certificates/root.crt")
            context.load_cert_chain("Bob/bob.crt", "Bob/bob_key.pem")
            context.verify_mode = ssl.CERT_REQUIRED
            context.check_hostname = False

            # Wrapping the TCP socket using the context to get encrypted communication
            clientsocket = context.wrap_socket(clientsocket, server_side=True, do_handshake_on_connect=True)
            clean()
            print(f"{bcol.OKGREEN}[INFO]: Secure TLS 1.3 pipe Established with Client: {clientIP[0]}{bcol.ENDC}\n")

        # Requested "chat_close" from the client
        elif recv_data.decode() == "chat_close":
            print("Chat Close requested by Client")
            print("Leaving the communication in 2 secs...")
            time.sleep(TIME_DELAY + 1)
            raise SystemExit
        # else
        else:
            # If none of above conditions match meaning there is not close request, no encryption request
            # So, we will continue on with the plain TCP communication
            send_data = input("Enter message to send: ")
            clientsocket.sendall(send_data.encode())

            # Chat close request from the server side.
            if send_data == "chat_close":
                print("Leaving the communication in 2 sec...")
                time.sleep(TIME_DELAY + 1)
                clientsocket.close()
                serversocket.close()
                raise SystemExit


def runclient(server: str = "bob1", PORT: int = 6060, clientcertificate: str = None, clientkey: str = None, run_dns: bool = False) -> None:
    """Function to run the client for chat application

    Args:
        server (str, optional): Name of the server. Defaults to "bob1".
        PORT (int, optional): Client side port. Defaults to 6060.
        clientcertificate (str, optional): Client Certificate. Defaults to None.
        clientkey (str, optional): Private Key of Client. Defaults to None.
        run_dns (bool, optional): Flag for DNS. Defaults to False.

    Raises:
        Exception: DNS Name Resolution Exception
    """

    # Client Socket
    clientsocket = create_socket()
    if server == "alice1":
        serverIP = "172.31.0.2"
    else:
        serverIP = "172.31.0.3"
    # Client Connecting to the server with a given port
    clientsocket.connect((serverIP, PORT))

    print(f"{bcol.OKGREEN}[SUCCESS]: Connection established,{bcol.ENDC} {server}: {serverIP}\n")

    print("Creating a TCP Communication Channel...")
    time.sleep(TIME_DELAY + 1)
    clean()

    print(bcol.OKGREEN + "[SUCCESS]: TCP Communication Channel established !!\n" + bcol.ENDC)

    # Mandatory "chat_hello" at the begining of each conversation
    clientsocket.sendall("chat_hello".encode())

    # The client is immediately in receiving mode after sending a message = HALF DUPLEX
    recv_data = clientsocket.recv(1024)

    # Printing all the received messages
    print(f"{bcol.OKCYAN}{server}:{bcol.ENDC} {recv_data.decode()}\n")

    while True:

        # Get the message from the client to send to the server
        # The received message is sent via the client socket.
        msg = input("Enter message to send: ")

        # SEND
        clientsocket.sendall(msg.encode())

        # If the sent message is "chat_close" from the client
        # Server is bound to close the connection, TCP
        if msg == "chat_close":
            print("Leaving the communication in 2 sec...")
            time.sleep(TIME_DELAY + 1)
            break

        # RECEIVE
        # Waiting for any message sent from server
        recv_data = clientsocket.recv(1024)
        print(f"\n{bcol.OKCYAN}{server}{bcol.ENDC}: {recv_data.decode()}\n")

        # Received Message:
        #     = "chat_STARTTLS_ACK" => Start TLS Encryption
        #     = "chat_STARTTLS_NOT_SUPPORTED" => Reject TLS Encryption and continue with TCP
        #     = "chat_close" => Quit chat

        if recv_data.decode() == "chat_STARTTLS_ACK":
            print("[INFO]: Encryption Accepted.")

            # Start TLS Procedure with proided certficates
            context = get_context(certificate=clientcertificate, private_key=clientkey)

            clientsocket = context.wrap_socket(clientsocket, server_hostname=server, do_handshake_on_connect=True)
            print("[SUCCESS]: SSL Certificates Verified Succesfully\n")

            print(f"[INFO]: Connecting to secure channel ...")
            time.sleep(TIME_DELAY)
            clean()
            print(f"{bcol.OKGREEN}[INFO]: End-to-End Encryption Enabled!!{bcol.ENDC}\n")

        elif recv_data.decode() == "chat_STARTTLS_NOT_SUPPORTED":
            # print("[INFO]: Encryption Rejected.\n")
            # print("Continuing in TCP connection")
            continue

        if recv_data.decode() == "chat_close":
            print("Chat Close request by server.")
            print("Leaving the communication...")
            time.sleep(TIME_DELAY + 1)
            break
    clientsocket.close()


# Terminal line options
@click.command()
@click.option("-s", help="Server side Communication", default=True, is_flag=True)
@click.option("-c", help="Client Side Communication", default=None)
@click.option("-p", help="Port for communication between server and client", default=6060)
@click.option("-dns", help="Flag to specify if mannual DNS resolution is required or not", default=False, is_flag=True)
def main(s, c, p, dns):

    if c == None and s is False:
        print("\n[INFO]: Opening Communication Server...\n")
        time.sleep(1)

        runserver(PORT=p)
    if c is not None:
        print(f"\n [INFO]: Creating a TCP connection between client and server: '{c}'...\n")
        time.sleep(1)
        clientcertificate = "Alice/alice.crt"
        clientkey = "Alice/alice_key.pem"
        runclient(server=c, PORT=p, clientcertificate=clientcertificate, clientkey=clientkey, run_dns=dns)

    else:
        print(f"\n[ERROR]: Input Parameters not matching..\n")
        print(f"[INFO]: Run `python3 secure_chat_app.py --help`")


# Main Runner
if __name__ == "__main__":
    main()

