CMAKE_MINIMUM_REQUIRED(VERSION 2.6)

PROJECT( PAM_MKHOMEDIRS )

SET( POLOCPPBINDING_SRCS
  ${CMAKE_SOURCE_DIR}/src/pam_mkpolohomedir.c
  ${CMAKE_SOURCE_DIR}/src/createpolodir.cpp
  )

SET( TEST_SRCS
	${CMAKE_SOURCE_DIR}/src/createpolodir.cpp
	${CMAKE_SOURCE_DIR}/src/test.cpp
)

FIND_PACKAGE(MarcoCPPBinding)

INCLUDE_DIRECTORIES( "${CMAKE_SOURCE_DIR}/include" )
INCLUDE_DIRECTORIES( ${CMAKE_BINARY_DIR} )
INCLUDE_DIRECTORIES( ${PAM_INCLUDE_DIR} )
INCLUDE_DIRECTORIES( ${OPENSSL_INCLUDE_DIRS})

SET(CMAKE_EXE_LINKER_FLAGS "-Wall -O2")
add_definitions(${CMAKE_EXE_LINKER_FLAGS})

find_package(PkgConfig REQUIRED)

pkg_search_module(OPENSSL REQUIRED openssl)

if( OPENSSL_FOUND )
    include_directories(${OPENSSL_INCLUDE_DIRS})
    message(STATUS "Using OpenSSL ${OPENSSL_VERSION}")
else()
    # Error; with REQUIRED, pkg_search_module() will throw an error by it's own
endif() #http://stackoverflow.com/a/26534464/2628463

ADD_LIBRARY( pam_mkpolohomedir SHARED ${POLOCPPBINDING_SRCS})
SET_TARGET_PROPERTIES( pam_mkpolohomedir PROPERTIES PREFIX "")
TARGET_LINK_LIBRARIES( pam_mkpolohomedir ${PAM_LIBRARIES})
TARGET_LINK_LIBRARIES( pam_mkpolohomedir ${OPENSSL_LIBRARIES})
TARGET_LINK_LIBRARIES( pam_mkpolohomedir ${MARCOCPPBINDING_LIBRARY})

ADD_EXECUTABLE ( test_createdirs ${TEST_SRCS})
TARGET_LINK_LIBRARIES(test_createdirs ${PAM_LIBRARIES})
TARGET_LINK_LIBRARIES ( test_createdirs ${OPENSSL_LIBRARIES})
TARGET_LINK_LIBRARIES(test_createdirs ${MARCOCPPBINDING_LIBRARY})

find_package(RapidJSON)

install(TARGETS pam_mkpolohomedir
      DESTINATION /lib/security)




