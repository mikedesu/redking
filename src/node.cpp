#include <arpa/inet.h>
#include <cstdio>
#include <cstdlib>
#include <iostream>
#include <netinet/in.h>
#include <random>
#include <string.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <unistd.h>
#include <unordered_map>

using std::cout;
using std::default_random_engine;
using std::endl;
using std::fixed;
using std::uniform_real_distribution;
using std::unordered_map;

typedef struct {
  size_t ip_addr;
  size_t port;
} neighbor;

default_random_engine rng;
uniform_real_distribution<double> vaddr_dist(0.0, 1.0);
double my_vaddr = -1.0;
unordered_map<double, neighbor> neighbors;

void check_usage(int argc, char *argv[]);
int do_client(char *argv[]);
int do_server(char *argv[]);
void print_my_neighbors();

int main(int argc, char *argv[]) {
  rng.seed(time(NULL));
  my_vaddr = vaddr_dist(rng);
  cout.precision(30);
  check_usage(argc, argv);
  int retval = 0;
  if (argc < 3) {
    retval = do_server(argv);
  } else {
    retval = do_client(argv);
  }
  return retval;
}

int do_client(char *argv[]) {
  char *ipaddr = argv[1];
  int port = atoi(argv[2]);
  cout << "Running as client connecting to port: " << port << endl;
  cout << fixed << "My virtual address: " << my_vaddr << endl;
  // open a socket and connect to the primary server
  int sockfd = socket(AF_INET, SOCK_STREAM, 0);
  if (sockfd < 0) {
    perror("socket");
    return 1;
  }
  struct sockaddr_in addr;
  addr.sin_family = AF_INET;
  addr.sin_port = htons(port);
  addr.sin_addr.s_addr = inet_addr(ipaddr);
  if (connect(sockfd, (struct sockaddr *)&addr, sizeof(addr)) < 0) {
    perror("connect");
    return 1;
  }
  int n = write(sockfd, &my_vaddr, sizeof(my_vaddr));
  if (n < 0) {
    perror("write");
    return 1;
  }
  close(sockfd);
  return 0;
}

void check_usage(int argc, char *argv[]) {
  if (argc < 3) {
    if (argc < 2) {
      cout << "Usage: " << argv[0] << " <port>" << endl;
      exit(1);
    }
    int port = atoi(argv[1]);
    if (port < 0) {
      cout << "Invalid port number" << endl;
      exit(1);
    }
  }
}

int do_server(char *argv[]) {
  int port = atoi(argv[1]);
  if (port < 0) {
    cout << "Invalid port number" << endl;
    return 1;
  }
  int connfd = -1;
  int n = -1;
  struct sockaddr_in addr;
  cout << "Running as primary server on port " << port << endl;
  cout << "vaddr: " << my_vaddr << endl;
  // open a socket and listen for incoming connections
  int sockfd = socket(AF_INET, SOCK_STREAM, 0);
  if (sockfd < 0) {
    perror("socket");
    return 1;
  }
  addr.sin_family = AF_INET;
  addr.sin_port = htons(port);
  addr.sin_addr.s_addr = INADDR_ANY;
  if (bind(sockfd, (struct sockaddr *)&addr, sizeof(addr)) < 0) {
    perror("bind");
    return 1;
  }
  // listen for incoming connections
  if (listen(sockfd, 10) < 0) {
    perror("listen");
    return 1;
  }
  // wait for a connection
  while (true) {
    connfd = accept(sockfd, NULL, NULL);
    if (connfd < 0) {
      perror("accept");
      return 1;
    }
    double connecting_vaddr = -1.0;
    struct sockaddr_in peer_addr;
    socklen_t peer_addr_len = sizeof(peer_addr);
    // read the virtual address of the connecting node
    n = read(connfd, &connecting_vaddr, sizeof(connecting_vaddr));
    if (n < 0) {
      perror("read");
      return 1;
    }
    getpeername(connfd, (struct sockaddr *)&peer_addr, &peer_addr_len);
    close(connfd);
    cout << "connecting: " << inet_ntoa(peer_addr.sin_addr) << ":"
         << ntohs(peer_addr.sin_port) << " vaddr: " << connecting_vaddr << endl;
    neighbors[connecting_vaddr] = {peer_addr.sin_addr.s_addr,
                                   ntohs(peer_addr.sin_port)};
    // print out the list of neighbors
    print_my_neighbors();
  }
  close(sockfd);
  return 0;
}

void print_my_neighbors() {
  cout << "neighbors:" << endl;
  for (auto &neighbor : neighbors) {
    cout << fixed << neighbor.first << " "
         << inet_ntoa(*(struct in_addr *)&neighbor.second.ip_addr) << " "
         << neighbor.second.port << endl;
  }
}
