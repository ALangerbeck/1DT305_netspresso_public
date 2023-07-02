import socket


def webpage(phrase):
    #Template HTML
    html = f"""
            <!DOCTYPE html>
            <html>
            <p>{phrase}</p>
            </body>
            </html>
            """
    return str(html).encode()

def serve(connection,phrase):
        try:
            client = connection.accept()[0]
            request = client.recv(1024)
            request = str(request)
            print(request)
            html = webpage(phrase)
            client.send(html)
            client.close()
        except OSError: #Not ideal, to general of a catch but this seems to be the best solution
            print("No connection. Stopping to update value...")

def open_socket(ip):
    # Open a socket
    address = (ip, 80)
    connection = socket.socket()
    connection.settimeout(10)
    connection.bind(address)
    connection.listen(1)
    return connection
    
