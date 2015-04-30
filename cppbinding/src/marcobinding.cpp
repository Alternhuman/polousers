
#include <iostream>
#include <exception>
#include <vector>

#include <sys/socket.h>
#include <stdio.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <strings.h>
#include "JSON.h"
#include "JSONValue.h"
#include <sstream>
#include <string>

#include <string>
#include <iterator>
#include <stdlib.h>
#include <iconv.h>

#include "utf8.h"

#include "rapidjson/document.h"
#include "rapidjson/writer.h"
#include "rapidjson/stringbuffer.h"
#define UTF8_SEQUENCE_MAXLEN 8
using namespace std;

int request_for(wchar_t* service){
	int sd = socket(AF_INET, SOCK_DGRAM, 0);
	struct sockaddr_in bind_addr;

	if (sd < 0){
		perror("Internal error when opening connection to Marco");
		//throw marcoexception("Internal error when opening connection to Marco");
	}

	bzero((char *) &bind_addr, sizeof(bind_addr));

	bind_addr.sin_family = AF_INET;
	bind_addr.sin_port = htons(1358);
	bind_addr.sin_addr.s_addr = inet_addr("127.0.1.1");

	socklen_t m = sizeof(bind_addr);

	JSONObject j;
	j[L"Command"] = new JSONValue(L"Request-For");
	j[L"Params"] = new JSONValue(service);

	JSONValue *value = new JSONValue(j);

	//printf("%ls", value->Stringify().c_str());
	


	const wchar_t *wcs = value->Stringify().c_str();
    signed char utf8[(wcslen(wcs) + 1 /* L'\0' */) * UTF8_SEQUENCE_MAXLEN];
    char *iconv_in = (char *) wcs;
    char *iconv_out = (char *) &utf8[0];
    size_t iconv_in_bytes = (wcslen(wcs) + 1 /* L'\0' */) * sizeof(wchar_t);
    size_t iconv_out_bytes = sizeof(utf8);
    size_t ret;
    
    size_t b = wchar_to_utf8(wcs, iconv_in_bytes, iconv_out, iconv_out_bytes, 0);
    if(b < 1){
    	perror("Internal error during UTF-8 conversion");
    }
    sendto(sd,iconv_out,(b/4)-1,0,(struct sockaddr *)&bind_addr,m);
    
    char recv_response[250];
    size_t response = recv(sd, recv_response, 250,0);

    wchar_t to_arr[response];
    char to_arr_aux[response];
    strncpy(to_arr_aux, recv_response, response);
    
    printf("%s", to_arr_aux);
    
    size_t c = utf8_to_wchar(to_arr_aux, response, to_arr, response, 0);
    
    string str = to_arr_aux;
    
    rapidjson::Document document;
    if(document.Parse<0>(str.c_str()).HasParseError())
    	printf("Error\n");
    else
    	printf("No. Size: %d\n", document.Size());
    assert(document.IsArray());

    for(int i= 0; i<document.Size();i++){
    	printf("%s", document[i]["Address"][0].GetString());
    }

/*	rapidjson::GenericDocument<rapidjson::UTF8 <>> d;
 	char buffer[sizeof(to_arr_aux)];
    memcpy(buffer, to_arr_aux, sizeof(to_arr_aux));
    
    if (d.ParseInsitu(buffer).HasParseError()){
        printf("Error");
        return 1;
    }*/

    
    /*d.Parse(recv_response);
    printf("%d",d.Size());*/

/*
    JSONValue *jresponse = JSON::Parse(to_arr);
    if(jresponse == NULL){
    	printf("Error");
    }
    //printf(jresponse->IsObject() ?  "Si" : "No");
    printf("%s\n--------------------------\n", recv_response);
    printf("%ls", to_arr);*/

}