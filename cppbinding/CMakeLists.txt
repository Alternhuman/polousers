CMAKE_MINIMUM_REQUIRED(VERSION 2.6)

PROJECT( POLOCPPBINDING )

SET( POLOCPPBINDING_SRCS
  ${CMAKE_SOURCE_DIR}/src/test.cpp
  ${CMAKE_SOURCE_DIR}/src/marcobinding.cpp
  ${CMAKE_SOURCE_DIR}/src/marcoexception.cpp
  ${CMAKE_SOURCE_DIR}/src/JSON.cpp
  ${CMAKE_SOURCE_DIR}/src/JSONValue.cpp
  ${CMAKE_SOURCE_DIR}/src/utf8.c

  )

# SET(BIN_INSTALL_DIR
#     "/bin"
#     CACHE PATH "The subdirectory relative to the install prefix for executables (default is bin)"
#    )

#SET(CMAKE_MODULE_PATH "${CMAKE_SOURCE_DIR}/cmake/modules/")
#ADD_DEFINITIONS (-DVERSION='"${VERSION}"' -DPKGDATADIR=\"${PKGDATADIR}\" -DBINDIR=\"${BINDIR}\")
#ADD_DEFINITIONS (-DVERSION='"${VERSION}"' -DPKGDATADIR=\"${PKGDATADIR}\" -DBINDIR=\"${BINDIR}\")

INCLUDE_DIRECTORIES( "${CMAKE_SOURCE_DIR}/include" )
INCLUDE_DIRECTORIES( ${CMAKE_BINARY_DIR} )

ADD_EXECUTABLE( marcobinding ${POLOCPPBINDING_SRCS})
find_package(RapidJSON)
# INSTALL(
#      TARGETS
#      marcobinding
#      DESTINATION
#      /lib/security/
# )

# SET( PAM_FACE_AUTHENTICATE_SRCS
#      ${CMAKE_SOURCE_DIR}/src/pam_face_authentication.cpp
#      ${CMAKE_SOURCE_DIR}/src/opencvWebcam.cpp
#      ${CMAKE_SOURCE_DIR}/src/detector.cpp
#      ${CMAKE_SOURCE_DIR}/src/faceDetector.cpp
#      ${CMAKE_SOURCE_DIR}/src/eyesDetector.cpp
#      ${CMAKE_SOURCE_DIR}/src/webcamImagePaint.cpp
#      ${CMAKE_SOURCE_DIR}/src/tracker.cpp
#      ${CMAKE_SOURCE_DIR}/src/verifier.cpp
#      ${CMAKE_SOURCE_DIR}/src/utils.cpp
#    )



# SET(BIN_INSTALL_DIR
#     "/bin"
#     CACHE PATH "The subdirectory relative to the install prefix for executables (default is bin)"
#    )

# SET(DATA_INSTALL_DIR
#     "/share"
#     CACHE PATH "The subdirectory relative to the install prefix where shared data will be installed (default is share)."
#    )





#ADD_LIBRARY(pam_face_authentication SHARED ${PAM_FACE_AUTHENTICATE_SRCS})
#SET_TARGET_PROPERTIES( pam_face_authentication PROPERTIES PREFIX "")

#TARGET_LINK_LIBRARIES( xwindowFaceAuth ${X11_LIBRARIES})

#ADD_EXECUTABLE( qt-facetrainer ${QT_FACETRAINER_SRCS} ${QT_FACETRAINER_MOC_SRCS} ${QT_FACETRAINER_RC_SRCS} ${QT_FACETRAINER_UI_HDRS} )
#TARGET_LINK_LIBRARIES( pam_face_authentication  ${PAM_LIBRARIES} ${OPENCV_LIBRARIES})
#TARGET_LINK_LIBRARIES( qt-facetrainer ${QT_LIBRARIES} ${OPENCV_LIBRARIES})
 


# INSTALL(
#     TARGETS
#     pam_face_authentication
#     DESTINATION
#     /lib/security/
# )

# INSTALL(
#     TARGETS
#     qt-facetrainer
#     DESTINATION
#     ${BINDIR}
# )

# INSTALL(
#     TARGETS
#     xwindowFaceAuth
#     DESTINATION
#     ${XWINDOW_BINDIR}
# )

# INSTALL(
#     FILES
#     ${HAAR_CASCADES}
#     DESTINATION
#     ${PKGDATADIR}
# )

# INSTALL(
#     FILES
#     ${APP_ICON}
#     DESTINATION
#     ${PKGDATADIR}/icons/
# )

# INSTALL( FILES ${CMAKE_CURRENT_BINARY_DIR}/${DESKTOP_ENTRY} DESTINATION ${PKGDATADIR}/applications )

