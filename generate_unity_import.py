import re

from dataclasses import dataclass
from enum import Enum
from typing import Dict, List
from argparse import ArgumentParser
from pprint import pprint


TEMPLATE = """using System.Runtime.InteropServices;

public static class {c_sharp_class_name}
{{
#if UNITY_STANDALONE_WIN || UNITY_EDITOR_WIN
    const string LIB_NAME = "{lib_name}"; // {lib_name}.dll
#elif UNITY_STANDALONE_LINUX || UNITY_EDITOR_LINUX
    const string LIB_NAME = "lib{lib_name}.so"; // Linux
#elif UNITY_STANDALONE_OSX || UNITY_EDITOR_OSX
    const string LIB_NAME = "lib{lib_name}.dylib"; // macOS
#else
    const string LIB_NAME = "__Internal"; // iOS uses static linking
#endif

{functions}
}}
"""


class CPPType(Enum):
    INT = "int"
    FLOAT = "float"
    DOUBLE = "double"
    VOID = "void"
    STRING = "string"
    CHAR = "char"
    CHAR_PTR = "char*"
    INT_PTR = "int*"
    FLOAT_PTR = "float*"
    DOUBLE_PTR = "double*"
    VOID_PTR = "void*"

    @staticmethod
    def to_csharp(type_value):
        if type_value == CPPType.INT:
            return "int"
        elif type_value == CPPType.FLOAT:
            return "float"
        elif type_value == CPPType.DOUBLE:
            return "double"
        elif type_value == CPPType.VOID:
            return "void"
        elif type_value == CPPType.STRING:
            return "string"
        elif type_value == CPPType.CHAR:
            return "char"
        elif type_value == CPPType.CHAR_PTR:
            return "string"
        elif type_value == CPPType.INT_PTR:
            return "IntPtr"
        elif type_value == CPPType.FLOAT_PTR:
            return "IntPtr"
        elif type_value == CPPType.DOUBLE_PTR:
            return "IntPtr"
        elif type_value == CPPType.VOID_PTR:
            return "IntPtr"
        else:
            raise NotImplementedError(f"Unknown type {type_value}")


@dataclass
class FunctionParam:
    type: CPPType
    name: str


@dataclass
class CommentBlock:
    summary: str
    params_desc: Dict[str, str]
    return_desc: str

    def to_csharp(self):
        string = f"    /// <summary>\n"

        lines = self.summary.split("\n")
        for line in lines:
            string += f"    /// {line}\n"

        string += f"    /// </summary>\n"

        for param_name, param_desc in self.params_desc.items():
            string += f"    /// <param name=\"{param_name}\">{param_desc}</param>\n"

        if self.return_desc != "":
            string += f"    /// <returns>{self.return_desc}</returns>\n"

        return string


@dataclass
class Function:
    name: str
    params: List[FunctionParam]
    return_type: CPPType
    comment: CommentBlock

    def to_csharp(self):
        string = "\n"
        if self.comment:
            string += self.comment.to_csharp()
        string += f"    [DllImport(LIB_NAME)]\n"
        string += f"    public static extern {CPPType.to_csharp(self.return_type)} {self.name}("
        for i, param in enumerate(self.params):
            string += f"{CPPType.to_csharp(param.type)} {param.name}"
            if i != len(self.params) - 1:
                string += ", "
        string += ");"
        return string


