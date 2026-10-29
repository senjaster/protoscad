from protoscad.diagnostics import ErrorCode, ProtoSCADError
from protoscad.grammar.OpenSCADParser import OpenSCADParser
from protoscad.grammar.OpenSCADVisitor import OpenSCADVisitor
from protoscad.tree.expression import (
    Assignment,
    BinaryOp,
    BooleanLiteral,
    Call,
    Expression,
    Index,
    LetExpr,
    NumberLiteral,
    Paren,
    RangeLiteral,
    StringLiteral,
    TernaryOp,
    UnaryOp,
    Undefined,
    UndefLiteral,
    Variable,
    VectorLiteral,
    fold,
)
from protoscad.tree.statement import (
    ModuleCallStatement,
    ModuleDefinitionStatement,
    SourceSpan,
    Statement,
    VariableBindingStatement,
)
from protoscad.tree.values import unescape_string


class AstOpenSCADVisitor(OpenSCADVisitor):
    """Build a uniform Statement tree from the OpenSCAD parse tree.

    A scope is a ``ModuleCallStatement`` whose ``children`` hold the
    statements: the root scope is an artificial ``union`` call, a module body
    is a ``union`` call, and ``let`` is a ``let`` call. Bare ``{}`` blocks are
    transparent: ``visitBlock`` returns the statements inside as a list, which
    the caller splices into its own scope. No ``block`` node exists.
    """

    @staticmethod
    def _span(ctx) -> SourceSpan | None:
        """The source region a rule context covers, or ``None`` if unknown."""
        if ctx.start is None or ctx.stop is None:
            return None
        return SourceSpan(
            start_line=ctx.start.line,
            start_column=ctx.start.column,
            end_line=ctx.stop.line,
            end_column=ctx.stop.column + len(ctx.stop.text or ""),
        )

    @staticmethod
    def _span_of(statements: list[Statement]) -> SourceSpan | None:
        """The region from the first to the last statement's span, or ``None``."""
        spans = [s.span for s in statements if s is not None and s.span is not None]
        if not spans:
            return None
        return SourceSpan(
            start_line=spans[0].start_line,
            start_column=spans[0].start_column,
            end_line=spans[-1].end_line,
            end_column=spans[-1].end_column,
        )

    # Visit a parse tree produced by OpenSCADParser#start.
    def visitStart(self, ctx: OpenSCADParser.StartContext) -> ModuleCallStatement:
        scope: list[Statement] = []
        for statement in ctx.statement():
            scope.extend(self.visit(statement))
        # The root scope is synthesized, so its span is derived from its
        # children rather than the EOF token the start rule ends on.
        return ModuleCallStatement("union", span=self._span_of(scope), children=scope)

    # Visit a parse tree produced by OpenSCADParser#statement.
    def visitStatement(self, ctx: OpenSCADParser.StatementContext) -> list[Statement]:
        if ctx.moduleCallSeq() is not None:
            return [self.visit(ctx.moduleCallSeq())]
        if ctx.moduleDefinition() is not None:
            return [self.visit(ctx.moduleDefinition())]
        if ctx.assignment() is not None:
            return [self.visit(ctx.assignment())]
        # A bare block is transparent: splice its statements into the scope.
        if ctx.block() is not None:
            return self.visit(ctx.block())
        return []

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

    # Visit a parse tree produced by OpenSCADParser#ChainedIfCall.
    def visitChainedIfCall(self, ctx: OpenSCADParser.ChainedIfCallContext) -> ModuleCallStatement:
        # `if` is a module call like any other; in a chain it is a child of
        # the call to its left and terminates the chain.
        return self.visit(ctx.ifStatement())

    # Visit a parse tree produced by OpenSCADParser#ifStatement.
    def visitIfStatement(self, ctx: OpenSCADParser.IfStatementContext) -> ModuleCallStatement:
        node = ModuleCallStatement(
            "if",
            positional_args=[self.visit(ctx.expr())],
            span=self._span(ctx),
        )
        node.children.append(self.visit(ctx.ifBody()))
        if ctx.elseBody() is not None:
            node.children.append(self.visit(ctx.elseBody()))
        return node

    # Visit a parse tree produced by OpenSCADParser#ifBody.
    def visitIfBody(self, ctx: OpenSCADParser.IfBodyContext) -> ModuleCallStatement:
        return self._branch_scope(ctx)

    # Visit a parse tree produced by OpenSCADParser#elseBody.
    def visitElseBody(self, ctx: OpenSCADParser.ElseBodyContext) -> ModuleCallStatement:
        if ctx.ifStatement() is not None:
            # `else if` chains: the nested if is the else scope's single child.
            return ModuleCallStatement("union", span=self._span(ctx), children=[self.visit(ctx.ifStatement())])
        return self.visit(ctx.ifBody())

    def _branch_scope(self, ctx) -> ModuleCallStatement:
        """One `if` branch as an implicit-union scope — the same wrapping a
        module body gets — so each branch is a single child call no matter
        how many statements the source branch holds."""
        if ctx.block() is not None:
            children = self.visit(ctx.block())
        elif ctx.moduleCallSeq() is not None:
            children = [self.visit(ctx.moduleCallSeq())]
        else:
            children = []  # the `;` empty branch
        return ModuleCallStatement("union", span=self._span(ctx), children=children)

    # Visit a parse tree produced by OpenSCADParser#moduleCall.
    def visitModuleCall(self, ctx: OpenSCADParser.ModuleCallContext) -> ModuleCallStatement:
        node = ModuleCallStatement(ctx.IDENT().getText(), span=self._span(ctx))
        if ctx.argList() is not None:
            positional, named = self.visit(ctx.argList())
            node.positional_args = positional
            node.named_args = named
        return node

    # Visit a parse tree produced by OpenSCADParser#body.
    def visitBody(self, ctx: OpenSCADParser.BodyContext) -> ModuleCallStatement:

        children = self.visit(ctx.block()) if ctx.block() is not None else [self.visit(ctx.moduleCallSeq())]
        return ModuleCallStatement("union", span=self._span(ctx), children=children)

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
            VariableBindingStatement(name=assignment.name, value=assignment.value, span=span)
            for assignment, span in bindings
        ]
        return ModuleCallStatement("let", span=self._span(ctx), children=children)

    # Visit a parse tree produced by OpenSCADParser#letBindingList.
    def visitLetBindingList(
        self, ctx: OpenSCADParser.LetBindingListContext
    ) -> list[tuple[Assignment, SourceSpan | None]]:
        bindings = []
        current = ctx
        while current is not None:
            assignment = self.visit(current.letBinding())
            bindings.append((assignment, self._span(current.letBinding())))
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
        return ModuleDefinitionStatement(name=name, parameters=parameters, body=body, span=self._span(ctx))

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
            span=self._span(ctx),
        )

    # Visit a parse tree produced by OpenSCADParser#argList.
    def visitArgList(self, ctx: OpenSCADParser.ArgListContext) -> tuple[list, dict]:
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
        expr = self.visit(ctx.expr())
        # Widen the value's span to the whole `name = expr` argument so
        # argument errors point at the argument, not just its value.
        expr.span = self._span(ctx)
        return ctx.IDENT().getText(), expr

    ## =========================================================================
    #  Expressions

    # Shared shape of every binary alternative: `left op right` with the
    # operator as the middle child.
    def _binary_expr(self, ctx, left, right) -> Expression:
        op = ctx.getChild(1).getText()
        return fold(BinaryOp(op=op, left=left, right=right, span=self._span(ctx)))

    # Visit a parse tree produced by OpenSCADParser#NumberExpr.
    def visitNumberExpr(self, ctx: OpenSCADParser.NumberExprContext) -> NumberLiteral:
        return NumberLiteral(float(ctx.NUMBER().getText()), span=self._span(ctx))

    # Visit a parse tree produced by OpenSCADParser#StringExpr.
    def visitStringExpr(self, ctx: OpenSCADParser.StringExprContext) -> StringLiteral:
        raw = ctx.STRING().getText()
        return StringLiteral(unescape_string(raw[1:-1]), span=self._span(ctx))

    # Visit a parse tree produced by OpenSCADParser#TrueExpr.
    def visitTrueExpr(self, ctx: OpenSCADParser.TrueExprContext) -> BooleanLiteral:
        return BooleanLiteral(True, span=self._span(ctx))

    # Visit a parse tree produced by OpenSCADParser#FalseExpr.
    def visitFalseExpr(self, ctx: OpenSCADParser.FalseExprContext) -> BooleanLiteral:
        return BooleanLiteral(False, span=self._span(ctx))

    # Visit a parse tree produced by OpenSCADParser#UndefExpr.
    def visitUndefExpr(self, ctx: OpenSCADParser.UndefExprContext) -> UndefLiteral:
        return UndefLiteral(span=self._span(ctx))

    # Visit a parse tree produced by OpenSCADParser#IdentExpr.
    def visitIdentExpr(self, ctx: OpenSCADParser.IdentExprContext) -> Variable:
        return Variable(ctx.IDENT().getText(), span=self._span(ctx))

    # Visit a parse tree produced by OpenSCADParser#FunctionCallExpr.
    def visitFunctionCallExpr(self, ctx: OpenSCADParser.FunctionCallExprContext) -> Call:
        positional: list[Expression] = []
        named: dict[str, Expression] = {}
        if ctx.argList() is not None:
            positional, named = self.visit(ctx.argList())
        if named:
            # User-defined functions (the callers that accept named
            # arguments) do not exist yet; builtins are positional.
            arg = next(iter(named.values()))
            raise ProtoSCADError(
                "Named arguments are not supported in function calls",
                code=ErrorCode.INVALID_ARGUMENT,
                span=arg.span,
            )
        return Call(ctx.IDENT().getText(), positional, span=self._span(ctx))

    # Visit a parse tree produced by OpenSCADParser#VectorExpr.
    def visitVectorExpr(self, ctx: OpenSCADParser.VectorExprContext) -> Expression:
        elements = self.visit(ctx.exprList())
        return fold(VectorLiteral(elements, span=self._span(ctx)))

    # Visit a parse tree produced by OpenSCADParser#EmptyVectorExpr.
    def visitEmptyVectorExpr(self, ctx: OpenSCADParser.EmptyVectorExprContext) -> Expression:
        return fold(VectorLiteral([], span=self._span(ctx)))

    # Visit a parse tree produced by OpenSCADParser#RangeExpr.
    def visitRangeExpr(self, ctx: OpenSCADParser.RangeExprContext) -> Expression:
        # The `range` rule accessor is `range_` in the generated code
        # (ANTLR avoids shadowing the Python builtin).
        parts = ctx.range_().expr()
        step = self.visit(parts[1]) if len(parts) == 3 else None
        end = parts[2] if len(parts) == 3 else parts[1]
        return fold(
            RangeLiteral(
                start=self.visit(parts[0]),
                step=step,
                end=self.visit(end),
                span=self._span(ctx),
            )
        )

    # Visit a parse tree produced by OpenSCADParser#IndexExpr.
    def visitIndexExpr(self, ctx: OpenSCADParser.IndexExprContext) -> Expression:
        collection = self.visit(ctx.expr(0))
        index = self.visit(ctx.expr(1))
        return fold(Index(collection=collection, index=index, span=self._span(ctx)))

    # Visit a parse tree produced by OpenSCADParser#MemberExpr.
    def visitMemberExpr(self, ctx: OpenSCADParser.MemberExprContext) -> Expression:
        # `.x/.y/.z` are sugar for [0]/[1]/[2]; OpenSCAD defines no other
        # members (object fields are a dev-snapshot feature).
        axis = {"x": 0.0, "y": 1.0, "z": 2.0}.get(ctx.IDENT().getText())
        if axis is None:
            raise ProtoSCADError(
                f"Unknown member .{ctx.IDENT().getText()}: only .x, .y, .z are defined",
                code=ErrorCode.SYNTAX,
                span=self._span(ctx),
            )
        collection = self.visit(ctx.expr())
        return fold(Index(collection=collection, index=NumberLiteral(axis), span=self._span(ctx)))

    # Visit a parse tree produced by OpenSCADParser#ExponentExpr.
    def visitExponentExpr(self, ctx: OpenSCADParser.ExponentExprContext) -> Expression:
        return self._binary_expr(ctx, self.visit(ctx.expr(0)), self.visit(ctx.expr(1)))

    # Visit a parse tree produced by OpenSCADParser#UnaryExpr.
    def visitUnaryExpr(self, ctx: OpenSCADParser.UnaryExprContext) -> Expression:
        op = ctx.getChild(0).getText()
        return fold(UnaryOp(op=op, operand=self.visit(ctx.expr()), span=self._span(ctx)))

    # Visit a parse tree produced by OpenSCADParser#MultiplicativeExpr.
    def visitMultiplicativeExpr(self, ctx: OpenSCADParser.MultiplicativeExprContext) -> Expression:
        return self._binary_expr(ctx, self.visit(ctx.expr(0)), self.visit(ctx.expr(1)))

    # Visit a parse tree produced by OpenSCADParser#AdditiveExpr.
    def visitAdditiveExpr(self, ctx: OpenSCADParser.AdditiveExprContext) -> Expression:
        return self._binary_expr(ctx, self.visit(ctx.expr(0)), self.visit(ctx.expr(1)))

    # Visit a parse tree produced by OpenSCADParser#RelationalExpr.
    def visitRelationalExpr(self, ctx: OpenSCADParser.RelationalExprContext) -> Expression:
        return self._binary_expr(ctx, self.visit(ctx.expr(0)), self.visit(ctx.expr(1)))

    # Visit a parse tree produced by OpenSCADParser#EqualityExpr.
    def visitEqualityExpr(self, ctx: OpenSCADParser.EqualityExprContext) -> Expression:
        return self._binary_expr(ctx, self.visit(ctx.expr(0)), self.visit(ctx.expr(1)))

    # Visit a parse tree produced by OpenSCADParser#LogicalAndExpr.
    def visitLogicalAndExpr(self, ctx: OpenSCADParser.LogicalAndExprContext) -> Expression:
        return self._binary_expr(ctx, self.visit(ctx.expr(0)), self.visit(ctx.expr(1)))

    # Visit a parse tree produced by OpenSCADParser#LogicalOrExpr.
    def visitLogicalOrExpr(self, ctx: OpenSCADParser.LogicalOrExprContext) -> Expression:
        return self._binary_expr(ctx, self.visit(ctx.expr(0)), self.visit(ctx.expr(1)))

    # Visit a parse tree produced by OpenSCADParser#TernaryExpr.
    def visitTernaryExpr(self, ctx: OpenSCADParser.TernaryExprContext) -> Expression:
        return fold(
            TernaryOp(
                condition=self.visit(ctx.expr(0)),
                then_expr=self.visit(ctx.expr(1)),
                else_expr=self.visit(ctx.expr(2)),
                span=self._span(ctx),
            )
        )

    # Visit a parse tree produced by OpenSCADParser#LetExpression.
    def visitLetExpression(self, ctx: OpenSCADParser.LetExpressionContext) -> Expression:
        bindings = [assignment for assignment, _ in self.visit(ctx.letBindingList())]
        return fold(LetExpr(bindings=bindings, body=self.visit(ctx.expr()), span=self._span(ctx)))

    # Visit a parse tree produced by OpenSCADParser#ParenExpr.
    def visitParenExpr(self, ctx: OpenSCADParser.ParenExprContext) -> Expression:
        return fold(Paren(self.visit(ctx.expr()), span=self._span(ctx)))

    # Visit a parse tree produced by OpenSCADParser#exprList.
    def visitExprList(self, ctx: OpenSCADParser.ExprListContext) -> list:
        elements = [self.visit(ctx.expr())]
        if ctx.exprList() is not None:
            elements.extend(self.visit(ctx.exprList()))
        return elements
