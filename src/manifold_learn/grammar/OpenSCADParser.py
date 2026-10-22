# Generated from OpenSCAD.g4 by ANTLR 4.13.2
# encoding: utf-8
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
	from typing import TextIO
else:
	from typing.io import TextIO

def serializedATN():
    return [
        4,1,21,181,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,2,6,7,
        6,2,7,7,7,2,8,7,8,2,9,7,9,2,10,7,10,2,11,7,11,2,12,7,12,2,13,7,13,
        2,14,7,14,2,15,7,15,2,16,7,16,2,17,7,17,1,0,5,0,38,8,0,10,0,12,0,
        41,9,0,1,0,1,0,1,1,1,1,1,1,3,1,48,8,1,1,2,1,2,1,2,1,2,1,2,1,2,1,
        2,1,2,1,2,1,2,3,2,60,8,2,1,3,1,3,1,3,3,3,65,8,3,1,3,1,3,1,4,1,4,
        5,4,71,8,4,10,4,12,4,74,9,4,1,4,1,4,1,5,1,5,1,5,1,5,1,5,1,6,1,6,
        1,6,1,6,1,6,3,6,88,8,6,1,7,1,7,1,7,1,7,1,8,1,8,1,8,5,8,97,8,8,10,
        8,12,8,100,9,8,1,9,1,9,3,9,104,8,9,1,10,1,10,1,10,1,10,3,10,110,
        8,10,1,10,1,10,1,10,1,11,1,11,1,11,1,11,1,11,1,12,1,12,1,12,3,12,
        123,8,12,1,12,3,12,126,8,12,1,13,1,13,1,13,5,13,131,8,13,10,13,12,
        13,134,9,13,1,14,1,14,1,14,5,14,139,8,14,10,14,12,14,142,9,14,1,
        15,1,15,1,15,1,15,1,16,1,16,1,16,1,16,1,16,1,16,3,16,154,8,16,1,
        16,1,16,1,16,1,16,1,16,3,16,161,8,16,1,16,1,16,1,16,1,16,1,16,1,
        16,5,16,169,8,16,10,16,12,16,172,9,16,1,17,1,17,1,17,1,17,1,17,3,
        17,179,8,17,1,17,0,1,32,18,0,2,4,6,8,10,12,14,16,18,20,22,24,26,
        28,30,32,34,0,2,1,0,8,9,1,0,10,11,186,0,39,1,0,0,0,2,47,1,0,0,0,
        4,59,1,0,0,0,6,61,1,0,0,0,8,68,1,0,0,0,10,77,1,0,0,0,12,87,1,0,0,
        0,14,89,1,0,0,0,16,93,1,0,0,0,18,103,1,0,0,0,20,105,1,0,0,0,22,114,
        1,0,0,0,24,125,1,0,0,0,26,127,1,0,0,0,28,135,1,0,0,0,30,143,1,0,
        0,0,32,160,1,0,0,0,34,178,1,0,0,0,36,38,3,2,1,0,37,36,1,0,0,0,38,
        41,1,0,0,0,39,37,1,0,0,0,39,40,1,0,0,0,40,42,1,0,0,0,41,39,1,0,0,
        0,42,43,5,0,0,1,43,1,1,0,0,0,44,48,3,4,2,0,45,48,3,20,10,0,46,48,
        3,22,11,0,47,44,1,0,0,0,47,45,1,0,0,0,47,46,1,0,0,0,48,3,1,0,0,0,
        49,50,3,6,3,0,50,51,3,4,2,0,51,60,1,0,0,0,52,53,3,10,5,0,53,54,3,
        4,2,0,54,60,1,0,0,0,55,56,3,6,3,0,56,57,5,1,0,0,57,60,1,0,0,0,58,
        60,3,8,4,0,59,49,1,0,0,0,59,52,1,0,0,0,59,55,1,0,0,0,59,58,1,0,0,
        0,60,5,1,0,0,0,61,62,5,16,0,0,62,64,5,2,0,0,63,65,3,24,12,0,64,63,
        1,0,0,0,64,65,1,0,0,0,65,66,1,0,0,0,66,67,5,3,0,0,67,7,1,0,0,0,68,
        72,5,4,0,0,69,71,3,2,1,0,70,69,1,0,0,0,71,74,1,0,0,0,72,70,1,0,0,
        0,72,73,1,0,0,0,73,75,1,0,0,0,74,72,1,0,0,0,75,76,5,5,0,0,76,9,1,
        0,0,0,77,78,5,15,0,0,78,79,5,2,0,0,79,80,3,12,6,0,80,81,5,3,0,0,
        81,11,1,0,0,0,82,88,3,14,7,0,83,84,3,14,7,0,84,85,5,6,0,0,85,86,
        3,12,6,0,86,88,1,0,0,0,87,82,1,0,0,0,87,83,1,0,0,0,88,13,1,0,0,0,
        89,90,5,16,0,0,90,91,5,14,0,0,91,92,3,32,16,0,92,15,1,0,0,0,93,98,
        3,18,9,0,94,95,5,6,0,0,95,97,3,18,9,0,96,94,1,0,0,0,97,100,1,0,0,
        0,98,96,1,0,0,0,98,99,1,0,0,0,99,17,1,0,0,0,100,98,1,0,0,0,101,104,
        5,16,0,0,102,104,3,14,7,0,103,101,1,0,0,0,103,102,1,0,0,0,104,19,
        1,0,0,0,105,106,5,7,0,0,106,107,5,16,0,0,107,109,5,2,0,0,108,110,
        3,16,8,0,109,108,1,0,0,0,109,110,1,0,0,0,110,111,1,0,0,0,111,112,
        5,3,0,0,112,113,3,4,2,0,113,21,1,0,0,0,114,115,5,16,0,0,115,116,
        5,14,0,0,116,117,3,32,16,0,117,118,5,1,0,0,118,23,1,0,0,0,119,122,
        3,26,13,0,120,121,5,6,0,0,121,123,3,28,14,0,122,120,1,0,0,0,122,
        123,1,0,0,0,123,126,1,0,0,0,124,126,3,28,14,0,125,119,1,0,0,0,125,
        124,1,0,0,0,126,25,1,0,0,0,127,132,3,32,16,0,128,129,5,6,0,0,129,
        131,3,32,16,0,130,128,1,0,0,0,131,134,1,0,0,0,132,130,1,0,0,0,132,
        133,1,0,0,0,133,27,1,0,0,0,134,132,1,0,0,0,135,140,3,30,15,0,136,
        137,5,6,0,0,137,139,3,30,15,0,138,136,1,0,0,0,139,142,1,0,0,0,140,
        138,1,0,0,0,140,141,1,0,0,0,141,29,1,0,0,0,142,140,1,0,0,0,143,144,
        5,16,0,0,144,145,5,14,0,0,145,146,3,32,16,0,146,31,1,0,0,0,147,148,
        6,16,-1,0,148,161,5,17,0,0,149,161,5,18,0,0,150,161,5,16,0,0,151,
        153,5,12,0,0,152,154,3,34,17,0,153,152,1,0,0,0,153,154,1,0,0,0,154,
        155,1,0,0,0,155,161,5,13,0,0,156,157,5,2,0,0,157,158,3,32,16,0,158,
        159,5,3,0,0,159,161,1,0,0,0,160,147,1,0,0,0,160,149,1,0,0,0,160,
        150,1,0,0,0,160,151,1,0,0,0,160,156,1,0,0,0,161,170,1,0,0,0,162,
        163,10,7,0,0,163,164,7,0,0,0,164,169,3,32,16,8,165,166,10,6,0,0,
        166,167,7,1,0,0,167,169,3,32,16,7,168,162,1,0,0,0,168,165,1,0,0,
        0,169,172,1,0,0,0,170,168,1,0,0,0,170,171,1,0,0,0,171,33,1,0,0,0,
        172,170,1,0,0,0,173,179,3,32,16,0,174,175,3,32,16,0,175,176,5,6,
        0,0,176,177,3,34,17,0,177,179,1,0,0,0,178,173,1,0,0,0,178,174,1,
        0,0,0,179,35,1,0,0,0,18,39,47,59,64,72,87,98,103,109,122,125,132,
        140,153,160,168,170,178
    ]