class GenerateUnityDLLImport:
    ENTIRE_FUNC_LINE_REGEX = r"EXTERN_C_API\s+[\w\*]+\s+\w+\s*\([^)]*\)"
    FUNC_LINE_SEPARATE_REGEX = r"EXTERN_C_API\s+([\w\*]+)\s+(\w+)\s*\(([^)]*)\)"
    PARAM_REGEX = r"\(([^)]*)\)"

    def __init__(self):
        self.functions: List[Function] = []
    
    def read_from_hfile(self, hfile_path: str):
        with open(hfile_path) as f:
            header = f.read()

        functions = re.findall(self.ENTIRE_FUNC_LINE_REGEX, header)

        for entire_line in functions:
            return_type_str, func_name, params = re.match(self.FUNC_LINE_SEPARATE_REGEX, entire_line).groups()
            return_type = CPPType[return_type_str.upper()]

            param_list: List[FunctionParam] = []
            for param in params.split(','):
                param = param.strip()
                if not param:
                    continue

                # TODO: param might have const or other things
                param_type_str, param_name = param.rsplit(' ', 1)
                param_type = CPPType[param_type_str.upper()]

                param_list.append(FunctionParam(param_type, param_name))
            
            comment_block = self.find_entire_comment_block(header, entire_line)

            function = Function(func_name, param_list, return_type, comment_block)
            self.functions.append(function)
    
    def find_entire_comment_block(self, header: str, entire_line: str) -> CommentBlock:
        index_in_header = header.index(entire_line)
        if index_in_header > 0:
            pass
    
        lines_before_func = header[:index_in_header].split("\n")
        lines_before_func.pop()

        entire_comments = []
        multiline_wrapped_comment = False
        for line in reversed(lines_before_func):
            if not multiline_wrapped_comment:
                if line.find("*/") != -1:
                    entire_comments.append(line)

                    if line.find("/*") != -1:
                        return self.parse_one_line_wrapped_comment(line)

                    multiline_wrapped_comment = True

                elif line.find("//") != -1:
                    entire_comments.append(line)
                else:
                    break

            else:
                if line.find("/*") != -1:
                    entire_comments.append(line)
                    break
                else:
                    entire_comments.append(line)

        entire_comments = reversed(entire_comments)
        comment_block = "\n".join(entire_comments)

        if multiline_wrapped_comment:
            return self.parse_multiline_wrapped_comment(comment_block)
        else:
            return self.parse_multiline_comment_block(comment_block)
    
    def parse_one_line_wrapped_comment(self, line: str) -> CommentBlock:
        start_mark = re.findall(r"/\*+", line)
        end_mark = re.findall(r"\*+/", line)
        line = line.replace(start_mark[0], "").replace(end_mark[0], "").strip()

        return CommentBlock(line, {}, "")

    def parse_multiline_wrapped_comment(self, comment_block: str) -> CommentBlock:
        start_mark = re.findall(r"/\*+", comment_block)
        end_mark = re.findall(r"\*+/", comment_block)
        comment_block = comment_block.replace(start_mark[0], "").replace(end_mark[0], "").strip()

        lines = comment_block.split("\n")
        summary = []
        params = {}
        return_desc = ""
        for line in lines:
            line = line.strip().strip("*").strip()

            if line.find("@param") != -1:
                param_line = line.replace("@param ", "").strip()
                param_name, param_desc = param_line.split(" ", 1)
                params[param_name] = param_desc
                
            elif line.find("@return") != -1:
                return_desc = line.replace("@return ", "").strip()
            else:
                summary.append(line)

        return CommentBlock("\n".join(summary), params, return_desc)

    def parse_multiline_comment_block(self, comment_block: str) -> CommentBlock:
        lines = comment_block.split("\n")

        for i, line in enumerate(lines):
            start_mark = re.findall(r"//+", line)
            lines[i] = line.replace(start_mark[0], "", 1).strip()

        return CommentBlock("\n".join(lines), {}, "")

    def generate_csharp(self, class_name: str, lib_name: str, output_folder: str=""):
        functions_str = ""

        for func in self.functions:
            functions_str += func.to_csharp() + "\n"

        content = TEMPLATE.format(
            c_sharp_class_name=class_name,
            lib_name=lib_name,
            functions=functions_str,
        )

        if output_folder == "":
            output_folder = "."

        output_path = f"{output_folder}/{class_name}.cs"

        with open(output_path, "w") as f:
            f.write(content)


if __name__ == "__main__":
    parser = ArgumentParser()

    parser.add_argument("lib_name", help="Name of the library")
    parser.add_argument("-f", "--hfile", action="append", help="Path to the header file")
    parser.add_argument("--cpp_class", help="Name of the C++ class", default="CppNative")
    parser.add_argument("--output_folder", help="Output folder", default="")

    args = parser.parse_args()

    generator = GenerateUnityDLLImport()

    for hfile in args.hfile:
        generator.read_from_hfile(hfile)

    generator.generate_csharp(args.cpp_class, args.lib_name, args.output_folder)
