cmake_minimum_required(VERSION 3.19)
project(c-api)

set(CMAKE_CXX_STANDARD 17)
#set(CMAKE_C_STANDARD 11)

set(WITH_FMUSIM ON CACHE BOOL "" FORCE)

add_subdirectory(Reference-FMUs)

set(SOURCES
        main.cpp
)

add_executable(run-c-api ${SOURCES})

if(TARGET fmusim_lib)
    message("fmusim_lib is available")
else()
    message("fmusim_lib is not available")
endif()


target_link_libraries(run-c-api fmusim_lib)
