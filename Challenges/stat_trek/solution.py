import ast
import os


class ClassFuncLister(ast.NodeVisitor):
    def __init__(self):
        self.func_count = 0
        self.class_count = 0
        self.unpleasant = []

    def visit_FunctionDef(self, node):
        self.func_count += 1
        if ClassFuncLister.is_unpleasant(node, node.col_offset):
            self.unpleasant.append(node.name)
        self.generic_visit(node)

    @staticmethod
    def is_unpleasant(node, def_col):
        if not hasattr(node, 'body'):
            return node.col_offset - def_col >= 13

        body = ast.parse(node).body
        for expr in body:
            if ClassFuncLister.is_unpleasant(expr, def_col):
                return True
        return False

    def visit_ClassDef(self, node):
        self.class_count += 1
        self.generic_visit(node)


def stats(path_to_directory):
    if not os.path.isdir(path_to_directory):
        raise NotADirectoryError(
            "Directory {} doesn't exist!".format(path_to_directory))

    class_count = 0
    func_count = 0
    unpleasant = []

    for root, dirs, files in os.walk(path_to_directory):
        for file in filter(lambda f: os.path.splitext(f)[1] == '.py', files):
                absolute_path = os.path.join(
                    os.sep, os.path.abspath(root), file)
                with open(absolute_path, 'r') as f:
                    parsed_module = ast.parse(f.read())

                cfl = ClassFuncLister()
                cfl.visit(parsed_module)

                class_count += cfl.class_count
                func_count += cfl.func_count

                relative_path = os.path.join(root, file)
                unpleasant.extend(["{}#{}". format(relative_path, unpl)
                                  for unpl in cfl.unpleasant])
    return {
        'classes': class_count,
        'functions': func_count,
        'unpleasant_functions': unpleasant
    }
