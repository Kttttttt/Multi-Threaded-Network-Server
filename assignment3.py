import selectors
import socket
import threading
import time
import sys

class Node:
    def __init__(self,data):
        self.data = data
        self.book_title = None
        self.next = None
        self.book_next = None
        self.next_frequent_search = None


def write_book(shared_list,book_title,counter):
    temp_Node = shared_list
    #find the first node with the book_title, which is the start of this book
    while temp_Node.book_title != book_title:
        temp_Node = temp_Node.next

    #create the book file and write in all data
    with open(f"book_{counter:02}.txt", "w") as f:
        while temp_Node != None:
            f.write(temp_Node.data)
            temp_Node = temp_Node.book_next
    return


def handle_client(connection, addr):
    global share_list, share_list_last_node, counter
    print(f"socket:{connection} from {addr} accepted")

    data_buffer = {}
    book_title = None
    connection.settimeout(5)

    while True:
        try:
            data = connection.recv(1024)

            if data == b'':
                # l.acquire()
                # write_book(share_list,book_title,counter)
                # print(f"book:{book_title} written as book0{counter}")
                # counter += 1
                # l.release()
                break
            
            if connection in data_buffer:
                data_buffer[connection] += data
                data_buffer[connection] += b'\n'
            else:
                data_buffer[connection] = data

            #Decode. once the UnicodeDecodeError raise: continue
            lines = data_buffer[connection].decode('utf-8').split('\n')
            #clean the buffer if decode successed
            data_buffer[connection] = b''

            for line in lines:
                new_node = Node(line)
                if book_title == None:
                    book_title = line
                    print(f"new book: {book_title} added")
                    same_book_last_node = new_node
                else:
                    same_book_last_node.book_next = new_node
                    same_book_last_node = new_node 

                new_node.book_title = book_title
                
                l.acquire()
                if share_list == None:
                    share_list = new_node

                #iterator go next
                if share_list_last_node == None:
                    share_list_last_node = new_node
                else:
                    share_list_last_node.next = new_node
                    share_list_last_node = new_node

                print(f"received data from {addr} added in share_list: {new_node.data}")
                l.release()
                     
        except UnicodeDecodeError:
            continue

        except socket.timeout:
            break
    
    #receive step completed
    l.acquire()
    write_book(share_list,book_title,counter)
    print(f"book:{book_title} written as book0{counter}")
    counter += 1
    l.release()

    #disconnect TCP socket
    connection.close()
    print(f"socket:{connection} closed ")
    return


def analysis(start_node,pattern):
    #part 2: pattern appear frequency
    global share_list, book_map
    appeared_list = None
    appeared_last_node = None
    if start_node == None:
        temp = share_list
    else:
        temp = start_node.next
    
    l.acquire()
    while temp != None:
        if temp.book_title not in book_map:
            book_map[temp.book_title] = 0
        appear_time = temp.data.count(pattern)
        book_map[temp.book_title] += appear_time
        if appear_time > 0:
            if appeared_list == None:
                appeared_list = temp
                appeared_last_node = temp
            else:
                appeared_last_node.next_frequent_search = temp
                appeared_last_node = temp
        start_node = temp
        temp = temp.next
    
    print("\n")
    print("Total pattern appear time:")
    for k,v in book_map.items():
        print(f"  Appeared {v} times in book: {k}\n")
    l.release()
    t = threading.Timer(5, analysis, [start_node, pattern])
    t.start()
    return    


#main process↓

#initialise the shared data
share_list = None
share_list_last_node = None
counter = 1
port = 12345
pattern = "no pattern"
book_map = {}

#read port number
if "-l" in sys.argv:
    port_index = sys.argv.index("-l") + 1
    port = int(sys.argv[port_index])

#read pattern
if "-p" in sys.argv:
    pattern = sys.argv[sys.argv.index("-p") + 1]

#initialise socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('localhost', port))
sock.listen(100)
print("Server is listening port:", port)

#create the lock
l = threading.Lock()

#create a thread for pattern checking
analysis_thread = threading.Thread(target=analysis, args=(share_list,pattern))
analysis_thread.start()

#create output files
for i in range(1, 11):
    filename = f"book_{i:02}.txt"
    with open(filename, "w") as file:
        pass

#create thread for each client
while True:
    connection, addr = sock.accept()
    client_thread = threading.Thread(target=handle_client, args=(connection, addr))
    client_thread.start()

