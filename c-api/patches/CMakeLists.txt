cmake_minimum_required(VERSION 3.17)
project(FMUSim)

include(FetchContent)

###############################
# Add cvode
###############################

set(BUILD_TESTING OFF CACHE BOOL "" FORCE)
set(EXAMPLES_INSTALL OFF CACHE BOOL "" FORCE)

FetchContent_Declare(
        cvode_dep
        GIT_REPOSITORY https://github.com/LLNL/sundials
        GIT_TAG v6.4.1
)

FetchContent_MakeAvailable(cvode_dep)

###############################
# Add libxml2
###############################

set(BUILD_SHARED_LIBS OFF CACHE BOOL "" FORCE)
set(LIBXML2_WITH_ICONV OFF CACHE BOOL "" FORCE)
set(LIBXML2_WITH_LZMA OFF CACHE BOOL "" FORCE)
set(LIBXML2_WITH_PYTHON OFF CACHE BOOL "" FORCE)
set(LIBXML2_WITH_ZLIB OFF CACHE BOOL "" FORCE)

FetchContent_Declare(
        libxml2_dep
        GIT_REPOSITORY https://github.com/GNOME/libxml2
        GIT_TAG v2.10.3
)

FetchContent_MakeAvailable(libxml2_dep)

###############################
# Add zlib
###############################

FetchContent_Declare(
        zlib_dep
        GIT_REPOSITORY https://github.com/madler/zlib
        GIT_TAG v1.2.13
)

FetchContent_MakeAvailable(zlib_dep)

###############################
# Create target fmusim_lib
###############################

set(SOURCES
        ../include/FMI.h
        ../src/FMI.c
        ../include/FMI1.h
        ../src/FMI1.c
        ../include/FMI2.h
        ../src/FMI2.c
        ../include/FMI3.h
        ../src/FMI3.c
        csv.h
        csv.c
        FMIUtil.h
        FMIUtil.c
        FMISolver.h
        FMIEuler.h
        FMIEuler.c
        FMICVode.h
        FMICVode.c
        FMIModelDescription.h
        FMIModelDescription.c
        FMIRecorder.h
        FMIRecorder.c
        FMIZip.h
        FMIZip.c
        fmi1schema.h
        fmi2schema.h
        fmi3schema.h
        fmusim_fmi1_cs.h
        fmusim_fmi1_cs.c
        fmusim_fmi1_me.h
        fmusim_fmi1_me.c
        fmusim_fmi2_cs.h
        fmusim_fmi2_cs.c
        fmusim_fmi2_me.h
        fmusim_fmi2_me.c
        fmusim_fmi3_cs.h
        fmusim_fmi3_cs.c
        fmusim_fmi3_me.h
        fmusim_fmi3_me.c
        fmusim_input.h
        fmusim_input.c
        miniunzip.c
        ${zlib_SOURCE_DIR}/contrib/minizip/ioapi.c
        ${zlib_SOURCE_DIR}/contrib/minizip/unzip.c
)

add_library(fmusim_lib STATIC ${SOURCES})

target_include_directories(fmusim_lib
        PUBLIC
        .
        ../include

        PRIVATE
        ${zlib_SOURCE_DIR}/contrib/minizip
        ${libxml2_BINARY_DIR}
        ${libxml2_SOURCE_DIR}/include
        ${cvode_BINARY_DIR}/include
        ${cvode_SOURCE_DIR}/include
)

target_link_libraries(fmusim_lib PRIVATE SUNDIALS::cvode_static LibXml2::LibXml2 zlibstatic)
