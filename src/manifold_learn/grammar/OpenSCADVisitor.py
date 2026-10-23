# Generated from src/manifold_learn/grammar/OpenSCAD.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .OpenSCADParser import OpenSCADParser
else:
    from OpenSCADParser import OpenSCADParser

# This class defines a complete generic visitor for a parse tree produced by OpenSCADParser.

class OpenSCADVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by OpenSCADParser#start.
    def visitStart(self, ctx:OpenSCADParser.StartContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenSCADParser#statement.
    def visitStatement(self, ctx:OpenSCADParser.StatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenSCADParser#ChainedModuleCall.
    def visitChainedModuleCall(self, ctx:OpenSCADParser.ChainedModuleCallContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenSCADParser#ChainedLetCall.
    def visitChainedLetCall(self, ctx:OpenSCADParser.ChainedLetCallContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenSCADParser#ModuleCallWithBlock.
    def visitModuleCallWithBlock(self, ctx:OpenSCADParser.ModuleCallWithBlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenSCADParser#LetWithBlock.
    def visitLetWithBlock(self, ctx:OpenSCADParser.LetWithBlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenSCADParser#TerminalModuleCall.
    def visitTerminalModuleCall(self, ctx:OpenSCADParser.TerminalModuleCallContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenSCADParser#TerminalLet.
    def visitTerminalLet(self, ctx:OpenSCADParser.TerminalLetContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenSCADParser#moduleCall.
    def visitModuleCall(self, ctx:OpenSCADParser.ModuleCallContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenSCADParser#body.
    def visitBody(self, ctx:OpenSCADParser.BodyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenSCADParser#block.
    def visitBlock(self, ctx:OpenSCADParser.BlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenSCADParser#letExpr.
    def visitLetExpr(self, ctx:OpenSCADParser.LetExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenSCADParser#letBindingList.
    def visitLetBindingList(self, ctx:OpenSCADParser.LetBindingListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenSCADParser#letBinding.
    def visitLetBinding(self, ctx:OpenSCADParser.LetBindingContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenSCADParser#paramList.
    def visitParamList(self, ctx:OpenSCADParser.ParamListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenSCADParser#ParamNoDefault.
    def visitParamNoDefault(self, ctx:OpenSCADParser.ParamNoDefaultContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenSCADParser#ParamWithDefault.
    def visitParamWithDefault(self, ctx:OpenSCADParser.ParamWithDefaultContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenSCADParser#moduleDefinition.
    def visitModuleDefinition(self, ctx:OpenSCADParser.ModuleDefinitionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenSCADParser#assignment.
    def visitAssignment(self, ctx:OpenSCADParser.AssignmentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenSCADParser#argList.
    def visitArgList(self, ctx:OpenSCADParser.ArgListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenSCADParser#positionalArgs.
    def visitPositionalArgs(self, ctx:OpenSCADParser.PositionalArgsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenSCADParser#namedArgs.
    def visitNamedArgs(self, ctx:OpenSCADParser.NamedArgsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenSCADParser#namedArg.
    def visitNamedArg(self, ctx:OpenSCADParser.NamedArgContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenSCADParser#StringExpr.
    def visitStringExpr(self, ctx:OpenSCADParser.StringExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenSCADParser#MultiplicativeExpr.
    def visitMultiplicativeExpr(self, ctx:OpenSCADParser.MultiplicativeExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenSCADParser#IdentExpr.
    def visitIdentExpr(self, ctx:OpenSCADParser.IdentExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenSCADParser#ArrayExpr.
    def visitArrayExpr(self, ctx:OpenSCADParser.ArrayExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenSCADParser#AdditiveExpr.
    def visitAdditiveExpr(self, ctx:OpenSCADParser.AdditiveExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenSCADParser#NumberExpr.
    def visitNumberExpr(self, ctx:OpenSCADParser.NumberExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenSCADParser#ParenExpr.
    def visitParenExpr(self, ctx:OpenSCADParser.ParenExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OpenSCADParser#exprList.
    def visitExprList(self, ctx:OpenSCADParser.ExprListContext):
        return self.visitChildren(ctx)



del OpenSCADParser