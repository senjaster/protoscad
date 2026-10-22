from manifold_learn.grammar.OpenSCADParser import OpenSCADParser
from manifold_learn.grammar.OpenSCADVisitor import OpenSCADVisitor
from manifold_learn.ast.tree_node import TreeNode
from manifold_learn.ast.expression import (
    Assignment,
    BinaryOp,
    NumberLiteral,
    Paren,
    Raw,
    Variable,
)
from manifold3d import Manifold as m3d

class AstOpenSCADVisitor(OpenSCADVisitor):

    # Visit a parse tree produced by OpenSCADParser#start.
    def visitStart(self, ctx:OpenSCADParser.StartContext):
        root = TreeNode("root", positional_args=[], named_args={})
        for statement in ctx.statement():
            self._register_statement(root, self.visit(statement))
        return root

    def _register_statement(self, scope: TreeNode, result):
        """Add a visited statement to the scope node.

        An assignment defines a variable on the scope node; any other result
        is a module-call subtree added as a child.
        """
        if isinstance(result, Assignment):
            scope.assign_variable(result)
        elif result is not None:
            scope.add_child(result)


    # Visit a parse tree produced by OpenSCADParser#statement.
    # def visitStatement(self, ctx:OpenSCADParser.StatementContext):
    # Это не нужно реализовывать - это просто OR для трех правил


    ## =========================================================================
    #  Группа методов для вызова модулей

    # Visit a parse tree produced by OpenSCADParser#ChainedModuleCall.
    def visitChainedModuleCall(self, ctx:OpenSCADParser.ChainedModuleCallContext) -> TreeNode:
        node = self.visit(ctx.moduleCall())
        child = self.visit(ctx.moduleCallSeq())
        node.add_child(child)
        return node


    # Visit a parse tree produced by OpenSCADParser#ChainedLetCall.
    def visitChainedLetCall(self, ctx:OpenSCADParser.ChainedLetCallContext) -> TreeNode:
        node = self.visit(ctx.letExpr())
        child = self.visit(ctx.moduleCallSeq())
        node.add_child(child)
        return node


    # Visit a parse tree produced by OpenSCADParser#TerminalModuleCall.
    def visitTerminalModuleCall(self, ctx:OpenSCADParser.TerminalModuleCallContext) -> TreeNode:
        return self.visit(ctx.moduleCall())


    # Visit a parse tree produced by OpenSCADParser#TerminalBlock.
    def visitTerminalBlock(self, ctx:OpenSCADParser.TerminalBlockContext) -> TreeNode:
        return self.visit(ctx.block())


    # Visit a parse tree produced by OpenSCADParser#moduleCall.
    def visitModuleCall(self, ctx:OpenSCADParser.ModuleCallContext):
        node = TreeNode(ctx.IDENT().getText(), positional_args=[], named_args={})
        if ctx.argList() is not None:
            positional, named = self.visit(ctx.argList())
            node.positional_args = positional
            node.named_args = named
        return node


    # Visit a parse tree produced by OpenSCADParser#block.
    def visitBlock(self, ctx:OpenSCADParser.BlockContext):
        node = TreeNode("block", positional_args=[], named_args={})
        for statement in ctx.statement():
            self._register_statement(node, self.visit(statement))
        return node


    # Visit a parse tree produced by OpenSCADParser#letExpr.
    def visitLetExpr(self, ctx:OpenSCADParser.LetExprContext):
        node = TreeNode("let", positional_args=[], named_args={})
        for assignment in self.visit(ctx.letBindingList()):
            node.assign_variable(assignment)
        return node


    # Visit a parse tree produced by OpenSCADParser#letBindingList.
    def visitLetBindingList(self, ctx:OpenSCADParser.LetBindingListContext) -> list[Assignment]:
        bindings = []
        current = ctx
        while current is not None:
            bindings.append(self.visit(current.letBinding()))
            current = current.letBindingList()
        return bindings


    # Visit a parse tree produced by OpenSCADParser#letBinding.
    def visitLetBinding(self, ctx:OpenSCADParser.LetBindingContext) -> Assignment:
        return Assignment(name=ctx.IDENT().getText(), value=self.visit(ctx.expr()))


    # Visit a parse tree produced by OpenSCADParser#moduleDefinition.
    def visitModuleDefinition(self, ctx:OpenSCADParser.ModuleDefinitionContext) -> TreeNode:
        node = TreeNode(ctx.IDENT().getText(), positional_args=[], named_args={})
        body = self.visit(ctx.moduleCallSeq())
        node.add_child(body)
        return node


    # Visit a parse tree produced by OpenSCADParser#assignment.
    def visitAssignment(self, ctx:OpenSCADParser.AssignmentContext) -> Assignment:
        return Assignment(name=ctx.IDENT().getText(), value=self.visit(ctx.expr()))


    # Visit a parse tree produced by OpenSCADParser#argList.
    def visitArgList(self, ctx:OpenSCADParser.ArgListContext) -> tuple[list[Expression], dict[str, Expression]]:
        positional = self.visit(ctx.positionalArgs()) if ctx.positionalArgs() is not None else []
        named = self.visit(ctx.namedArgs()) if ctx.namedArgs() is not None else {}
        return positional, named


    # Visit a parse tree produced by OpenSCADParser#positionalArgs.
    def visitPositionalArgs(self, ctx:OpenSCADParser.PositionalArgsContext) -> list[Expression]:
        return [self.visit(expr) for expr in ctx.expr()]


    # Visit a parse tree produced by OpenSCADParser#namedArgs.
    def visitNamedArgs(self, ctx:OpenSCADParser.NamedArgsContext) -> dict[str, Expression]:
        named = {}
        for arg in ctx.namedArg():
            name, expr = self.visitNamedArg(arg)
            named[name] = expr
        return named


    # Visit a parse tree produced by OpenSCADParser#namedArg.
    def visitNamedArg(self, ctx:OpenSCADParser.NamedArgContext) -> tuple[str, Expression]:
        return ctx.IDENT().getText(), self.visit(ctx.expr())


    # Visit a parse tree produced by OpenSCADParser#StringExpr.
    def visitStringExpr(self, ctx:OpenSCADParser.StringExprContext):
        return self._expr_stub(ctx)


    # Visit a parse tree produced by OpenSCADParser#IdentExpr.
    def visitIdentExpr(self, ctx:OpenSCADParser.IdentExprContext) -> Variable:
        return Variable(ctx.IDENT().getText())


    # Visit a parse tree produced by OpenSCADParser#ArrayExpr.
    def visitArrayExpr(self, ctx:OpenSCADParser.ArrayExprContext):
        return self._expr_stub(ctx)


    # Visit a parse tree produced by OpenSCADParser#NumberExpr.
    def visitNumberExpr(self, ctx:OpenSCADParser.NumberExprContext) -> NumberLiteral:
        return NumberLiteral(float(ctx.NUMBER().getText()))


    # Visit a parse tree produced by OpenSCADParser#AdditiveExpr.
    def visitAdditiveExpr(self, ctx:OpenSCADParser.AdditiveExprContext) -> BinaryOp:
        left = self.visit(ctx.expr(0))
        right = self.visit(ctx.expr(1))
        return BinaryOp(op=ctx.getChild(1).getText(), left=left, right=right)


    # Visit a parse tree produced by OpenSCADParser#MultiplicativeExpr.
    def visitMultiplicativeExpr(self, ctx:OpenSCADParser.MultiplicativeExprContext) -> BinaryOp:
        left = self.visit(ctx.expr(0))
        right = self.visit(ctx.expr(1))
        return BinaryOp(op=ctx.getChild(1).getText(), left=left, right=right)


    # Visit a parse tree produced by OpenSCADParser#ParenExpr.
    def visitParenExpr(self, ctx:OpenSCADParser.ParenExprContext) -> Paren:
        return Paren(self.visit(ctx.expr()))


    # Visit a parse tree produced by OpenSCADParser#exprList.
    def visitExprList(self, ctx:OpenSCADParser.ExprListContext):
        return self._expr_stub(ctx)

    # Temporary stand-in for the not-yet-implemented expression forms
    # (string, array). Captures the raw source text so args/let-bindings
    # are wired up correctly.
    def _expr_stub(self, ctx):
        return Raw(ctx.getText())
