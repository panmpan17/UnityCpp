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

    [DllImport(LIB_NAME)]
    public static extern int add(int a, int b);
}
