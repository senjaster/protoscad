# Generated from OpenSCAD.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .OpenSCADParser import OpenSCADParser
else:
    from OpenSCADParser import OpenSCADParser

# This class defines a complete listener for a parse tree produced by OpenSCADParser.
class OpenSCADListener(ParseTreeListener):

    # Enter a parse tree produced by OpenSCADParser#start.
    def enterStart(self, ctx:OpenSCADParser.StartContext):
        pass

    # Exit a parse tree produced by OpenSCADParser#start.
    def exitStart(self, ctx:OpenSCADParser.StartContext):
        pass


    # Enter a parse tree produced by OpenSCADParser#statement.
    def enterStatement(self, ctx:OpenSCADParser.StatementContext):
        pass

    # Exit a parse tree produced by OpenSCADParser#statement.
    def exitStatement(self, ctx:OpenSCADParser.StatementContext):
        pass


    # Enter a parse tree produced by OpenSCADParser#ChainedModuleCall.
    def enterChainedModuleCall(self, ctx:OpenSCADParser.ChainedModuleCallContext):
        pass

    # Exit a parse tree produced by OpenSCADParser#ChainedModuleCall.
    def exitChainedModuleCall(self, ctx:OpenSCADParser.ChainedModuleCallContext):
        pass


    # Enter a parse tree produced by OpenSCADParser#ChainedLetCall.
    def enterChainedLetCall(self, ctx:OpenSCADParser.ChainedLetCallContext):
        pass

    # Exit a parse tree produced by OpenSCADParser#ChainedLetCall.
    def exitChainedLetCall(self, ctx:OpenSCADParser.ChainedLetCallContext):
        pass


    # Enter a parse tree produced by OpenSCADParser#TerminalModuleCall.
    def enterTerminalModuleCall(self, ctx:OpenSCADParser.TerminalModuleCallContext):
        pass

    # Exit a parse tree produced by OpenSCADParser#TerminalModuleCall.
    def exitTerminalModuleCall(self, ctx:OpenSCADParser.TerminalModuleCallContext):
        pass


    # Enter a parse tree produced by OpenSCADParser#TerminalBlock.
    def enterTerminalBlock(self, ctx:OpenSCADParser.TerminalBlockContext):
        pass

    # Exit a parse tree produced by OpenSCADParser#TerminalBlock.
    def exitTerminalBlock(self, ctx:OpenSCADParser.TerminalBlockContext):
        pass


    # Enter a parse tree produced by OpenSCADParser#moduleCall.
    def enterModuleCall(self, ctx:OpenSCADParser.ModuleCallContext):
        pass

    # Exit a parse tree produced by OpenSCADParser#moduleCall.
    def exitModuleCall(self, ctx:OpenSCADParser.ModuleCallContext):
        pass


    # Enter a parse tree produced by OpenSCADParser#block.
    def enterBlock(self, ctx:OpenSCADParser.BlockContext):
        pass

    # Exit a parse tree produced by OpenSCADParser#block.
    def exitBlock(self, ctx:OpenSCADParser.BlockContext):
        pass


    # Enter a parse tree produced by OpenSCADParser#letExpr.
    def enterLetExpr(self, ctx:OpenSCADParser.LetExprContext):
        pass

    # Exit a parse tree produced by OpenSCADParser#letExpr.
    def exitLetExpr(self, ctx:OpenSCADParser.LetExprContext):
        pass


    # Enter a parse tree produced by OpenSCADParser#letBindingList.
    def enterLetBindingList(self, ctx:OpenSCADParser.LetBindingListContext):
        pass

    # Exit a parse tree produced by OpenSCADParser#letBindingList.
    def exitLetBindingList(self, ctx:OpenSCADParser.LetBindingListContext):
        pass


    # Enter a parse tree produced by OpenSCADParser#letBinding.
    def enterLetBinding(self, ctx:OpenSCADParser.LetBindingContext):
        pass

    # Exit a parse tree produced by OpenSCADParser#letBinding.
    def exitLetBinding(self, ctx:OpenSCADParser.LetBindingContext):
        pass


    # Enter a parse tree produced by OpenSCADParser#moduleDefinition.
    def enterModuleDefinition(self, ctx:OpenSCADParser.ModuleDefinitionContext):
        pass

    # Exit a parse tree produced by OpenSCADParser#moduleDefinition.
    def exitModuleDefinition(self, ctx:OpenSCADParser.ModuleDefinitionContext):
        pass


    # Enter a parse tree produced by OpenSCADParser#assignment.
    def enterAssignment(self, ctx:OpenSCADParser.AssignmentContext):
        pass

    # Exit a parse tree produced by OpenSCADParser#assignment.
    def exitAssignment(self, ctx:OpenSCADParser.AssignmentContext):
        pass


    # Enter a parse tree produced by OpenSCADParser#argList.
    def enterArgList(self, ctx:OpenSCADParser.ArgListContext):
        pass

    # Exit a parse tree produced by OpenSCADParser#argList.
    def exitArgList(self, ctx:OpenSCADParser.ArgListContext):
        pass


    # Enter a parse tree produced by OpenSCADParser#positionalArgs.
    def enterPositionalArgs(self, ctx:OpenSCADParser.PositionalArgsContext):
        pass

    # Exit a parse tree produced by OpenSCADParser#positionalArgs.
    def exitPositionalArgs(self, ctx:OpenSCADParser.PositionalArgsContext):
        pass


    # Enter a parse tree produced by OpenSCADParser#namedArgs.
    def enterNamedArgs(self, ctx:OpenSCADParser.NamedArgsContext):
        pass

    # Exit a parse tree produced by OpenSCADParser#namedArgs.
    def exitNamedArgs(self, ctx:OpenSCADParser.NamedArgsContext):
        pass


    # Enter a parse tree produced by OpenSCADParser#namedArg.
    def enterNamedArg(self, ctx:OpenSCADParser.NamedArgContext):
        pass

    # Exit a parse tree produced by OpenSCADParser#namedArg.
    def exitNamedArg(self, ctx:OpenSCADParser.NamedArgContext):
        pass


    # Enter a parse tree produced by OpenSCADParser#StringExpr.
    def enterStringExpr(self, ctx:OpenSCADParser.StringExprContext):
        pass

    # Exit a parse tree produced by OpenSCADParser#StringExpr.
    def exitStringExpr(self, ctx:OpenSCADParser.StringExprContext):
        pass


    # Enter a parse tree produced by OpenSCADParser#MultiplicativeExpr.
    def enterMultiplicativeExpr(self, ctx:OpenSCADParser.MultiplicativeExprContext):
        pass

    # Exit a parse tree produced by OpenSCADParser#MultiplicativeExpr.
    def exitMultiplicativeExpr(self, ctx:OpenSCADParser.MultiplicativeExprContext):
        pass


    # Enter a parse tree produced by OpenSCADParser#IdentExpr.
    def enterIdentExpr(self, ctx:OpenSCADParser.IdentExprContext):
        pass

    # Exit a parse tree produced by OpenSCADParser#IdentExpr.
    def exitIdentExpr(self, ctx:OpenSCADParser.IdentExprContext):
        pass


    # Enter a parse tree produced by OpenSCADParser#ArrayExpr.
    def enterArrayExpr(self, ctx:OpenSCADParser.ArrayExprContext):
        pass

    # Exit a parse tree produced by OpenSCADParser#ArrayExpr.
    def exitArrayExpr(self, ctx:OpenSCADParser.ArrayExprContext):
        pass


    # Enter a parse tree produced by OpenSCADParser#AdditiveExpr.
    def enterAdditiveExpr(self, ctx:OpenSCADParser.AdditiveExprContext):
        pass

    # Exit a parse tree produced by OpenSCADParser#AdditiveExpr.
    def exitAdditiveExpr(self, ctx:OpenSCADParser.AdditiveExprContext):
        pass


    # Enter a parse tree produced by OpenSCADParser#NumberExpr.
    def enterNumberExpr(self, ctx:OpenSCADParser.NumberExprContext):
        pass

    # Exit a parse tree produced by OpenSCADParser#NumberExpr.
    def exitNumberExpr(self, ctx:OpenSCADParser.NumberExprContext):
        pass


    # Enter a parse tree produced by OpenSCADParser#ParenExpr.
    def enterParenExpr(self, ctx:OpenSCADParser.ParenExprContext):
        pass

    # Exit a parse tree produced by OpenSCADParser#ParenExpr.
    def exitParenExpr(self, ctx:OpenSCADParser.ParenExprContext):
        pass


    # Enter a parse tree produced by OpenSCADParser#exprList.
    def enterExprList(self, ctx:OpenSCADParser.ExprListContext):
        pass

    # Exit a parse tree produced by OpenSCADParser#exprList.
    def exitExprList(self, ctx:OpenSCADParser.ExprListContext):
        pass



del OpenSCADParser