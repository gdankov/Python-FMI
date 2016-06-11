import ast
import re
from collections import defaultdict


class FunctionCrawler(ast.NodeVisitor):
    def __init__(self, tree):
        self.__tree = ast.parse(tree)
        self.__functions_arguments = {}
        self.__lines_in_functions = {}
        self.__method_count = {}
        self.__nestings = {}
        self.__indentations = {}

    @property
    def max_arity(self):
        return self.__functions_arguments

    @property
    def lines_per_function(self):
        return self.__lines_in_functions

    @property
    def nestings(self):
        return self.__nestings

    @property
    def indentations(self):
        return self.__indentations

    @property
    def method_count(self):
        return self.__method_count

    def visit_Lambda(self, node):
        self.__functions_arguments[node.lineno] = len(node.args.args)

    def visit_FunctionDef(self, node):
        self._find_nestings(node)
        self._find_indentations(node)
        self.__functions_arguments[node.lineno] = len(node.args.args)
        self.__lines_in_functions[node.lineno] = FunctionCrawler.lines_count(
            node)

        self.generic_visit(node)

    def visit_ClassDef(self, node):
        self.__method_count[node.lineno] = sum(
            1 for stmn in node.body
            if isinstance(stmn, ast.FunctionDef))

        self.generic_visit(node)

    def _find_indentations(self, finc):
        for node in finc.body:
            lineno = node.lineno
            col_offset = node.col_offset

            if(lineno not in self.__indentations or
                    col_offset < self.__indentations[lineno]):
                self.__indentations[lineno] = col_offset

            if hasattr(node, 'body'):
                self._find_indentations(node)

    def _find_nestings(self, node, current_depth=0):
        current_depth += 1
        for statement in node.body:
            self.__nestings[statement.lineno] = current_depth

            if(not isinstance(statement, ast.FunctionDef) and
                    not isinstance(statement, ast.ClassDef) and
                    hasattr(statement, 'body')):
                self._find_nestings(statement, current_depth)

    def get_nestings(self, max_nesting):
        issues = {}
        for linenum, depth in self.nestings.items():
            if depth > max_nesting:
                issues[linenum] = 'nesting too deep ({} > {})'.format(
                    depth, max_nesting)
        return issues

    def get_wrong_indentations(self, indentation_size):
        nestings = self._find_all_nestings(self.__tree)
        indentations = self._find_all_indentations(self.__tree)

        issues = {}
        for linenum, nesting in nestings.items():
            if not indentations[linenum] == nesting * indentation_size:
                issues[linenum] = 'indentation is {} instead of {}'.format(
                    indentations[linenum], nesting * indentation_size)
        return issues

    def _find_all_indentations(self, tree, result={}):
        for node in tree.body:
            lineno = node.lineno
            col_offset = node.col_offset

            if(lineno not in result or
                    col_offset < result[lineno]):
                result[lineno] = col_offset

            if hasattr(node, 'body'):
                self._find_all_indentations(node)
        return result

    def _find_all_nestings(self, tree, current_depth=0, result={}):
        for node in tree.body:
            result[node.lineno] = current_depth
            if hasattr(node, 'body'):
                self._find_all_nestings(node, current_depth + 1, result)
        return result

    @staticmethod
    def lines_count(node):
        count = 0
        for statement in node.body:
            count += 1
            if(hasattr(statement, 'body') and not
                    isinstance(statement, ast.FunctionDef)):
                count += FunctionCrawler.lines_count(statement)
        return count


def critic(code, **rules):
    if not isinstance(code, str):
        raise ValueError(
            "First argument must be a string! Yours was {}".format(type(code)))

    line_length = rules.get("line_length", 79)
    forbid_semicolons = rules.get("forbid_semicolons", True)
    forbid_trailing_whitespace = rules.get("forbid_trailing_whitespace", True)

    issues_log = defaultdict(set)
    for linenum, line in enumerate(code.splitlines()):
        if len(line) > line_length:
            issues_log[linenum + 1].add('line too long ({} > {})'.format(
                len(line), line_length))

        if forbid_semicolons and ';' in re.sub(r'([\'"]).*?\1', "''", line):
            issues_log[linenum + 1].add(
                'multiple expressions on the same line')

        if forbid_trailing_whitespace and re.search(r'\s+$', line):
            issues_log[linenum + 1].add('trailing whitespace')

    crawler = FunctionCrawler(code)
    crawler.visit(ast.parse(code))
    indentation_size = rules.get("indentation_size", 4)
    indentations = crawler.get_wrong_indentations(indentation_size)
    for linenum, message in indentations.items():
            issues_log[linenum].add(message)

    max_nesting = rules.get("max_nesting", None)
    if max_nesting is not None:
        nestings = crawler.get_nestings(max_nesting)
        for linenum, message in nestings.items():
            issues_log[linenum].add(message)

    methods_per_class = rules.get("methods_per_class", None)
    max_arity = rules.get("max_arity", None)
    max_lines_per_function = rules.get("max_lines_per_function", None)

    if methods_per_class is not None:
        for linenum, method_count in crawler.method_count.items():
            if method_count > methods_per_class:
                issues_log[linenum].add(
                    'too many methods in class({} > {})'.format(
                        method_count,
                        methods_per_class))

    if max_arity is not None:
        for linenum, arg_count in crawler.max_arity.items():
            if arg_count > max_arity:
                issues_log[linenum].add(
                    'too many arguments({} > {})'.format(arg_count,
                                                         max_arity))

    if max_lines_per_function is not None:
        for linenum, lines_count in crawler.lines_per_function.items():
            if lines_count > max_lines_per_function:
                issues_log[linenum].add(
                    'method with too many lines ({} > {})'.format(
                        lines_count,
                        max_lines_per_function))
    return issues_log
