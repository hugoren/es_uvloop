import selectors
import socket

selector = selectors.DefaultSelector()
stopped = False


def accept(sock, mask):
    conn, addr = sock.accept()
    conn.setblocking(False)
    selector.register(conn, selectors.EVENT_READ, read)
    print(1111)


def read(conn, mask):
    data = conn.recv(1000)
    if data:
        print(22222)
        print(data)
        conn.send(data)
    else:
        selector.unregister(conn)
        conn.close()


sock =socket.socket()
sock.bind(("127.0.0.1", 60001))
sock.listen(100)
selector.register(sock, selectors.EVENT_READ, accept)

while 1:
    events = selector.select()
    for key, mask in events:
       callback = key.data
       callback(key.fileobj, mask)