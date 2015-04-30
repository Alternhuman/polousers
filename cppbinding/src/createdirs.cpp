#include "marcoexception.h"
#include "conf.h"

#include <stdio.h>
#include <strings.h>

#include <string>
#include <vector>

#include <sys/socket.h>
#include <stdio.h>
#include <netinet/in.h>
#include <arpa/inet.h>

#include "rapidjson/document.h"
#include "rapidjson/writer.h"
#include "rapidjson/stringbuffer.h"
#include "rapidjson/prettywriter.h"

using namespace std;

int createdirs(string home, int uid, int gid){

	int sd = socket(AF_INET, SOCK_DGRAM, 0);
	struct sockaddr_in poloserver;
	size_t size_addr = sizeof(poloserver);
	//std::vector<string> nodes = request_for(L"deployer"); //TODO: change to "polousers"

	std::vector<string> nodes;
	nodes.push_back("127.0.1.1");

	if (sd < 0){
		perror("Internal error when opening connection to Marco");
		throw marcoexception("Internal error when opening connection to Marco");
	}

	for(int i=0; i<nodes.size();i++){
		bzero((char *) &poloserver, sizeof(poloserver));

		poloserver.sin_family = AF_INET;
		poloserver.sin_port = htons(USERS_PORT);
		poloserver.sin_addr.s_addr = inet_addr(nodes[i].c_str());
		
		rapidjson::Document writer;
		rapidjson::Document::AllocatorType& allocator = writer.GetAllocator();

		writer.SetObject();
		
		rapidjson::Value Command(rapidjson::kStringType);
		Command.SetString("Create-Home");
		writer.AddMember("Command", Command, allocator);
		
		char aux[BUFFSIZE];
		int len = sprintf(aux, "%s,%d,%d", home.c_str(), uid, gid);
		char aux2[len];
		strcpy(aux2, aux);

		rapidjson::Value Params(rapidjson::kStringType);
		Params.SetString(aux2,len);
		writer.AddMember("Params", Params, allocator);

		rapidjson::StringBuffer buffer;
		rapidjson::Writer<rapidjson::StringBuffer> salida(buffer);
		writer.Accept(salida);

		string data =  buffer.GetString();
		char data_arr[data.size()];
		memcpy(data_arr, data.c_str(), data.size());
		sendto(sd,data_arr,sizeof(data_arr),0,(struct sockaddr *)&poloserver,size_addr);

	}

}

int main(){
	return 0;
}