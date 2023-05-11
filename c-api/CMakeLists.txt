cmake_minimum_required(VERSION 3.19)
project(c-api)

set(CMAKE_CXX_STANDARD 17)

include(FetchContent)

FetchContent_Declare(
        Reference-FMUs

        GIT_REPOSITORY https://github.com/modelica/Reference-FMUs
        GIT_TAG v0.0.23
        GIT_SHALLOW TRUE
)

set(WITH_FMUSIM ON CACHE BOOL "" FORCE)

FetchContent_GetProperties(Reference-FMUs)

FetchContent_Populate(Reference-FMUs)

execute_process(
        COMMAND git apply ${CMAKE_CURRENT_SOURCE_DIR}/patches/cmake.patch
        WORKING_DIRECTORY ${Reference-FMUs_SOURCE_DIR}
#        COMMAND_ERROR_IS_FATAL ANY
)

execute_process(
        COMMAND
        python3 ${Reference-FMUs_SOURCE_DIR}/ThirdParty/build_cvode.py
        python3 ${Reference-FMUs_SOURCE_DIR}/ThirdParty/build_libxml2.py
        python3 ${Reference-FMUs_SOURCE_DIR}/ThirdParty/build_zlib.py
        WORKING_DIRECTORY ${Reference-FMUs_SOURCE_DIR}/ThirdParty
        COMMAND_ERROR_IS_FATAL ANY
)

FetchContent_MakeAvailable(Reference-FMUs)

set(SOURCES
        main.cpp
)

add_executable(run-c-api ${SOURCES})

target_link_libraries(run-c-api fmusim_lib)
