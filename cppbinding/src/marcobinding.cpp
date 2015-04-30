
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
	bind_addr.sin_port = htons(1348);
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
    recv(sd, iconv_out, iconv_out_bytes,0);
    

    /*wchar_t * to_arr;
    size_t c = wchar_to_utf8(iconv_out, iconv_out_bytes, to_arr, iconv_in_bytes, 0);
*/
    printf("%ls", iconv_out);

}