import threading
import socket

def start_server():
    tick = 0
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('localhost', 1234))
    sock.listen(100)
    while True:
        print 'listening...'
        csock, address = sock.accept()
        tick+=1
        print 'connection!' 
        handshake(csock, tick)
        print 'handshaken'
        while True:
            interact(csock, tick)
            tick+=1

def handshake(client, tick):
    our_handshake = "HTTP/1.1 101 Web Socket Protocol Handshake\r\n"+"Upgrade: WebSocket\r\n"+"Connection: Upgrade\r\n"+"WebSocket-Origin: http://localhost:8888\r\n"+"WebSocket-Location: "+" ws://localhost:1234/websession\r\n\r\n"
    shake = client.recv(255)
    print shake
    client.send(our_handshake)
         
def interact(client, tick):
    data = client.recv(255)
    print 'got:%s' %(data)
    client.send("clock ! tick%d\r\n" % (tick))
    client.send("out ! recv\r\n")

if __name__ == '__main__':
    start_server()