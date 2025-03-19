#ifdef _WIN32
  #define API __declspec(dllexport)
#else
  #define API
#endif

extern "C" {
    API int add(int a, int b);
}
