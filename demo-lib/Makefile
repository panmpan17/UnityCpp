CXX=g++
CXXWIN=x86_64-w64-mingw32-g++
INCLUDE=-Iinclude
SRC=src/mylib.cpp

all: so dll

so:
	$(CXX) -shared -fPIC $(INCLUDE) $(SRC) -o build/libmylib.so

dll:
	$(CXXWIN) -shared -fPIC $(INCLUDE) $(SRC) -o build/mylib.dll

clean:
	rm -f build/libmylib.so build/mylib.dll
