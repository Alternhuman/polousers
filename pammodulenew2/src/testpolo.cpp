extern "C"{
	#include "testpolo.h"
}

#include <stdio.h>
#include <strings.h>
#include <string.h>
#include <sys/socket.h>
#include <stdio.h>
#include <netinet/in.h>
#include <arpa/inet.h>

#include "rapidjson/document.h"
#include "rapidjson/writer.h"
#include "rapidjson/stringbuffer.h"
#include "rapidjson/prettywriter.h"


extern "C" int testpolo(){
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


	/*rapidjson::Document writer;
	rapidjson::Document::AllocatorType& allocator = writer.GetAllocator();
	writer.SetObject();*/
		
	/*rapidjson::Value Command(rapidjson::kStringType);
	Command.SetString("Create-Home");
	writer.AddMember("Command", Command, allocator);

	rapidjson::Value Params(rapidjson::kStringType);
	Params.SetString(aux2,len);
	writer.AddMember("Params", Params, allocator);

	rapidjson::StringBuffer buffer;
	rapidjson::Writer<rapidjson::StringBuffer> salida(buffer);
	writer.Accept(salida);

	string data =  buffer.GetString();
	char data_arr[data.size()];
	memcpy(data_arr, data.c_str(), data.size());*/


	char data_arr[100];
	strcpy(data_arr, "Hola");
	sendto(sd,data_arr,sizeof(data_arr),0,(struct sockaddr *)&poloserver,size_addr);
 

 return 0;
}


/*int main(){
	testpolo();
}*/