import socket
import threading

SERVER_IP = "127.0.0.1"  # TODO: 改成服务器的公网 IP
PORT = 9999

def receive(sock):
    """死循环收服务器转发的消息"""
    while True:
        try:
            msg = sock.recv(1024)
            if not msg:
                break
            print(f"\r{msg.decode()}\n> ", end="")
        except:
            break
    print("\n[!] 与服务器断开连接")

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((SERVER_IP, PORT))
    print(f"已连接到 {SERVER_IP}:{PORT}，开始聊天吧！")

    # 开一个线程专门收消息
    threading.Thread(target=receive, args=(sock,), daemon=True).start()

    # 主线程负责发消息
    while True:
        try:
            msg = input("> ")
            sock.send(msg.encode())
        except:
            break
    sock.close()

if __name__ == "__main__":
    main()
