# Multithreaded Concurrent Non-blocking Reception Simulation
	This is a server simulation application designed to concurrently receive data from multiple clients. The server accepts the content of books, with the content of each book being transmitted consecutively. Upon the full reception of each book's content, the server saves it as book01.txt to book10.txt. Additionally, the server periodically checks for the occurrence of a specified pattern in the received data.

## Usage
### Running the Server
1. Open your terminal or command prompt.
2. Navigate to the directory containing Multi-Threaded_Network_Server.py.
3. Run the following command to start the server:
	- python3 Multi-Threaded_Network_Server.py -l <port_number> -p "<pattern>"
	Where <port_number> is the port number you wish the server to listen on, and "<pattern>" is the pattern you wish to search for within the data.

For instance:
	- python3 Multi-Threaded_Network_Server.py -l 12345 -p "example"
	This will start the server on port 12345 and search for the pattern "example".


### Running the Client
1. Ensure the server is running and is listening on the specified port.
2. In another terminal, execute the following command to start a client:
	- nc localhost <port_number> -i <delay> < file.txt
	Where <port_number> is the port the server is listening on, <delay> is the delay between sending data in seconds, and <file.txt> is the filename of the book to be transmitted.
3. Run 10 clients at the same time, simulating concurrent transfer of files from book01.txt to book10.txt.

For example, to transmit book1.txt to a server listening on port 12345 with a 1-second delay between sending each line of data, run:
	- nc localhost 12345 -i 1 < book1.txt

### Feedback
- The server will display the received data, and save it to the respective file once the data is fully received.
- Every 5 seconds, the server will display the occurrences of the specified pattern in total and within each book following the order.
