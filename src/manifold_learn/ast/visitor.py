from manifold_learn.grammar.OpenSCADParser import OpenSCADParser
from manifold_learn.grammar.OpenSCADVisitor import OpenSCADVisitor
from manifold_learn.ast.statement import (
    ModuleCallStatement,
    ModuleDefinitionStatement,
    Statement,
    VariableBindingStatement,
)
from manifold_learn.ast.expression import (
    ArrayLiteral,
    Assignment,
    BinaryOp,
    NumberLiteral,
    Paren,
    Raw,
    Undefined,
    Variable,
)


class AstOpenSCADVisitor(OpenSCADVisitor):
    """Build a uniform Statement tree from the OpenSCAD parse tree.

    A scope is a plain ``list[Statement]``. Bare ``{}`` blocks are transparent:
    ``visitBlock`` returns the statements inside as a list, which the caller
    splices into its own scope. No ``block`` node exists.
    """

    # Visit a parse tree produced by OpenSCADParser#start.
    def visitStart(self, ctx: OpenSCADParser.StartContext) -> list[Statement]:
        scope: list[Statement] = []
        for statement in ctx.statement():
            scope.extend(self.visit(statement))
        return scope

    # Visit a parse tree produced by OpenSCADParser#statement.
    def visitStatement(self, ctx: OpenSCADParser.StatementContext) -> list[Statement]:
        if ctx.moduleCallSeq() is not None:
            return [self.visit(ctx.moduleCallSeq())]
        if ctx.moduleDefinition() is not None:
            return [self.visit(ctx.moduleDefinition())]
        if ctx.assignment() is not None:
            return [self.visit(ctx.assignment())]
        # A bare block is transparent: splice its statements into the scope.
        return self.visit(ctx.block())

    ## =========================================================================
    #  Module call sequences

    # Visit a parse tree produced by OpenSCADParser#ChainedModuleCall.
    def visitChainedModuleCall(self, ctx: OpenSCADParser.ChainedModuleCallContext) -> ModuleCallStatement:
        node = self.visit(ctx.moduleCall())
        child = self.visit(ctx.moduleCallSeq())
        node.children.append(child)
        return node

    # Visit a parse tree produced by OpenSCADParser#ChainedLetCall.
    def visitChainedLetCall(self, ctx: OpenSCADParser.ChainedLetCallContext) -> ModuleCallStatement:
        node = self.visit(ctx.letExpr())
        child = self.visit(ctx.moduleCallSeq())
        node.children.append(child)
        return node

    # Visit a parse tree produced by OpenSCADParser#ModuleCallWithBlock.
    def visitModuleCallWithBlock(self, ctx: OpenSCADParser.ModuleCallWithBlockContext) -> ModuleCallStatement:
        node = self.visit(ctx.moduleCall())
        node.children.extend(self.visit(ctx.block()))
        return node

    # Visit a parse tree produced by OpenSCADParser#LetWithBlock.
    def visitLetWithBlock(self, ctx: OpenSCADParser.LetWithBlockContext) -> ModuleCallStatement:
        node = self.visit(ctx.letExpr())
        node.children.extend(self.visit(ctx.block()))
        return node

    # Visit a parse tree produced by OpenSCADParser#TerminalModuleCall.
    def visitTerminalModuleCall(self, ctx: OpenSCADParser.TerminalModuleCallContext) -> ModuleCallStatement:
        return self.visit(ctx.moduleCall())

    # Visit a parse tree produced by OpenSCADParser#TerminalLet.
    def visitTerminalLet(self, ctx: OpenSCADParser.TerminalLetContext) -> ModuleCallStatement:
        return self.visit(ctx.letExpr())

    # Visit a parse tree produced by OpenSCADParser#moduleCall.
    def visitModuleCall(self, ctx: OpenSCADParser.ModuleCallContext) -> ModuleCallStatement:
        node = ModuleCallStatement(ctx.IDENT().getText())
        if ctx.argList() is not None:
            positional, named = self.visit(ctx.argList())
            node.positional_args = positional
            node.named_args = named
        return node

    # Visit a parse tree produced by OpenSCADParser#body.
    def visitBody(self, ctx: OpenSCADParser.BodyContext) -> list[Statement]:
        if ctx.block() is not None:
            return self.visit(ctx.block())
        return [self.visit(ctx.moduleCallSeq())]

    # Visit a parse tree produced by OpenSCADParser#block.
    def visitBlock(self, ctx: OpenSCADParser.BlockContext) -> list[Statement]:
        scope: list[Statement] = []
        for statement in ctx.statement():
            scope.extend(self.visit(statement))
        return scope

    # Visit a parse tree produced by OpenSCADParser#letExpr.
    def visitLetExpr(self, ctx: OpenSCADParser.LetExprContext) -> ModuleCallStatement:
        # `let` is a scope: its bindings become leading VariableBindingStatements
        # in the let node's body, followed by the visited continuation.
        bindings = self.visit(ctx.letBindingList())
        children: list[Statement] = [
            VariableBindingStatement(name=assignment.name, value=assignment.value)
            for assignment in bindings
        ]
        return ModuleCallStatement("let", children=children)

    # Visit a parse tree produced by OpenSCADParser#letBindingList.
    def visitLetBindingList(self, ctx: OpenSCADParser.LetBindingListContext) -> list[Assignment]:
        bindings = []
        current = ctx
        while current is not None:
            bindings.append(self.visit(current.letBinding()))
            current = current.letBindingList()
        return bindings

    # Visit a parse tree produced by OpenSCADParser#letBinding.
    def visitLetBinding(self, ctx: OpenSCADParser.LetBindingContext) -> Assignment:
        return Assignment(name=ctx.IDENT().getText(), value=self.visit(ctx.expr()))

    # Visit a parse tree produced by OpenSCADParser#moduleDefinition.
    def visitModuleDefinition(self, ctx: OpenSCADParser.ModuleDefinitionContext) -> ModuleDefinitionStatement:
        name = ctx.IDENT().getText()
        parameters: dict[str, Assignment] = {}
        if ctx.paramList() is not None:
            for param in self.visit(ctx.paramList()):
                parameters[param.name] = param
        body = self.visit(ctx.body())
        return ModuleDefinitionStatement(name=name, parameters=parameters, body=body)

    # Visit a parse tree produced by OpenSCADParser#paramList.
    def visitParamList(self, ctx: OpenSCADParser.ParamListContext) -> list[Assignment]:
        return [self.visit(param) for param in ctx.param()]

    # Visit a parse tree produced by OpenSCADParser#ParamNoDefault.
    def visitParamNoDefault(self, ctx: OpenSCADParser.ParamNoDefaultContext) -> Assignment:
        return Assignment(name=ctx.IDENT().getText(), value=Undefined())

    # Visit a parse tree produced by OpenSCADParser#ParamWithDefault.
    def visitParamWithDefault(self, ctx: OpenSCADParser.ParamWithDefaultContext) -> Assignment:
        return self.visit(ctx.letBinding())

    # Visit a parse tree produced by OpenSCADParser#assignment.
    def visitAssignment(self, ctx: OpenSCADParser.AssignmentContext) -> VariableBindingStatement:
        return VariableBindingStatement(
            name=ctx.IDENT().getText(),
            value=self.visit(ctx.expr()),
        )

    # Visit a parse tree produced by OpenSCADParser#argList.
    def visitArgList(
        self, ctx: OpenSCADParser.ArgListContext
    ) -> tuple[list, dict]:
        positional = self.visit(ctx.positionalArgs()) if ctx.positionalArgs() is not None else []
        named = self.visit(ctx.namedArgs()) if ctx.namedArgs() is not None else {}
        return positional, named

    # Visit a parse tree produced by OpenSCADParser#positionalArgs.
    def visitPositionalArgs(self, ctx: OpenSCADParser.PositionalArgsContext) -> list:
        return [self.visit(expr) for expr in ctx.expr()]

    # Visit a parse tree produced by OpenSCADParser#namedArgs.
    def visitNamedArgs(self, ctx: OpenSCADParser.NamedArgsContext) -> dict:
        named = {}
        for arg in ctx.namedArg():
            name, expr = self.visitNamedArg(arg)
            named[name] = expr
        return named

    # Visit a parse tree produced by OpenSCADParser#namedArg.
    def visitNamedArg(self, ctx: OpenSCADParser.NamedArgContext) -> tuple[str, object]:
        return ctx.IDENT().getText(), self.visit(ctx.expr())

    ## =========================================================================
    #  Expressions

    # Visit a parse tree produced by OpenSCADParser#StringExpr.
    def visitStringExpr(self, ctx: OpenSCADParser.StringExprContext):
        return self._expr_stub(ctx)

    # Visit a parse tree produced by OpenSCADParser#IdentExpr.
    def visitIdentExpr(self, ctx: OpenSCADParser.IdentExprContext) -> Variable:
        return Variable(ctx.IDENT().getText())

    # Visit a parse tree produced by OpenSCADParser#ArrayExpr.
    def visitArrayExpr(self, ctx: OpenSCADParser.ArrayExprContext) -> ArrayLiteral:
        elements = self.visit(ctx.exprList()) if ctx.exprList() is not None else []
        return ArrayLiteral(elements)

    # Visit a parse tree produced by OpenSCADParser#NumberExpr.
    def visitNumberExpr(self, ctx: OpenSCADParser.NumberExprContext) -> NumberLiteral:
        return NumberLiteral(float(ctx.NUMBER().getText()))

    # Visit a parse tree produced by OpenSCADParser#AdditiveExpr.
    def visitAdditiveExpr(self, ctx: OpenSCADParser.AdditiveExprContext) -> BinaryOp:
        left = self.visit(ctx.expr(0))
        right = self.visit(ctx.expr(1))
        return BinaryOp(op=ctx.getChild(1).getText(), left=left, right=right)

    # Visit a parse tree produced by OpenSCADParser#MultiplicativeExpr.
    def visitMultiplicativeExpr(self, ctx: OpenSCADParser.MultiplicativeExprContext) -> BinaryOp:
        left = self.visit(ctx.expr(0))
        right = self.visit(ctx.expr(1))
        return BinaryOp(op=ctx.getChild(1).getText(), left=left, right=right)

    # Visit a parse tree produced by OpenSCADParser#ParenExpr.
    def visitParenExpr(self, ctx: OpenSCADParser.ParenExprContext) -> Paren:
        return Paren(self.visit(ctx.expr()))

    # Visit a parse tree produced by OpenSCADParser#exprList.
    def visitExprList(self, ctx: OpenSCADParser.ExprListContext) -> list:
        elements = [self.visit(ctx.expr())]
        if ctx.exprList() is not None:
            elements.extend(self.visit(ctx.exprList()))
        return elements

    # Temporary stand-in for the not-yet-implemented string expression.
    # Captures the raw source text so args/let-bindings are wired up correctly.
    def _expr_stub(self, ctx):
        return Raw(ctx.getText())