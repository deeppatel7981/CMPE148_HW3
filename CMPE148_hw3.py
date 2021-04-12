import base64
import ssl
from socket import *


# from smtplib import SMTP
def main():
    msg = "\r\n I love computer networks!"
    endmsg = "\r\n.\r\n"

    # Choose a mail server (e.g. Google mail server) and call it mailserver
    mailserver = ("smtp.gmail.com", 587)

    # Create socket called client_socket and establish a TCP connection with mailserver
    client_socket = socket(AF_INET, SOCK_STREAM)
    client_socket.connect(mailserver)
    recv = client_socket.recv(1024).decode()
    print(recv)
    if recv[:3] != '220':
        print('220 reply not received from server.')

    # Send HELO command and print server response.
    heloCommand = 'HELO Alice\r\n'
    client_socket.send(heloCommand.encode())
    recv_1 = client_socket.recv(1024).decode()
    print(recv_1)
    if recv_1[:3] != '250':
        print('250 reply not received from server.')

    # gmail smtp requires ssl/tls authentication
    tls_command = "STARTTLS\r\n"
    client_socket.send(tls_command.encode())
    recv_2 = client_socket.recv(1024).decode()
    print(recv_2)
    client_socket = ssl.wrap_socket(client_socket)

    # send HELO command again after auth
    heloCommand = 'HELO Alice\r\n'
    client_socket.send(heloCommand.encode())
    recv_3 = client_socket.recv(1024).decode()
    print(recv_3)
    if recv_3[:3] != '250':
        print('250 reply not received from server.')

    username = "pateldcp18@gmail.com"
    password = "Sunita@19721618"
    base64_str = ("\x00" + username + "\x00" + password).encode()
    base64_str = base64.b64encode(base64_str)
    auth_msg = "AUTH PLAIN ".encode() + base64_str + "\r\n".encode()
    client_socket.send(auth_msg)
    recv_4 = client_socket.recv(1024).decode()
    print(recv_4)

    # Send MAIL FROM command and print server response.
    mail_from_command = 'MAIL FROM:<pateldcp18@gmail.com>\r\n'
    client_socket.send(mail_from_command.encode())
    recv_5 = client_socket.recv(1024).decode()
    print(recv_5)
    if recv_5[:3] != '250':
        print('250 mail from error.')

    # Send RCPT TO command and print server response.
    mail_from_command = 'RCPT TO:<deep.c.patel@sjsu.edu>\r\n'
    client_socket.send(mail_from_command.encode())
    recv_6 = client_socket.recv(1024).decode()
    print(recv_6)
    if recv_6[:3] != '250':
        print('250 mail from error.')

    # Send DATA command and print server response.
    client_socket.send('DATA\r\n'.encode())
    recv_7 = client_socket.recv(1024).decode()
    print(recv_7)
    if recv_7[:3] != '354':
        print('354 reply not received from server.')

    # Send message data.
    # subject from to
    subject = "Subject: CMPE148 SMTP Lab \r\n\r\n"
    client_socket.send(subject.encode())
    client_socket.send(msg.encode())

    # Message ends with a single period.
    client_socket.send(endmsg.encode())
    recv_8 = client_socket.recv(1024)
    print("Response " + recv_8.decode())

    # Send QUIT command and get server response.
    client_socket.send('QUIT\r\n'.encode())
    recv_9 = client_socket.recv(1024)
    print(recv_9.decode())
    client_socket.close()


# main code to run
if __name__ == "__main__":
    main()
