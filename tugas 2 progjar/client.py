import socket
import logging

logging.basicConfig(level=logging.INFO)

def main():
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = ('localhost', 45000)
        logging.info(f"Connecting to {server_address}")
        sock.connect(server_address)
        sock.settimeout(5)  # Timeout untuk cegah client nunggu selamanya

        # Kirim permintaan TIME
        message = "TIME\r\n"
        logging.info(f"Sending: {message.strip()}")
        sock.sendall(message.encode('utf-8'))

        # Terima respon
        response = b""
        while True:
            try:
                data = sock.recv(1024)
                if not data:
                    break
                response += data
            except socket.timeout:
                break  # Jika timeout, keluar dari loop

        logging.info(f"Received: {response.decode('utf-8').strip()}")

        # Kirim permintaan QUIT
        quit_message = "QUIT\r\n"
        logging.info("Sending QUIT")
        sock.sendall(quit_message.encode('utf-8'))

    except Exception as e:
        logging.error(f"ERROR: {str(e)}")
    finally:
        logging.info("Closing connection")
        sock.close()

if __name__ == "__main__":
    main()
