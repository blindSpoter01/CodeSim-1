from tree_sitter import Language, Parser
import sys
import difflib
import os, sys

def resource_path(relative_path):
    if hasattr(sys, "_MEIPASS"):
        #sys._MEIPASS 是pyinstaller打包后生成的exe文件执行时，将所有的二进制动态链接文件存放的目录。
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

CPP_LANGUAGE = Language(resource_path('language.so'), 'cpp')
parser = Parser()
parser.set_language(CPP_LANGUAGE)

def tokenize(root, b_code, tokens, types):
    childrenList = root.children
    if len(childrenList) == 0:
        tokens.append(b_code[root.start_byte:root.end_byte].decode('utf-8'))
        types.append(root.type)
    else:
        for child in childrenList:
            tokenize(child, b_code, tokens, types)

def types_diff(types1, types2):
    all_types = list(set(types1).union(set(types2)))
    all_types.sort()
    vocab = dict(zip(all_types, range(len(all_types))))
    str1 = ' '.join([str(vocab[item]) for item in types1])
    str2 = ' '.join([str(vocab[item]) for item in types2])
    return difflib.SequenceMatcher(None, str1, str2).quick_ratio()

def tokens_diff(tokens1, tokens2):
    all_tokens = list(set(tokens1).union(set(tokens2)))
    all_tokens.sort()
    vocab = dict(zip(all_tokens, range(len(all_tokens))))
    str1 = ' '.join([str(vocab[token]) for token in tokens1])
    str2 = ' '.join([str(vocab[token]) for token in tokens2])
    return difflib.SequenceMatcher(None, str1, str2).quick_ratio()

def codesim(code1, code2):
    b_code1 = code1.encode('utf-8')
    b_code2 = code2.encode('utf-8')
    tree1 = parser.parse(b_code1)
    if tree1.root_node.has_error:
        print("The first Code has a Structural Error !", file=sys.stderr)
        sys.exit()
    tree2 = parser.parse(b_code2)
    if tree2.root_node.has_error:
        print("The Second Code has a Structural Error !", file=sys.stderr)
        sys.exit()
    tokens1, tokens2 = [], []
    types1, types2 = [], []
    tokenize(tree1.root_node, b_code1, tokens1, types1)
    tokenize(tree2.root_node, b_code2, tokens2, types2)
    return round((types_diff(types1, types2) + tokens_diff(tokens1, tokens2)), 3) * 50

def main(path1, path2):
    with open(path1, 'r', encoding='utf-8') as file1:
        code1 = ' '.join(file1.readlines())
    with open(path2, 'r', encoding='utf-8') as file2:
        code2 = ' '.join(file2.readlines())
    print(codesim(code1, code2))

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print('Requires Two Input Parameters !', file=sys.stderr)
        sys.exit()
    main(sys.argv[1], sys.argv[2])