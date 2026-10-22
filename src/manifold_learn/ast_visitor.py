from manifold_learn.grammar.OpenSCADParser import OpenSCADParser
from manifold_learn.grammar.OpenSCADVisitor import OpenSCADVisitor
from manifold_learn.ast.tree_node import TreeNode
from manifold_learn.ast.expression import Expression
from manifold3d import Manifold as m3d

class AstOpenSCADVisitor(OpenSCADVisitor):

    # Visit a parse tree produced by OpenSCADParser#start.
    def visitStart(self, ctx:OpenSCADParser.StartContext):
        root = TreeNode("root", positional_args=[], named_args={})
        for statement in ctx.statement():
            child = self.visit(statement)
            if child is not None:
                root.add_child(child)
        return root


    # Visit a parse tree produced by OpenSCADParser#statement.
    # def visitStatement(self, ctx:OpenSCADParser.StatementContext):
        return self.visitChildren(ctx)
    # Это не нужно реализовывать - это просто OR для трех правил


    ## =========================================================================
    #  Группа методов для вызова модулей

    # Visit a parse tree produced by OpenSCADParser#ChainedModuleCall.
    def visitChainedModuleCall(self, ctx:OpenSCADParser.ChainedModuleCallContext):
        node = self.visit(ctx.moduleCall())
        child = self.visit(ctx.moduleCallSeq())
        node.add_child(child)
        return node


    # Visit a parse tree produced by OpenSCADParser#ChainedLetCall.
    def visitChainedLetCall(self, ctx:OpenSCADParser.ChainedLetCallContext):
        node = self.visit(ctx.letExpr())
        child = self.visit(ctx.moduleCallSeq())
        node.add_child(child)
        return node


    # Visit a parse tree produced by OpenSCADParser#TerminalModuleCall.
    def visitTerminalModuleCall(self, ctx:OpenSCADParser.TerminalModuleCallContext):
        return self.visit(ctx.moduleCall())


    # Visit a parse tree produced by OpenSCADParser#TerminalBlock.
    def visitTerminalBlock(self, ctx:OpenSCADParser.TerminalBlockContext):
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
            child = self.visit(statement)
            if child is not None:
                node.add_child(child)
        return node


    # Visit a parse tree produced by OpenSCADParser#letExpr.
    def visitLetExpr(self, ctx:OpenSCADParser.LetExprContext):
        node = TreeNode("let", positional_args=[], named_args={})
        for name, expr in self.visit(ctx.letBindingList()).items():
            node.assign_variable(name, expr)
        return node


    # Visit a parse tree produced by OpenSCADParser#letBindingList.
    def visitLetBindingList(self, ctx:OpenSCADParser.LetBindingListContext) -> dict[str, Expression]:
        bindings = {}
        current = ctx
        while current is not None:
            name, expr = self.visit(current.letBinding())
            bindings[name] = expr
            current = current.letBindingList()
        return bindings


    # Visit a parse tree produced by OpenSCADParser#letBinding.
    def visitLetBinding(self, ctx:OpenSCADParser.LetBindingContext) -> tuple[str, Expression]:
        return ctx.IDENT().getText(), self.visit(ctx.expr())


    # Visit a parse tree produced by OpenSCADParser#moduleDefinition.
    def visitModuleDefinition(self, ctx:OpenSCADParser.ModuleDefinitionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenSCADParser#assignment.
    def visitAssignment(self, ctx:OpenSCADParser.AssignmentContext):
        return self.visitChildren(ctx)


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
    def visitIdentExpr(self, ctx:OpenSCADParser.IdentExprContext):
        return self._expr_stub(ctx)


    # Visit a parse tree produced by OpenSCADParser#ArrayExpr.
    def visitArrayExpr(self, ctx:OpenSCADParser.ArrayExprContext):
        return self._expr_stub(ctx)


    # Visit a parse tree produced by OpenSCADParser#NumberExpr.
    def visitNumberExpr(self, ctx:OpenSCADParser.NumberExprContext):
        return self._expr_stub(ctx)


    # Visit a parse tree produced by OpenSCADParser#BinaryExpr.
    def visitBinaryExpr(self, ctx:OpenSCADParser.BinaryExprContext):
        return self._expr_stub(ctx)


    # Visit a parse tree produced by OpenSCADParser#ParenExpr.
    def visitParenExpr(self, ctx:OpenSCADParser.ParenExprContext):
        return self._expr_stub(ctx)


    # Visit a parse tree produced by OpenSCADParser#exprList.
    def visitExprList(self, ctx:OpenSCADParser.ExprListContext):
        return self._expr_stub(ctx)

    # Temporary stand-in for the not-yet-implemented expression evaluation.
    # Captures the raw source text so args/let-bindings are wired up correctly.
    def _expr_stub(self, ctx):
        return Expression(ctx.getText())