class OpenSCADParser ( Parser ):

    grammarFileName = "OpenSCAD.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "';'", "'('", "')'", "'{'", "'}'", "','", 
                     "'module'", "'*'", "'/'", "'+'", "'-'", "'['", "']'", 
                     "'='", "'let'" ]

    symbolicNames = [ "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "EQ", "LET", "IDENT", "NUMBER", 
                      "STRING", "COMMENT", "BLOCK_CMT", "WS" ]

    RULE_start = 0
    RULE_statement = 1
    RULE_moduleCallSeq = 2
    RULE_moduleCall = 3
    RULE_block = 4
    RULE_letExpr = 5
    RULE_letBindingList = 6
    RULE_letBinding = 7
    RULE_paramList = 8
    RULE_param = 9
    RULE_moduleDefinition = 10
    RULE_assignment = 11
    RULE_argList = 12
    RULE_positionalArgs = 13
    RULE_namedArgs = 14
    RULE_namedArg = 15
    RULE_expr = 16
    RULE_exprList = 17

    ruleNames =  [ "start", "statement", "moduleCallSeq", "moduleCall", 
                   "block", "letExpr", "letBindingList", "letBinding", "paramList", 
                   "param", "moduleDefinition", "assignment", "argList", 
                   "positionalArgs", "namedArgs", "namedArg", "expr", "exprList" ]

    EOF = Token.EOF
    T__0=1
    T__1=2
    T__2=3
    T__3=4
    T__4=5
    T__5=6
    T__6=7
    T__7=8
    T__8=9
    T__9=10
    T__10=11
    T__11=12
    T__12=13
    EQ=14
    LET=15
    IDENT=16
    NUMBER=17
    STRING=18
    COMMENT=19
    BLOCK_CMT=20
    WS=21

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.13.2")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class StartContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def EOF(self):
            return self.getToken(OpenSCADParser.EOF, 0)

        def statement(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(OpenSCADParser.StatementContext)
            else:
                return self.getTypedRuleContext(OpenSCADParser.StatementContext,i)


        def getRuleIndex(self):
            return OpenSCADParser.RULE_start

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitStart" ):
                return visitor.visitStart(self)
            else:
                return visitor.visitChildren(self)




    def start(self):

        localctx = OpenSCADParser.StartContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_start)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 39
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 98448) != 0):
                self.state = 36
                self.statement()
                self.state = 41
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 42
            self.match(OpenSCADParser.EOF)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class StatementContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def moduleCallSeq(self):
            return self.getTypedRuleContext(OpenSCADParser.ModuleCallSeqContext,0)


        def moduleDefinition(self):
            return self.getTypedRuleContext(OpenSCADParser.ModuleDefinitionContext,0)


        def assignment(self):
            return self.getTypedRuleContext(OpenSCADParser.AssignmentContext,0)


        def getRuleIndex(self):
            return OpenSCADParser.RULE_statement

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitStatement" ):
                return visitor.visitStatement(self)
            else:
                return visitor.visitChildren(self)




    def statement(self):

        localctx = OpenSCADParser.StatementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_statement)
        try:
            self.state = 47
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,1,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 44
                self.moduleCallSeq()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 45
                self.moduleDefinition()
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 46
                self.assignment()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ModuleCallSeqContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return OpenSCADParser.RULE_moduleCallSeq

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)



    class TerminalBlockContext(ModuleCallSeqContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a OpenSCADParser.ModuleCallSeqContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def block(self):
            return self.getTypedRuleContext(OpenSCADParser.BlockContext,0)


        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitTerminalBlock" ):
                return visitor.visitTerminalBlock(self)
            else:
                return visitor.visitChildren(self)


    class ChainedLetCallContext(ModuleCallSeqContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a OpenSCADParser.ModuleCallSeqContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def letExpr(self):
            return self.getTypedRuleContext(OpenSCADParser.LetExprContext,0)

        def moduleCallSeq(self):
            return self.getTypedRuleContext(OpenSCADParser.ModuleCallSeqContext,0)


        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitChainedLetCall" ):
                return visitor.visitChainedLetCall(self)
            else:
                return visitor.visitChildren(self)


    class TerminalModuleCallContext(ModuleCallSeqContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a OpenSCADParser.ModuleCallSeqContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def moduleCall(self):
            return self.getTypedRuleContext(OpenSCADParser.ModuleCallContext,0)


        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitTerminalModuleCall" ):
                return visitor.visitTerminalModuleCall(self)
            else:
                return visitor.visitChildren(self)


    class ChainedModuleCallContext(ModuleCallSeqContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a OpenSCADParser.ModuleCallSeqContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def moduleCall(self):
            return self.getTypedRuleContext(OpenSCADParser.ModuleCallContext,0)

        def moduleCallSeq(self):
            return self.getTypedRuleContext(OpenSCADParser.ModuleCallSeqContext,0)


        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitChainedModuleCall" ):
                return visitor.visitChainedModuleCall(self)
            else:
                return visitor.visitChildren(self)



    def moduleCallSeq(self):

        localctx = OpenSCADParser.ModuleCallSeqContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_moduleCallSeq)
        try:
            self.state = 59
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,2,self._ctx)
            if la_ == 1:
                localctx = OpenSCADParser.ChainedModuleCallContext(self, localctx)
                self.enterOuterAlt(localctx, 1)
                self.state = 49
                self.moduleCall()
                self.state = 50
                self.moduleCallSeq()
                pass

            elif la_ == 2:
                localctx = OpenSCADParser.ChainedLetCallContext(self, localctx)
                self.enterOuterAlt(localctx, 2)
                self.state = 52
                self.letExpr()
                self.state = 53
                self.moduleCallSeq()
                pass

            elif la_ == 3:
                localctx = OpenSCADParser.TerminalModuleCallContext(self, localctx)
                self.enterOuterAlt(localctx, 3)
                self.state = 55
                self.moduleCall()
                self.state = 56
                self.match(OpenSCADParser.T__0)
                pass

            elif la_ == 4:
                localctx = OpenSCADParser.TerminalBlockContext(self, localctx)
                self.enterOuterAlt(localctx, 4)
                self.state = 58
                self.block()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ModuleCallContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def IDENT(self):
            return self.getToken(OpenSCADParser.IDENT, 0)

        def argList(self):
            return self.getTypedRuleContext(OpenSCADParser.ArgListContext,0)


        def getRuleIndex(self):
            return OpenSCADParser.RULE_moduleCall

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitModuleCall" ):
                return visitor.visitModuleCall(self)
            else:
                return visitor.visitChildren(self)




    def moduleCall(self):

        localctx = OpenSCADParser.ModuleCallContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_moduleCall)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 61
            self.match(OpenSCADParser.IDENT)
            self.state = 62
            self.match(OpenSCADParser.T__1)
            self.state = 64
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if (((_la) & ~0x3f) == 0 and ((1 << _la) & 462852) != 0):
                self.state = 63
                self.argList()


            self.state = 66
            self.match(OpenSCADParser.T__2)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class BlockContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def statement(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(OpenSCADParser.StatementContext)
            else:
                return self.getTypedRuleContext(OpenSCADParser.StatementContext,i)


        def getRuleIndex(self):
            return OpenSCADParser.RULE_block

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitBlock" ):
                return visitor.visitBlock(self)
            else:
                return visitor.visitChildren(self)




    def block(self):

        localctx = OpenSCADParser.BlockContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_block)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 68
            self.match(OpenSCADParser.T__3)
            self.state = 72
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 98448) != 0):
                self.state = 69
                self.statement()
                self.state = 74
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 75
            self.match(OpenSCADParser.T__4)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class LetExprContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def LET(self):
            return self.getToken(OpenSCADParser.LET, 0)

        def letBindingList(self):
            return self.getTypedRuleContext(OpenSCADParser.LetBindingListContext,0)


        def getRuleIndex(self):
            return OpenSCADParser.RULE_letExpr

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitLetExpr" ):
                return visitor.visitLetExpr(self)
            else:
                return visitor.visitChildren(self)




    def letExpr(self):

        localctx = OpenSCADParser.LetExprContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_letExpr)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 77
            self.match(OpenSCADParser.LET)
            self.state = 78
            self.match(OpenSCADParser.T__1)
            self.state = 79
            self.letBindingList()
            self.state = 80
            self.match(OpenSCADParser.T__2)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class LetBindingListContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def letBinding(self):
            return self.getTypedRuleContext(OpenSCADParser.LetBindingContext,0)


        def letBindingList(self):
            return self.getTypedRuleContext(OpenSCADParser.LetBindingListContext,0)


        def getRuleIndex(self):
            return OpenSCADParser.RULE_letBindingList

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitLetBindingList" ):
                return visitor.visitLetBindingList(self)
            else:
                return visitor.visitChildren(self)




    def letBindingList(self):

        localctx = OpenSCADParser.LetBindingListContext(self, self._ctx, self.state)
        self.enterRule(localctx, 12, self.RULE_letBindingList)
        try:
            self.state = 87
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,5,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 82
                self.letBinding()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 83
                self.letBinding()
                self.state = 84
                self.match(OpenSCADParser.T__5)
                self.state = 85
                self.letBindingList()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class LetBindingContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def IDENT(self):
            return self.getToken(OpenSCADParser.IDENT, 0)

        def EQ(self):
            return self.getToken(OpenSCADParser.EQ, 0)

        def expr(self):
            return self.getTypedRuleContext(OpenSCADParser.ExprContext,0)


        def getRuleIndex(self):
            return OpenSCADParser.RULE_letBinding

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitLetBinding" ):
                return visitor.visitLetBinding(self)
            else:
                return visitor.visitChildren(self)




    def letBinding(self):

        localctx = OpenSCADParser.LetBindingContext(self, self._ctx, self.state)
        self.enterRule(localctx, 14, self.RULE_letBinding)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 89
            self.match(OpenSCADParser.IDENT)
            self.state = 90
            self.match(OpenSCADParser.EQ)
            self.state = 91
            self.expr(0)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ParamListContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def param(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(OpenSCADParser.ParamContext)
            else:
                return self.getTypedRuleContext(OpenSCADParser.ParamContext,i)


        def getRuleIndex(self):
            return OpenSCADParser.RULE_paramList

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitParamList" ):
                return visitor.visitParamList(self)
            else:
                return visitor.visitChildren(self)




    def paramList(self):

        localctx = OpenSCADParser.ParamListContext(self, self._ctx, self.state)
        self.enterRule(localctx, 16, self.RULE_paramList)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 93
            self.param()
            self.state = 98
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==6:
                self.state = 94
                self.match(OpenSCADParser.T__5)
                self.state = 95
                self.param()
                self.state = 100
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ParamContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return OpenSCADParser.RULE_param

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)



    class ParamNoDefaultContext(ParamContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a OpenSCADParser.ParamContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def IDENT(self):
            return self.getToken(OpenSCADParser.IDENT, 0)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitParamNoDefault" ):
                return visitor.visitParamNoDefault(self)
            else:
                return visitor.visitChildren(self)


    class ParamWithDefaultContext(ParamContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a OpenSCADParser.ParamContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def letBinding(self):
            return self.getTypedRuleContext(OpenSCADParser.LetBindingContext,0)


        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitParamWithDefault" ):
                return visitor.visitParamWithDefault(self)
            else:
                return visitor.visitChildren(self)



    def param(self):

        localctx = OpenSCADParser.ParamContext(self, self._ctx, self.state)
        self.enterRule(localctx, 18, self.RULE_param)
        try:
            self.state = 103
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,7,self._ctx)
            if la_ == 1:
                localctx = OpenSCADParser.ParamNoDefaultContext(self, localctx)
                self.enterOuterAlt(localctx, 1)
                self.state = 101
                self.match(OpenSCADParser.IDENT)
                pass

            elif la_ == 2:
                localctx = OpenSCADParser.ParamWithDefaultContext(self, localctx)
                self.enterOuterAlt(localctx, 2)
                self.state = 102
                self.letBinding()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ModuleDefinitionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def IDENT(self):
            return self.getToken(OpenSCADParser.IDENT, 0)

        def moduleCallSeq(self):
            return self.getTypedRuleContext(OpenSCADParser.ModuleCallSeqContext,0)


        def paramList(self):
            return self.getTypedRuleContext(OpenSCADParser.ParamListContext,0)


        def getRuleIndex(self):
            return OpenSCADParser.RULE_moduleDefinition

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitModuleDefinition" ):
                return visitor.visitModuleDefinition(self)
            else:
                return visitor.visitChildren(self)




    def moduleDefinition(self):

        localctx = OpenSCADParser.ModuleDefinitionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 20, self.RULE_moduleDefinition)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 105
            self.match(OpenSCADParser.T__6)
            self.state = 106
            self.match(OpenSCADParser.IDENT)
            self.state = 107
            self.match(OpenSCADParser.T__1)
            self.state = 109
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==16:
                self.state = 108
                self.paramList()


            self.state = 111
            self.match(OpenSCADParser.T__2)
            self.state = 112
            self.moduleCallSeq()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class AssignmentContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def IDENT(self):
            return self.getToken(OpenSCADParser.IDENT, 0)

        def EQ(self):
            return self.getToken(OpenSCADParser.EQ, 0)

        def expr(self):
            return self.getTypedRuleContext(OpenSCADParser.ExprContext,0)


        def getRuleIndex(self):
            return OpenSCADParser.RULE_assignment

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAssignment" ):
                return visitor.visitAssignment(self)
            else:
                return visitor.visitChildren(self)




    def assignment(self):

        localctx = OpenSCADParser.AssignmentContext(self, self._ctx, self.state)
        self.enterRule(localctx, 22, self.RULE_assignment)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 114
            self.match(OpenSCADParser.IDENT)
            self.state = 115
            self.match(OpenSCADParser.EQ)
            self.state = 116
            self.expr(0)
            self.state = 117
            self.match(OpenSCADParser.T__0)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ArgListContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def positionalArgs(self):
            return self.getTypedRuleContext(OpenSCADParser.PositionalArgsContext,0)


        def namedArgs(self):
            return self.getTypedRuleContext(OpenSCADParser.NamedArgsContext,0)


        def getRuleIndex(self):
            return OpenSCADParser.RULE_argList

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitArgList" ):
                return visitor.visitArgList(self)
            else:
                return visitor.visitChildren(self)




    def argList(self):

        localctx = OpenSCADParser.ArgListContext(self, self._ctx, self.state)
        self.enterRule(localctx, 24, self.RULE_argList)
        self._la = 0 # Token type
        try:
            self.state = 125
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,10,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 119
                self.positionalArgs()
                self.state = 122
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==6:
                    self.state = 120
                    self.match(OpenSCADParser.T__5)
                    self.state = 121
                    self.namedArgs()


                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 124
                self.namedArgs()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class PositionalArgsContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(OpenSCADParser.ExprContext)
            else:
                return self.getTypedRuleContext(OpenSCADParser.ExprContext,i)


        def getRuleIndex(self):
            return OpenSCADParser.RULE_positionalArgs

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitPositionalArgs" ):
                return visitor.visitPositionalArgs(self)
            else:
                return visitor.visitChildren(self)




    def positionalArgs(self):

        localctx = OpenSCADParser.PositionalArgsContext(self, self._ctx, self.state)
        self.enterRule(localctx, 26, self.RULE_positionalArgs)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 127
            self.expr(0)
            self.state = 132
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,11,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 128
                    self.match(OpenSCADParser.T__5)
                    self.state = 129
                    self.expr(0) 
                self.state = 134
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,11,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class NamedArgsContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def namedArg(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(OpenSCADParser.NamedArgContext)
            else:
                return self.getTypedRuleContext(OpenSCADParser.NamedArgContext,i)


        def getRuleIndex(self):
            return OpenSCADParser.RULE_namedArgs

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitNamedArgs" ):
                return visitor.visitNamedArgs(self)
            else:
                return visitor.visitChildren(self)




    def namedArgs(self):

        localctx = OpenSCADParser.NamedArgsContext(self, self._ctx, self.state)
        self.enterRule(localctx, 28, self.RULE_namedArgs)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 135
            self.namedArg()
            self.state = 140
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==6:
                self.state = 136
                self.match(OpenSCADParser.T__5)
                self.state = 137
                self.namedArg()
                self.state = 142
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class NamedArgContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def IDENT(self):
            return self.getToken(OpenSCADParser.IDENT, 0)

        def EQ(self):
            return self.getToken(OpenSCADParser.EQ, 0)

        def expr(self):
            return self.getTypedRuleContext(OpenSCADParser.ExprContext,0)


        def getRuleIndex(self):
            return OpenSCADParser.RULE_namedArg

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitNamedArg" ):
                return visitor.visitNamedArg(self)
            else:
                return visitor.visitChildren(self)




    def namedArg(self):

        localctx = OpenSCADParser.NamedArgContext(self, self._ctx, self.state)
        self.enterRule(localctx, 30, self.RULE_namedArg)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 143
            self.match(OpenSCADParser.IDENT)
            self.state = 144
            self.match(OpenSCADParser.EQ)
            self.state = 145
            self.expr(0)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ExprContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return OpenSCADParser.RULE_expr

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)


    class StringExprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a OpenSCADParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def STRING(self):
            return self.getToken(OpenSCADParser.STRING, 0)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitStringExpr" ):
                return visitor.visitStringExpr(self)
            else:
                return visitor.visitChildren(self)


    class MultiplicativeExprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a OpenSCADParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(OpenSCADParser.ExprContext)
            else:
                return self.getTypedRuleContext(OpenSCADParser.ExprContext,i)


        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitMultiplicativeExpr" ):
                return visitor.visitMultiplicativeExpr(self)
            else:
                return visitor.visitChildren(self)


    class IdentExprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a OpenSCADParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def IDENT(self):
            return self.getToken(OpenSCADParser.IDENT, 0)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitIdentExpr" ):
                return visitor.visitIdentExpr(self)
            else:
                return visitor.visitChildren(self)


    class ArrayExprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a OpenSCADParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def exprList(self):
            return self.getTypedRuleContext(OpenSCADParser.ExprListContext,0)


        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitArrayExpr" ):
                return visitor.visitArrayExpr(self)
            else:
                return visitor.visitChildren(self)


    class AdditiveExprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a OpenSCADParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(OpenSCADParser.ExprContext)
            else:
                return self.getTypedRuleContext(OpenSCADParser.ExprContext,i)


        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAdditiveExpr" ):
                return visitor.visitAdditiveExpr(self)
            else:
                return visitor.visitChildren(self)


    class NumberExprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a OpenSCADParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def NUMBER(self):
            return self.getToken(OpenSCADParser.NUMBER, 0)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitNumberExpr" ):
                return visitor.visitNumberExpr(self)
            else:
                return visitor.visitChildren(self)


    class ParenExprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a OpenSCADParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def expr(self):
            return self.getTypedRuleContext(OpenSCADParser.ExprContext,0)


        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitParenExpr" ):
                return visitor.visitParenExpr(self)
            else:
                return visitor.visitChildren(self)



    def expr(self, _p:int=0):
        _parentctx = self._ctx
        _parentState = self.state
        localctx = OpenSCADParser.ExprContext(self, self._ctx, _parentState)
        _prevctx = localctx
        _startState = 32
        self.enterRecursionRule(localctx, 32, self.RULE_expr, _p)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 160
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [17]:
                localctx = OpenSCADParser.NumberExprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx

                self.state = 148
                self.match(OpenSCADParser.NUMBER)
                pass
            elif token in [18]:
                localctx = OpenSCADParser.StringExprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 149
                self.match(OpenSCADParser.STRING)
                pass
            elif token in [16]:
                localctx = OpenSCADParser.IdentExprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 150
                self.match(OpenSCADParser.IDENT)
                pass
            elif token in [12]:
                localctx = OpenSCADParser.ArrayExprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 151
                self.match(OpenSCADParser.T__11)
                self.state = 153
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if (((_la) & ~0x3f) == 0 and ((1 << _la) & 462852) != 0):
                    self.state = 152
                    self.exprList()


                self.state = 155
                self.match(OpenSCADParser.T__12)
                pass
            elif token in [2]:
                localctx = OpenSCADParser.ParenExprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 156
                self.match(OpenSCADParser.T__1)
                self.state = 157
                self.expr(0)
                self.state = 158
                self.match(OpenSCADParser.T__2)
                pass
            else:
                raise NoViableAltException(self)

            self._ctx.stop = self._input.LT(-1)
            self.state = 170
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,16,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    self.state = 168
                    self._errHandler.sync(self)
                    la_ = self._interp.adaptivePredict(self._input,15,self._ctx)
                    if la_ == 1:
                        localctx = OpenSCADParser.MultiplicativeExprContext(self, OpenSCADParser.ExprContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 162
                        if not self.precpred(self._ctx, 7):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 7)")
                        self.state = 163
                        _la = self._input.LA(1)
                        if not(_la==8 or _la==9):
                            self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 164
                        self.expr(8)
                        pass

                    elif la_ == 2:
                        localctx = OpenSCADParser.AdditiveExprContext(self, OpenSCADParser.ExprContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 165
                        if not self.precpred(self._ctx, 6):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 6)")
                        self.state = 166
                        _la = self._input.LA(1)
                        if not(_la==10 or _la==11):
                            self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 167
                        self.expr(7)
                        pass

             
                self.state = 172
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,16,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.unrollRecursionContexts(_parentctx)
        return localctx


    class ExprListContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def expr(self):
            return self.getTypedRuleContext(OpenSCADParser.ExprContext,0)


        def exprList(self):
            return self.getTypedRuleContext(OpenSCADParser.ExprListContext,0)


        def getRuleIndex(self):
            return OpenSCADParser.RULE_exprList

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitExprList" ):
                return visitor.visitExprList(self)
            else:
                return visitor.visitChildren(self)




    def exprList(self):

        localctx = OpenSCADParser.ExprListContext(self, self._ctx, self.state)
        self.enterRule(localctx, 34, self.RULE_exprList)
        try:
            self.state = 178
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,17,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 173
                self.expr(0)
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 174
                self.expr(0)
                self.state = 175
                self.match(OpenSCADParser.T__5)
                self.state = 176
                self.exprList()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx



    def sempred(self, localctx:RuleContext, ruleIndex:int, predIndex:int):
        if self._predicates == None:
            self._predicates = dict()
        self._predicates[16] = self.expr_sempred
        pred = self._predicates.get(ruleIndex, None)
        if pred is None:
            raise Exception("No predicate with index:" + str(ruleIndex))
        else:
            return pred(localctx, predIndex)

    def expr_sempred(self, localctx:ExprContext, predIndex:int):
            if predIndex == 0:
                return self.precpred(self._ctx, 7)
         

            if predIndex == 1:
                return self.precpred(self._ctx, 6)
         




