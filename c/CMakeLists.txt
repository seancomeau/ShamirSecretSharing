cmake_minimum_required(VERSION 2.8)

project(ShamirSecretSharing)

include(CTest)

find_path(GMP_INCLUDE_DIR NAMES gmp.h)
if(NOT GMP_INCLUDE_DIR)
    message(FATAL_ERROR "libgmp header files could not be found!")
endif()
find_library(GMP_LIBRARIES gmp)
if(NOT EXISTS ${GMP_LIBRARIES})
    message(FATAL_ERROR "libgmp library could not be found!")
endif()

include_directories(${GMP_INCLUDES})

set(CMAKE_C_FLAGS "-std=c89 -Wall -Wextra -Werror")
include_directories(src)

add_library(shamir STATIC src/shamir.c)

add_executable(test1 tests/test1.c)
target_link_libraries(test1 shamir gmp)

add_test(NAME test_test1 COMMAND test1)
set_tests_properties(test_test1 PROPERTIES DEPENDS test1)

install(FILES src/shamir.h DESTINATION include)
install(TARGETS shamir DESTINATION lib)
