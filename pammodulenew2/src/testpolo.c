#include "testpolo.h"
#include <stdio.h>
#include <strings.h>
#include <string.h>
#include <sys/socket.h>
#include <stdio.h>
#include <netinet/in.h>
#include <arpa/inet.h>

int testpolo(){
	int sd = socket(AF_INET, SOCK_DGRAM, 0);
	struct sockaddr_in poloserver;
	size_t size_addr = sizeof(poloserver);

	if (sd < 0){
		perror("Internal error when opening connection to Marco");
		return -1;
	}

	bzero((char *) &poloserver, sizeof(poloserver));

	poloserver.sin_family = AF_INET;
	poloserver.sin_port = htons(1343);
	poloserver.sin_addr.s_addr = inet_addr("172.20.1.56");

	char data_arr[100];
	strcpy(data_arr, "Hola");
	sendto(sd,data_arr,sizeof(data_arr),0,(struct sockaddr *)&poloserver,size_addr);
 

 return 0;
}


/*int main(){
	testpolo();
}*/