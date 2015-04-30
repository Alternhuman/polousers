#include <stdio.h>
//#include "marcoexception.h"
#include "marcobinding.h"

int main(){
	request_for(L"deployer");
	return 0;
}
// #include <stdio.h>
// #include <stdlib.h>
// #include <iconv.h>
// #include <wchar.h>
// #include "utf8.h"

// #define UTF8_SEQUENCE_MAXLEN 16
/* #define UTF8_SEQUENCE_MAXLEN 16 */

// int
// main2(int argc, char **argv)
// {



//     wchar_t *wcs = L"ABBBB";
//     signed char utf8[(wcslen(wcs) + 1 /* L'\0' */) * UTF8_SEQUENCE_MAXLEN];
//     char *iconv_in = (char *) wcs;
//     char *iconv_out = (char *) &utf8[0];
//     size_t iconv_in_bytes = (wcslen(wcs) + 1 /* L'\0' */) * sizeof(wchar_t);
//     size_t iconv_out_bytes = sizeof(utf8);
//     size_t ret;
    
//     wchar_to_utf8(wcs, iconv_in_bytes, iconv_out, iconv_out_bytes, 0);
//     printf("%s", utf8);
//     return 0;

//     iconv_t cd;
//     //setlocale(LC_CTYPE,"");
//     cd = iconv_open("UTF-8","WCHAR_T");
//     if ((iconv_t) -1 == cd) {
//         perror("iconv_open");
//         return EXIT_FAILURE;
//     }

//     ret = iconv(cd, &iconv_in, &iconv_in_bytes, &iconv_out, &iconv_out_bytes);
//     if ((size_t) -1 == ret) {
//         perror("iconv");
//         return EXIT_FAILURE;
//     }

//     printf("Result: %s %d\n", iconv_out, ret);

//     return EXIT_SUCCESS;
// }
