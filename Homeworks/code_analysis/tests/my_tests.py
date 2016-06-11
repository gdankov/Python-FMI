import unittest
import ast
import solution as s


#class TestNestingFinder(unittest.TestCase):
#     def setUp(self):
#         self.test_code = '''class A:
#     def foo(self, a):
#         with file('SDasd'):
#             print(a)
#             if a == 0:
#                 return 0
#         return a

#     def bar(self, b):
#         print(b)

#     def unpleasant_one():
#         for x in ["smiling", "girl"]:
#             for y in ["cool", "long beard", "boy"]:
#                 if x == 'girl' and y == 'long beard':
#                     print("А {} {}!".format(y, x))

# '''

#     def test_max_nesting(self):
#         code = '''class A:
#     def some_func(self):
#         a_variable = 'some text'; another_variable = 'some more text'; even_moar_variables = 'just for to pass the time'
#         for char in a_variable:
#             if char != 'a':
#                 for _ in range(10):
#                     print('SOOOO MUUUCH INDENTATION')

# def some_func2():
#     a_variable = 'some text'; another_variable = 'some more text'; even_moar_variables = 'just for to pass the time'
#     for char in a_variable:
#         if char != 'a':
#             for _ in range(10):
#                 print('SOOOO MUUUCH INDENTATION')
# '''
#         finder = s.NestingFinder(code)
#         nestings = finder.nestings
#         expected = {1: 0, 2: 1, 3: 2, 7: 5, 10: 1, 14: 4}
#         self.assertEqual(expected, nestings)

#     def test_max_nesting_2(self):
#         finder = s.NestingFinder(self.test_code)
#         nestings = finder.nestings
#         expected = {4: 3, 6: 4, 7: 2, 10: 2, 16: 5}
#         self.assertEqual(expected, nestings)

#     def test_max_nesting_3(self):
#         code = '''def f1():
#     def nested():
#         def nested2():
#             a = 2 + 1
#             if a == 3:
#                 print("AAAAAA")
#             return a
#         return nested2()
#     return "NESTED"

# class A:
#     class B:
#         def f():
#             a = 5

#         def f2(fml):
#             if fml:
#                 for _ in range(10):
#                     print("FML")

#     def ffs():
#         if True == True:
#             print(";/")
# '''
#         finder = s.NestingFinder(code)
#         nestings = finder.nestings
#         expected = {4: 3, 6: 4, 7: 3, 8: 2, 9: 1, 14: 3, 19: 5, 23: 3}
#         self.assertEqual(expected, nestings)



class TestFunctionCrawler(unittest.TestCase):
    def setUp(self):
        self.test_code = '''class A:
    def foo(self, a):
        with file('SDasd'):
            print(a)
            if a == 0:
                return 0
        return a

    def bar(self, b):
        print(b)

    def unpleasant_one():
        for x in ["smiling", "girl"]:
            for y in ["cool", "long beard", "boy"]:
                if x == 'girl' and y == 'long beard':
                    print("А {} {}!".format(y, x))

def ffs(a):
    print(a)
'''

    def test_max_arity(self):
        crawler = s.FunctionCrawler()
        crawler.visit(ast.parse(self.test_code))
        max_arity = crawler.max_arity
        expected = {2: 2, 9: 2, 12: 0, 18: 1}
        self.assertEqual(expected, max_arity)

    def test_function_count_per_class(self):
        crawler = s.FunctionCrawler()
        crawler.visit(ast.parse(self.test_code))
        method_count = crawler.method_count
        expected = {1: 3}
        self.assertEqual(expected, method_count)

    def test_function_cout_per_class_2(self):
        code = '''class A:
    def foo(self, a):
        with file('SDasd'):
            print(a)
            if a == 0:
                return 0
        return a

    def bar(self, b):
        print(b)

    def unpleasant_one():
        for x in ["smiling", "girl"]:
            for y in ["cool", "long beard", "boy"]:
                if x == 'girl' and y == 'long beard':
                    print("А {} {}!".format(y, x))

class B:
    class N:
        def __init__(self):
            print("INIT")

        def n(s):
            if(s):
                return s
            print("damn")

    def b():
        def nested():
            print("Nested")
            return 1
        for _ in range(10):
            print("SDADA")

def ffs(a):
    print(a)
'''
        crawler = s.FunctionCrawler()
        crawler.visit(ast.parse(code))
        method_count = crawler.method_count
        expected = {1: 3, 18: 1, 19: 2}
        self.assertEqual(expected, method_count)

    def test_line_count_in_functions(self):
        code = '''def func():
    example = [long_list,
           second_element_of_long_list]
    return example
'''
        crawler = s.FunctionCrawler()
        crawler.visit(ast.parse(code))
        result = crawler.lines_per_function
        expected = {1: 2}
        self.assertEqual(expected, result)

    def test_line_count_in_functions_2(self):
        code = '''def na_maika_mu(putkata):
    a  = 4
    def  gfgh (fd):
        return 42
    #nekuf komentar deba
    return 32
'''
        crawler = s.FunctionCrawler()
        crawler.visit(ast.parse(code))
        result = crawler.lines_per_function
        expected = {1: 4, 3: 1}
        self.assertEqual(expected, result)

    def test_line_count_in_functions_3(self):
        code = '''def a(a):
    ad = a; a =5
#   nqkuv komentar
    ad += a
    return ad
'''
        crawler = s.FunctionCrawler()
        crawler.visit(ast.parse(code))
        result = crawler.lines_per_function
        expected = {1: 4}
        self.assertEqual(expected, result)

    def test_line_count_in_functions_4(self):
        code = '''def a(a):
    class A:
        def fuck(off):
            print(f)
            a = 5; b = 4
            return s
    print(drizzy)
    return ad
'''
        crawler = s.FunctionCrawler()
        crawler.visit(ast.parse(code))
        result = crawler.lines_per_function
        expected = {1: 8, 3: 4}
        self.assertEqual(expected, result)

