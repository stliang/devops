# Using CMake with gcov

After cloning this directory, an "out-of-source build" is recommended to
test the project. To perform an out-of-source build, run the following commands
from the project root directory:

```
mkdir build
cd build
cmake ..
make gcov
```

From the build directory you may build the project using `make`. The coverage
files from gcov can be generated using `make gcov`. A summary of the two source
files will be output and stored in `build/coverage/TestHello.tmp`. Running
`make clean` will remove the enitre coverage directory.

Run on docker
```
nerdctl run -v $(pwd):/home/Workspace/devops -it local/ubuntu:20.04 bash
```

# Sample output
```
root@417eaeb5e7b9:/home/Workspace/devops# mkdir build
root@417eaeb5e7b9:/home/Workspace/devops# cd build/
root@417eaeb5e7b9:/home/Workspace/devops/build# cmake ..
-- The CXX compiler identification is GNU 9.4.0
-- Check for working CXX compiler: /usr/lib/ccache/c++
-- Check for working CXX compiler: /usr/lib/ccache/c++ -- works
-- Detecting CXX compiler ABI info
-- Detecting CXX compiler ABI info - done
-- Detecting CXX compile features
-- Detecting CXX compile features - done
-- Object files will be output to: /home/Workspace/devops/build/CMakeFiles/tests.dir
-- Source files location: /home/Workspace/devops/src
-- Found GTest: /usr/local/lib/cmake/GTest/GTestConfig.cmake (found version "1.12.1")  
-- Configuring done
-- Generating done
-- Build files have been written to: /home/Workspace/devops/build
root@417eaeb5e7b9:/home/Workspace/devops/build# make gcov
Scanning dependencies of target tests
[ 25%] Building CXX object CMakeFiles/tests.dir/tests/foo_test.o
[ 50%] Building CXX object CMakeFiles/tests.dir/tests/bar_test.o
[ 75%] Building CXX object CMakeFiles/tests.dir/src/Adder.o
[100%] Linking CXX executable tests
[100%] Built target tests
Scanning dependencies of target gcov
Running tests...
Test project /home/Workspace/devops/build
    Start 1: Foo.Adder_add
1/3 Test #1: Foo.Adder_add ....................   Passed    0.05 sec
    Start 2: Foo.Adder_clear
2/3 Test #2: Foo.Adder_clear ..................   Passed    0.06 sec
    Start 3: Bar.Sum
3/3 Test #3: Bar.Sum ..........................   Passed    0.05 sec

100% tests passed, 0 tests failed out of 3

Total Test time (real) =   0.21 sec
=================== GCOV ====================
File '/home/Workspace/devops/src/Adder.cpp'
Lines executed:100.00% of 10
No branches
No calls
Creating 'Adder.cpp.gcov'

File '/usr/include/c++/9/iostream'
No executable lines
No branches
No calls
-- Coverage files have been output to /home/Workspace/devops/build/coverage
[100%] Built target gcov
root@417eaeb5e7b9:/home/Workspace/devops/build# ./tests 
Running main() from /opt/googletest/googletest/src/gtest_main.cc
[==========] Running 3 tests from 2 test suites.
[----------] Global test environment set-up.
[----------] 2 tests from Foo
[ RUN      ] Foo.Adder_add
[       OK ] Foo.Adder_add (1 ms)
[ RUN      ] Foo.Adder_clear
[       OK ] Foo.Adder_clear (0 ms)
[----------] 2 tests from Foo (1 ms total)

[----------] 1 test from Bar
[ RUN      ] Bar.Sum
[       OK ] Bar.Sum (0 ms)
[----------] 1 test from Bar (0 ms total)

[----------] Global test environment tear-down
[==========] 3 tests from 2 test suites ran. (5 ms total)
[  PASSED  ] 3 tests.

```

In Jenkins' job Console Output page, we should see the include and exclude rules application and the resulting number of files indexed for analysis. 
```
INFO:   Included sources: src/*.cpp, src/*.h
INFO:   Excluded sources: **/*.g.cs, **/*.ascx.g.cs, **/modernizr-custom-build-2.6.2.js, **/*.g.cs, **/*.ascx.g.cs
INFO: 2 files indexed
```

# Reference
- [install googletest and use with CMakeLists.txt](https://tttapa.github.io/Pages/Ubuntu/Software-Installation/GoogleTest.html)
- [simple cmake googletest](https://stackoverflow.com/questions/50861636/using-google-tests-with-cmake-ctest-with-the-new-command-gtest-discover-tests)
