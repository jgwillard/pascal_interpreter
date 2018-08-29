from keywords import PLUS, MINUS, MUL, FLOAT_DIV, INTEGER_DIV

class Visitor(object):
    '''
    base class for Visitors - Visitors must define their own calculate
    method which is used to perform binary ops, or they may pass
    '''
    GLOBAL_SCOPE = {}

    def visit_program(self, node):
        self.GLOBAL_SCOPE['PROGRAM'] = node.name
        return node.block.accept(self)

    def visit_block(self, node):
        for declaration in node.declarations:
            declaration.accept(self)
        return node.compound_statement.accept(self)

    def visit_var_decl(self, node):
        pass

    def visit_type(self, node):
        pass

    def visit_compound(self, node):
        for child in node.children:
            child.accept(self)

    def visit_assignment(self, node):
        var_name = node.left.value
        self.GLOBAL_SCOPE[var_name] = node.right.accept(self)
        return self.GLOBAL_SCOPE[var_name]

    def visit_var(self, node):
        var_name = node.value
        val = self.GLOBAL_SCOPE.get(var_name)
        if val is None:
            raise NameError(repr(var_name))
        return val

    def visit_no_op(self, node):
        pass

    def visit_bin_op(self, node):
        left = node.left.accept(self)
        right = node.right.accept(self)
        return self.calculate(node, left, right)

    def visit_unary_op(self, node):
        op = node.op.type
        if op == PLUS:
            return +node.expr.accept(self)
        elif op == MINUS:
            return -node.expr.accept(self)
        else:
            raise Exception('Invalid op type')

    def visit_num(self, node):
        return node.value

class CalculatorVisitor(Visitor):
    def calculate(self, node, left, right):
        if node.op.type == PLUS:
            return left + right
        elif node.op.type == MINUS:
            return left - right
        elif node.op.type == MUL:
            return left * right
        elif node.op.type == FLOAT_DIV:
            return left / right
        elif node.op.type == INTEGER_DIV:
            return left // right
        else:
            raise Exception('Invalid op type')

class PostfixNotationVisitor(Visitor):
    def calculate(self, node, left, right):
        return '{left} {right} {op}'.format(
            left=str(left),
            right=str(right),
            op=node.op.value
        )

class LispStyleNotationVisitor(Visitor):
    def calculate(self, node, left, right):
        return '({op} {left} {right})'.format(
            left=str(left),
            right=str(right),
            op=node.op.value
        )

class Interpreter(object):
    '''
    Interpreter is configured with one parse tree (output of parser)
    `interpret` method may be called several times with different
    visitors in order to allow multiple passes through the parse tree
    '''
    def __init__(self, tree):
        self.tree = tree

    def interpret(self, visitor):
        print(self.tree)
        return self.tree.accept(visitor)
