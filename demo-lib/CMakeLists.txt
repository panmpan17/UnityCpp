cmake_minimum_required(VERSION 3.10)
project(DemoLib)

# Let user specify the build type
if (NOT CMAKE_BUILD_TYPE)
    set(CMAKE_BUILD_TYPE Release)
endif()

# Include directories
include_directories(${CMAKE_SOURCE_DIR}/include)

# Source files
file(GLOB_RECURSE SOURCES "src/*.cpp")


# Platform-specific settings
if (WIN32)

else ()
    set(LIB_NAME "demo-lib")
    add_library(${LIB_NAME} SHARED ${SOURCES})
    set_target_properties(${LIB_NAME} PROPERTIES
        LIBRARY_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib
    )
endif()
