import socket
import threading
from datetime import datetime

HOST = '0.0.0.0'
PORT = 45000
BUFFER_SIZE = 1024

def handle_client(conn, addr):
    print(f"[+] Terhubung dengan {addr}")
    try:
        with conn:
            while True:
                data = conn.recv(BUFFER_SIZE)
                if not data:
                    break

                message = data.decode('utf-8').strip()  # Hapus whitespace
                print(f"[DEBUG] Diterima dari {addr}: {repr(message)}")

                if message == "QUIT":
                    print(f"[-] Klien {addr} mengirim QUIT, menutup koneksi.")
                    break
                elif message == "TIME":
                    current_time = datetime.now().strftime("%H:%M:%S")
                    response = f"JAM {current_time}\r\n"
                    print(f"[DEBUG] Mengirim respon ke {addr}: {repr(response)}")
                    conn.sendall(response.encode('utf-8'))
                else:
                    print(f"[!] Permintaan tidak valid dari {addr}: {repr(message)}")
    except Exception as e:
        print(f"[!] Error dari {addr}: {e}")
    finally:
        conn.close()
        print(f"[~] Koneksi dengan {addr} ditutup.")

def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind((HOST, PORT))
        server.listen()
        print(f"[*] Time server aktif di port {PORT}...")

        while True:
            conn, addr = server.accept()
            threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()

if __name__ == "__main__":
    start_server()
