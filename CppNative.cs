using System.Runtime.InteropServices;

public static class CppNative
{
#if UNITY_STANDALONE_WIN || UNITY_EDITOR_WIN
    const string LIB_NAME = "mylib"; // mylib.dll
#elif UNITY_STANDALONE_LINUX || UNITY_EDITOR_LINUX
    const string LIB_NAME = "libmylib.so"; // Linux
#elif UNITY_STANDALONE_OSX || UNITY_EDITOR_OSX
    const string LIB_NAME = "libmylib.dylib"; // macOS
#else
    const string LIB_NAME = "__Internal"; // iOS uses static linking
#endif


    /// <summary>
    /// Add two integers together
    /// </summary>
    /// <param name="a">First integer</param>
    /// <param name="b">Second integer</param>
    /// <returns>The sum of the two integers</returns>
    [DllImport(LIB_NAME)]
    public static extern int add(int a, int b);

    /// <summary>
    /// Subtract two integers
    /// </summary>
    [DllImport(LIB_NAME)]
    public static extern int subtract(int a, int b);

    /// <summary>
    /// Multiply two integer
    /// </summary>
    [DllImport(LIB_NAME)]
    public static extern int multiply(int a, int b);

    /// <summary>
    /// Divide two integers
    /// return a // b
    /// </summary>
    [DllImport(LIB_NAME)]
    public static extern int divide(int a, int b);

}