class TestCritic(unittest.TestCase):
    def setUp(self):
        self.test_code = '''def func1(a):
    a = a + 1 + 1 + 1 + 1 + 1 + 1 + 1 + 1 + 1 + 1 + 1 + 1 + 1 + 1 + 1 + 1 + 1 + 1 + 1 + 1
    print(a)


class A:
     def foo(self, a, pfff):
        with file('SDasd'):
            print(a)
            if a == 0:
                return 0
        return a

    def bar(self, b):
        print(b) 

    def unpleasant_one():
        for x in ["smiling", "girl"]:
            for y in ["cool", "long beard", "boy"]:
                if x == 'girl' and y == 'long beard':
                    a = 2 * 2 * 2 * 2 * 2 * 2 * 2 * 2 * 2 * 2 * 2 * 2 * 2 * 2 * 2
                    print("А {} {}!".format(y, x))

def neuf_tam(s, t, f, u):
   def nemanachin():
       a_ne = 2
   ugly_ident = 3
   return ugly_ident

class B:
    def foo_b(self, a):
         return a 

    def bar_b(self, b):
        b = 2 + 2 + 2 + 2 + 2 + 2 + 2 + 2 + 2 + 2 + 2 + 2 + 2 + 2 + 2 + 2 + 2 + 2 + 2 + 2 + 2 + 2 + 2 + 2 + 2 + 2 + 2 + 2
        print(b)

    def bla_b(self, c):
        pass


def basi():
    a = 1 + 2 + 3  
    a += 2

def pff(ne, be, se):
    a = 2 + 3 ; b = "of we"
     c = 2 ; dd = "ebigo" ; a = c + d
    e = "nema nachin ; tva da raboti"
    p1 = "arewe ; ';' ne ne"
    #nenenenenenenen
    p2 = 'ne ne ; " ; sads" dd'
'''

    def test_line_length(self):
        result = s.critic(self.test_code)
        self.assertIn('line too long (89 > 79)', result[2])
        self.assertIn('line too long (81 > 79)', result[21])
        self.assertIn('line too long (121 > 79)', result[30])

        result = s.critic(self.test_code, line_length=50)
        self.assertIn('line too long (89 > 50)', result[2])
        self.assertIn('line too long (81 > 50)', result[21])
        self.assertIn('line too long (121 > 50)', result[30])
        self.assertIn('line too long (51 > 50)', result[19])
        self.assertIn('line too long (53 > 50)', result[20])
        self.assertEqual(len(result[22]), 0)

        result = s.critic('''def some_func():
    a_variable = 'some text'; another_variable = 'some more text'; even_moar_variables = 'just for to pass the time'
''')
        self.assertIn('line too long (116 > 79)', result[2])

    def test_forbid_trailing_whitespaces(self):
        result = s.critic(self.test_code)
        self.assertIn('trailing whitespace', result[15])
        self.assertIn('trailing whitespace', result[27])
        self.assertIn('trailing whitespace', result[38])

    def test_forbid_semicolons(self):
        result = s.critic(self.test_code)
        self.assertIn('multiple expressions on the same line', result[42])
        self.assertIn('multiple expressions on the same line', result[43])
        self.assertNotIn('multiple expressions on the same line', result[44])
        self.assertNotIn('multiple expressions on the same line', result[45])
        self.assertNotIn('multiple expressions on the same line', result[46])

    def test_EVERYTHING(self):
        result = s.critic(self.test_code, forbid_semicolons=True,
                          max_nesting=3, methods_per_class=2, max_arity=2,
                          max_lines_per_function=4
                          )
        expected = {2: ['line too long (89 > 50)'],
                    6: ['too many methods in class(3 > 2)'],
                    7: ['indentation is 5 instead of 4', 'too many arguments(3 > 2)', 'method with too many lines (5 > 4)'],
                    15: ['trailing whitespace'],
                    11: ['nesting too deep (4 > 3)'],
                    17: ['method with too many lines (5 > 4)'],
                    20: ['nesting too deep (4 > 3)'],
                    21: ['line too long (81 > 79)', 'nesting too deep (5 > 3)'],
                    22: ['nesting too deep (5 > 3)'],
                    24: ['too many arguments(4 > 2)'],
                    25: ['indentation is 3 instead of 4'],
                    26: ['indentation is 7 instead of 8'],
                    27: ['indentation is 3 instead of 4'],
                    28: ['indentation is 3 instead of 4'],
                    30: ['too many methods in class(3 > 2)'],
                    32: ['indentation is 9 instead of 8', 'trailing whitespace'],
                    35: ['line too long (121 > 79)'],
                    43: ['trailing whitespace'],
                    46: ['too many arguments(3 > 2)', 'method with too many lines (8 > 4)'],
                    47: ['multiple expressions on the same line'],
                    48: ['multiple expressions on the same line', 'indentation is 5 instead of 4'],
                    }
        self.assertEqual(expected, result)

if __name__ == "__main__":
    unittest.main()
