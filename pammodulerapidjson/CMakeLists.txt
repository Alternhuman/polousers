CMAKE_MINIMUM_REQUIRED(VERSION 2.6)

PROJECT( POLOCPPBINDING )

SET( POLOCPPBINDING_SRCS
  #${CMAKE_SOURCE_DIR}/src/pam_mkpolohomedir.c
  ${CMAKE_SOURCE_DIR}/src/testpolo.cpp
#  ${CMAKE_SOURCE_DIR}/src/createdirs.cpp
#  ${CMAKE_SOURCE_DIR}/src/marcobinding.cpp
#  ${CMAKE_SOURCE_DIR}/src/marcoexception.cpp
  )

INCLUDE_DIRECTORIES( "${CMAKE_SOURCE_DIR}/include" )
INCLUDE_DIRECTORIES( ${CMAKE_BINARY_DIR} )
#INCLUDE_DIRECTORIES( ${PAM_INCLUDE_DIR} )
INCLUDE_DIRECTORIES( ${OPENSSL_INCLUDE_DIRS})

find_package(PkgConfig REQUIRED)

pkg_search_module(OPENSSL REQUIRED openssl)

if( OPENSSL_FOUND )
    include_directories(${OPENSSL_INCLUDE_DIRS})
    message(STATUS "Using OpenSSL ${OPENSSL_VERSION}")
else()
    # Error; with REQUIRED, pkg_search_module() will throw an error by it's own
endif() #http://stackoverflow.com/a/26534464/2628463

ADD_EXECUTABLE( marcobindingtest ${POLOCPPBINDING_SRCS})
TARGET_LINK_LIBRARIES(marcobindingtest ${OPENSSL_LIBRARIES})

#ADD_LIBRARY( pam_mkpolohomedir SHARED ${POLOCPPBINDING_SRCS})
#SET_TARGET_PROPERTIES( pam_mkpolohomedir PROPERTIES PREFIX "")
#TARGET_LINK_LIBRARIES( pam_mkpolohomedir ${PAM_LIBRARIES})
find_package(RapidJSON)
