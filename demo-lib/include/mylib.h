#ifdef _WIN32
  #define EXTERN_C_API __declspec(dllexport)
#else
  #define EXTERN_C_API
#endif

extern "C" {
    /**
     * Add two integers together
     * @param a First integer
     * @param b Second integer
     * @return The sum of the two integers
     */
    EXTERN_C_API int add(int a, int b);

    // Subtract two integers
    EXTERN_C_API int subtract(int a, int b);

    /**  Multiply two integer **/
    EXTERN_C_API int multiply(int a, int b);

    // Divide two integers
    // return a // b
    EXTERN_C_API int divide(int a, int b);
}
