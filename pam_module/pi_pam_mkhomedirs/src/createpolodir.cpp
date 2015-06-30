extern "C"{
    #include "createpolodir.h"
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

#include <resolv.h>

#include <openssl/bio.h>
#include <openssl/ssl.h>
#include <openssl/err.h>
#include <openssl/pem.h>
#include <openssl/x509.h>
#include <openssl/x509_vfy.h>
#include <openssl/evp.h>

#include <marcopolo/marco.hpp>

#define BUFFSIZE 400
#define PORT 1343
#define ROOTCA "/etc/polohomedir/certs/rootCA.pem"
#define CLIENT_CRT "/etc/polohomedir/certs/client.crt"
#define CLIENT_KEY "/etc/polohomedir/certs/client.key"

extern "C" int createdirectory(const char* home, int uid, int gid, const char* address_host){

    //BIO              *certbio = NULL;
    BIO               *outbio = NULL;
    //X509                *cert = NULL;
    //X509_NAME       *certname = NULL;
    const SSL_METHOD *method;
    SSL_CTX *ctx;
    SSL *ssl;

    OpenSSL_add_all_algorithms();
    ERR_load_BIO_strings();
    ERR_load_crypto_strings();
    SSL_load_error_strings();

    //certbio = BIO_new(BIO_s_file());
    outbio  = BIO_new_fp(stdout, BIO_NOCLOSE);

    if(SSL_library_init() < 0)
        BIO_printf(outbio, "Could not initialize the OpenSSL library !\n");

    /* ---------------------------------------------------------- *
    * Set SSLv2 client hello, also announce SSLv3 and TLSv1      *
    * ---------------------------------------------------------- */
    method = SSLv23_client_method();

    /* ---------------------------------------------------------- *
    * Try to create a new SSL context                            *
    * ---------------------------------------------------------- */
    if ( (ctx = SSL_CTX_new(method)) == NULL)
        BIO_printf(outbio, "Unable to create a new SSL context structure.\n");

    /* ---------------------------------------------------------- *
    * Disabling SSLv2 will leave v3 and TSLv1 for negotiation    *
    * ---------------------------------------------------------- */
    // SSL_CTX_set_options(ctx, SSL_OP_NO_SSLv2);
    if (!SSL_CTX_load_verify_locations(ctx, ROOTCA, NULL))
    {
        ERR_print_errors_fp(stderr);
        abort();
    }

    /* set the local certificate from CertFile */
    if ( SSL_CTX_use_certificate_file(ctx, CLIENT_CRT, SSL_FILETYPE_PEM) <= 0 )
    {
        ERR_print_errors_fp(stderr);
        
        abort();
    }
    /* set the private key from KeyFile (may be the same as CertFile) */
    if ( SSL_CTX_use_PrivateKey_file(ctx, CLIENT_KEY, SSL_FILETYPE_PEM) <= 0 )
    {
        ERR_print_errors_fp(stderr);
        abort();
    }
    /* verify private key */
    if ( !SSL_CTX_check_private_key(ctx) )
    {
        fprintf(stderr, "Private key does not match the public certificate\n");
        abort();
    }
    SSL_CTX_set_verify(ctx, SSL_VERIFY_PEER|SSL_VERIFY_FAIL_IF_NO_PEER_CERT, NULL);

    SSL_CTX_set_verify_depth(ctx, 1);

    /* ---------------------------------------------------------- *
    * Create new SSL connection state object                     *
    * ---------------------------------------------------------- */
    ssl = SSL_new(ctx);

    int sd = socket(AF_INET, SOCK_STREAM, 0);
    struct sockaddr_in poloserver;
    size_t size_addr = sizeof(poloserver);

    if (sd < 0){
        perror("Internal error when opening connection to Marco");
        return -1;
    }

    bzero((char *) &poloserver, sizeof(poloserver));

    poloserver.sin_family = AF_INET;
    poloserver.sin_port = htons(PORT);
    poloserver.sin_addr.s_addr = inet_addr(address_host);

    if(-1 == connect(sd, (sockaddr*)&poloserver, size_addr)){
        perror("Fail");
        return -1;
    }

    SSL_set_fd(ssl, sd);

    if ( SSL_connect(ssl) != 1 )
        BIO_printf(outbio, "Error: Could not build a SSL session");
    else
        BIO_printf(outbio, "Successfully enabled SSL/TLS session\n");

    rapidjson::Document writer;
    rapidjson::Document::AllocatorType& allocator = writer.GetAllocator();
    writer.SetObject();
        
    rapidjson::Value Command(rapidjson::kStringType);
    Command.SetString("Create-Home");
    writer.AddMember("Command", Command, allocator);

    char aux[BUFFSIZE];

    int len = sprintf(aux, "%s,%d,%d", home, uid, gid);
    char aux2[len];
    strcpy(aux2, aux);

    rapidjson::Value Params(rapidjson::kStringType);
    Params.SetString(aux2,len);
    writer.AddMember("Params", Params, allocator);

    rapidjson::StringBuffer buffer;
    rapidjson::Writer<rapidjson::StringBuffer> salida(buffer);
    writer.Accept(salida);

    std::string data =  buffer.GetString();
    char data_arr[data.size()];
    memcpy(data_arr, data.c_str(), data.size());

    SSL_write(ssl, data_arr, sizeof(data_arr));
    char buf_recv[500];
    len = SSL_read(ssl, buf_recv, sizeof(buf_recv));

    char aux3[len];
    if (len > 0){
        strncpy(aux3, buf_recv, len);
        printf("%s\n", aux3);
    }
    
    return 0;
}

extern "C" int create_polo_directories(const char* home, int uid, int gid){

    std::vector<Node> nodes;
    Marco marco;
    marco.request_for(nodes, "polousers");

    for (unsigned int i = 0; i < nodes.size(); i++)
    {
        createdirectory(home, uid, gid, nodes[i].getAddress().c_str());
    }
    return 0;
}

