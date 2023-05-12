cmake_minimum_required(VERSION 3.19)
project(c-api)

set(CMAKE_CXX_STANDARD 17)

include(FetchContent)

###############################
# Add fmusim_lib
###############################

set(WITH_FMUSIM ON CACHE BOOL "" FORCE)

FetchContent_Declare(
        fmusim_lib_dep
        GIT_REPOSITORY https://github.com/modelica/Reference-FMUs
        GIT_TAG v0.0.23
        PATCH_COMMAND cmake -E copy "${CMAKE_CURRENT_LIST_DIR}/patches/CMakeLists.txt" "fmusim"
)

FetchContent_MakeAvailable(fmusim_lib_dep)

###############################
# Create target run_c_api
###############################

set(SOURCES
        main.cpp)

add_executable(run_c_api ${SOURCES})

target_link_libraries(run_c_api fmusim_lib)
