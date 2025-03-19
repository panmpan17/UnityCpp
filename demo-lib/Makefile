CXX=g++
CXXWIN=x86_64-w64-mingw32-g++
AR=ar
INCLUDE=-Iinclude

# Source files
SRC_DIR=src
SRC=src/mylib.cpp


# Output
BUILD_DIR =build
SO_OUT    =$(BUILD_DIR)/libmylib.so
DYLIB_OUT =$(BUILD_DIR)/libmylib.dylib
DLL_OUT   =$(BUILD_DIR)/mylib.dll
O_OUT     =$(BUILD_DIR)/mylib.o
STATIC_OUT=$(BUILD_DIR)/libmylib.a

# Flags
CXXFLAGS=-fPIC
LDFLAGS=-shared


all: so dylib dll static

so:
	@mkdir -p $(BUILD_DIR)
	$(CXX) $(CXXFLAGS) $(INCLUDE) $(SRC) $(LDFLAGS) -o $(SO_OUT)
	@echo "Built shared library: $(SO_OUT)"

dylib:
	@mkdir -p $(BUILD_DIR)
	$(CXX) $(CXXFLAGS) $(INCLUDE) $(SRC) $(LDFLAGS) -o $(DYLIB_OUT)
	@echo "Built shared library: $(DYLIB_OUT)"

dll:
	@mkdir -p $(BUILD_DIR)
	$(CXXWIN) $(CXXFLAGS) $(INCLUDE) $(SRC) -shared -o $(DLL_OUT)
	@echo "Built shared library: $(DLL_OUT)"

static:
	@mkdir -p $(BUILD_DIR)
	$(CXX) $(CXXFLAGS) $(INCLUDE) -c $(SRC) -o $(O_OUT)
	$(AR) rcs $(STATIC_OUT) $(O_OUT)
	@echo "Built static library: $(STATIC_OUT)"

clean:
	rm -rf $(BUILD_DIR)
	@echo "Cleaned up"
