import socket
import threading

HOST = "0.0.0.0"  # 监听所有网卡
PORT = 9999

clients = []  # 保存所有连接的客户端

def handle(conn, addr):
    """每个客户端一个线程，死循环收消息然后广播"""
    name = f"{addr[0]}:{addr[1]}"
    print(f"[+] {name} 上线了")
    broadcast(f"--- {name} 加入了聊天室 ---".encode())
    while True:
        try:
            msg = conn.recv(1024)  # 阻塞等待对方发消息
            if not msg:
                break
            text = f"{name}: {msg.decode()}"
            print(text)
            broadcast(text.encode())
        except:
            break
    print(f"[-] {name} 断开了")
    clients.remove(conn)
    conn.close()

def broadcast(msg):
    """把消息发给所有在线的客户端"""
    for c in clients:
        try:
            c.send(msg)
        except:
            pass

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    print(f"服务器监听 {PORT} 端口...")
    while True:
        conn, addr = server.accept()  # 阻塞等待新连接
        clients.append(conn)
        threading.Thread(target=handle, args=(conn, addr), daemon=True).start()

if __name__ == "__main__":
    main()
