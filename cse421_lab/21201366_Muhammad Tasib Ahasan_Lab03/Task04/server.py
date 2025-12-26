import socket
import threading

port = 5050
buffer = 16
format = 'utf-8'

hostname = socket.gethostname()
server_ip_addr = socket.gethostbyname(hostname)


server_sock_addr = (server_ip_addr, port)
print("Server's socket address is", server_sock_addr)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(server_sock_addr)


server.listen()
print("I am listening to requests.....")

def calculate_salary(hours_worked):
    if hours_worked <= 40:
        return hours_worked * 200
    else:
        return 8000 + (hours_worked - 40) * 300

def client_in_different_thread(conn, client_sock_addr):
    print("Connected to client", client_sock_addr)
    connected = True
    while connected:
        next_msg_length = conn.recv(16).decode(format)
        print("Upcoming message lenght is", next_msg_length)


        if next_msg_length:
            message = conn.recv(int(next_msg_length)).decode(format)
            print("Sent from the client: ",message)


            if message == "Terminate":
                print("Terminating connection with", client_sock_addr)
                conn.send("Connection terminates as you have wished".encode(format))
                connected = False
            else:
                hours_worked = int(message)
                salary = calculate_salary(hours_worked)
                response = f"Calculated Salary: Tk {salary}"      
                conn.send(response.encode(format))

    conn.close            

while True:
    conn, client_sock_addr = server.accept()
    thread = threading.Thread(target=client_in_different_thread, args = (conn, client_sock_addr))
    thread.start()