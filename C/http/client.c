#include <stdio.h> // common C utils
#include <stdlib.h> // other common C utils
#include <sys/types.h> // common types
#include <sys/socket.h> // socket utils
#include <unistd.h> // unix api
#include <netinet/in.h> // protocol utils

int main() {
    int network_socket; // the client will conn here

    // we create a TCP sock working on IPv4
    // returns a int (known as a file descriptor)
    network_socket = socket(AF_INET, SOCK_STREAM, 0);

    if (network_socket < 0) {
        // could also use smthing like...
        // printf("Creating the socket failed: %s (Error code: %d)\n", strerror(errno), errno);
        perror("Socket creation failed");
        exit(EXIT_FAILURE);
    }

    // fetching the addr
    struct sockaddr_in server_address = {
        .sin_family = AF_INET, // addr belongs to IPv4 family
        .sin_port = htons(9002), // binding port..& htons translates my comps local fmting into the std internet fmting so pkts don't get lost in transit
        .sin_addr.s_addr = INADDR_ANY // "means bind to all available services"...allows the server to listen for incoming conns arriving thru wifi or ethernet (translates to 0.0.0.0)
    };

    // make the connection
    int connection_status = connect(network_socket, (struct sockaddr*) &server_address, sizeof(server_address));
    if (connection_status < 0) {
        perror("There was an error making a conn to the server");
        exit(EXIT_FAILURE);
    }

    char server_response[256] = {0}; // init the whole array to 0s
    int bytes_received = recv(network_socket, server_response, sizeof(server_response) - 1, 0);

    if (bytes_received < 0) {
        perror("Receive failed");
        exit(EXIT_FAILURE);
    }

    printf("The server sent the data: %s\n", server_response);

    close(network_socket);

    return 0;
}
