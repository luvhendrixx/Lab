#include <stdio.h> // common C utils
#include <stdlib.h> // other common C utils
#include <sys/types.h> // common types
#include <sys/socket.h> // socket utils
#include <unistd.h> // unix api
#include <netinet/in.h> // protocol utils

int main() {
    int server_socket;

    char server_message[256] = "Hello from the server";

    server_socket = socket(AF_INET, SOCK_STREAM, 0);

    if (server_socket < 0) {
        perror("Socket creation failed");
        exit(EXIT_FAILURE);
    }

    // fetching the addr
    struct sockaddr_in server_address = {
        .sin_family = AF_INET, // addr belongs to IPv4 family
        .sin_port = htons(9002), // binding port..& htons translates my comps local fmting into the std internet fmting so pkts don't get lost in transit
        .sin_addr.s_addr = INADDR_ANY // "means bind to all available services"...allows the server to listen for incoming conns arriving thru wifi or ethernet (translates to 0.0.0.0)
    };

     if (bind(server_socket, (struct sockaddr*) &server_address, sizeof(server_address)) < 0) {
         perror("Binding the socket failed");
         exit(EXIT_FAILURE);
     }

     if (listen(server_socket, 5) < 0) {
         perror("Server listening failed");
         exit(EXIT_FAILURE);
     }

     int client_socket;
     client_socket = accept(server_socket, NULL, NULL);
     if (client_socket < 0) {
         perror("Client socket is negative, couldn't accept");
         exit(EXIT_FAILURE);
     }

     send(client_socket, server_message, sizeof(server_message), 0);

     close(server_socket);
     close(client_socket);

     return 0;
}
