# Generated from src/protoscad/grammar/OpenSCAD.g4 by ANTLR 4.13.2
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
        4,1,21,196,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,2,6,7,
        6,2,7,7,7,2,8,7,8,2,9,7,9,2,10,7,10,2,11,7,11,2,12,7,12,2,13,7,13,
        2,14,7,14,2,15,7,15,2,16,7,16,2,17,7,17,2,18,7,18,1,0,5,0,40,8,0,
        10,0,12,0,43,9,0,1,0,1,0,1,1,1,1,1,1,1,1,3,1,51,8,1,1,2,1,2,1,2,
        1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,3,2,
        71,8,2,1,3,1,3,1,3,3,3,76,8,3,1,3,1,3,1,4,1,4,3,4,82,8,4,1,5,1,5,
        5,5,86,8,5,10,5,12,5,89,9,5,1,5,1,5,1,6,1,6,1,6,1,6,1,6,1,7,1,7,
        1,7,1,7,1,7,3,7,103,8,7,1,8,1,8,1,8,1,8,1,9,1,9,1,9,5,9,112,8,9,
        10,9,12,9,115,9,9,1,10,1,10,3,10,119,8,10,1,11,1,11,1,11,1,11,3,
        11,125,8,11,1,11,1,11,1,11,1,12,1,12,1,12,1,12,1,12,1,13,1,13,1,
        13,3,13,138,8,13,1,13,3,13,141,8,13,1,14,1,14,1,14,5,14,146,8,14,
        10,14,12,14,149,9,14,1,15,1,15,1,15,5,15,154,8,15,10,15,12,15,157,
        9,15,1,16,1,16,1,16,1,16,1,17,1,17,1,17,1,17,1,17,1,17,3,17,169,
        8,17,1,17,1,17,1,17,1,17,1,17,3,17,176,8,17,1,17,1,17,1,17,1,17,
        1,17,1,17,5,17,184,8,17,10,17,12,17,187,9,17,1,18,1,18,1,18,1,18,
        1,18,3,18,194,8,18,1,18,0,1,34,19,0,2,4,6,8,10,12,14,16,18,20,22,
        24,26,28,30,32,34,36,0,2,1,0,8,9,1,0,10,11,204,0,41,1,0,0,0,2,50,
        1,0,0,0,4,70,1,0,0,0,6,72,1,0,0,0,8,81,1,0,0,0,10,83,1,0,0,0,12,
        92,1,0,0,0,14,102,1,0,0,0,16,104,1,0,0,0,18,108,1,0,0,0,20,118,1,
        0,0,0,22,120,1,0,0,0,24,129,1,0,0,0,26,140,1,0,0,0,28,142,1,0,0,
        0,30,150,1,0,0,0,32,158,1,0,0,0,34,175,1,0,0,0,36,193,1,0,0,0,38,
        40,3,2,1,0,39,38,1,0,0,0,40,43,1,0,0,0,41,39,1,0,0,0,41,42,1,0,0,
        0,42,44,1,0,0,0,43,41,1,0,0,0,44,45,5,0,0,1,45,1,1,0,0,0,46,51,3,
        4,2,0,47,51,3,22,11,0,48,51,3,24,12,0,49,51,3,10,5,0,50,46,1,0,0,
        0,50,47,1,0,0,0,50,48,1,0,0,0,50,49,1,0,0,0,51,3,1,0,0,0,52,53,3,
        6,3,0,53,54,3,4,2,0,54,71,1,0,0,0,55,56,3,12,6,0,56,57,3,4,2,0,57,
        71,1,0,0,0,58,59,3,6,3,0,59,60,3,10,5,0,60,71,1,0,0,0,61,62,3,12,
        6,0,62,63,3,10,5,0,63,71,1,0,0,0,64,65,3,6,3,0,65,66,5,1,0,0,66,
        71,1,0,0,0,67,68,3,12,6,0,68,69,5,1,0,0,69,71,1,0,0,0,70,52,1,0,
        0,0,70,55,1,0,0,0,70,58,1,0,0,0,70,61,1,0,0,0,70,64,1,0,0,0,70,67,
        1,0,0,0,71,5,1,0,0,0,72,73,5,16,0,0,73,75,5,2,0,0,74,76,3,26,13,
        0,75,74,1,0,0,0,75,76,1,0,0,0,76,77,1,0,0,0,77,78,5,3,0,0,78,7,1,
        0,0,0,79,82,3,10,5,0,80,82,3,4,2,0,81,79,1,0,0,0,81,80,1,0,0,0,82,
        9,1,0,0,0,83,87,5,4,0,0,84,86,3,2,1,0,85,84,1,0,0,0,86,89,1,0,0,
        0,87,85,1,0,0,0,87,88,1,0,0,0,88,90,1,0,0,0,89,87,1,0,0,0,90,91,
        5,5,0,0,91,11,1,0,0,0,92,93,5,15,0,0,93,94,5,2,0,0,94,95,3,14,7,
        0,95,96,5,3,0,0,96,13,1,0,0,0,97,103,3,16,8,0,98,99,3,16,8,0,99,
        100,5,6,0,0,100,101,3,14,7,0,101,103,1,0,0,0,102,97,1,0,0,0,102,
        98,1,0,0,0,103,15,1,0,0,0,104,105,5,16,0,0,105,106,5,14,0,0,106,
        107,3,34,17,0,107,17,1,0,0,0,108,113,3,20,10,0,109,110,5,6,0,0,110,
        112,3,20,10,0,111,109,1,0,0,0,112,115,1,0,0,0,113,111,1,0,0,0,113,
        114,1,0,0,0,114,19,1,0,0,0,115,113,1,0,0,0,116,119,5,16,0,0,117,
        119,3,16,8,0,118,116,1,0,0,0,118,117,1,0,0,0,119,21,1,0,0,0,120,
        121,5,7,0,0,121,122,5,16,0,0,122,124,5,2,0,0,123,125,3,18,9,0,124,
        123,1,0,0,0,124,125,1,0,0,0,125,126,1,0,0,0,126,127,5,3,0,0,127,
        128,3,8,4,0,128,23,1,0,0,0,129,130,5,16,0,0,130,131,5,14,0,0,131,
        132,3,34,17,0,132,133,5,1,0,0,133,25,1,0,0,0,134,137,3,28,14,0,135,
        136,5,6,0,0,136,138,3,30,15,0,137,135,1,0,0,0,137,138,1,0,0,0,138,
        141,1,0,0,0,139,141,3,30,15,0,140,134,1,0,0,0,140,139,1,0,0,0,141,
        27,1,0,0,0,142,147,3,34,17,0,143,144,5,6,0,0,144,146,3,34,17,0,145,
        143,1,0,0,0,146,149,1,0,0,0,147,145,1,0,0,0,147,148,1,0,0,0,148,
        29,1,0,0,0,149,147,1,0,0,0,150,155,3,32,16,0,151,152,5,6,0,0,152,
        154,3,32,16,0,153,151,1,0,0,0,154,157,1,0,0,0,155,153,1,0,0,0,155,
        156,1,0,0,0,156,31,1,0,0,0,157,155,1,0,0,0,158,159,5,16,0,0,159,
        160,5,14,0,0,160,161,3,34,17,0,161,33,1,0,0,0,162,163,6,17,-1,0,
        163,176,5,17,0,0,164,176,5,18,0,0,165,176,5,16,0,0,166,168,5,12,
        0,0,167,169,3,36,18,0,168,167,1,0,0,0,168,169,1,0,0,0,169,170,1,
        0,0,0,170,176,5,13,0,0,171,172,5,2,0,0,172,173,3,34,17,0,173,174,
        5,3,0,0,174,176,1,0,0,0,175,162,1,0,0,0,175,164,1,0,0,0,175,165,
        1,0,0,0,175,166,1,0,0,0,175,171,1,0,0,0,176,185,1,0,0,0,177,178,
        10,7,0,0,178,179,7,0,0,0,179,184,3,34,17,8,180,181,10,6,0,0,181,
        182,7,1,0,0,182,184,3,34,17,7,183,177,1,0,0,0,183,180,1,0,0,0,184,
        187,1,0,0,0,185,183,1,0,0,0,185,186,1,0,0,0,186,35,1,0,0,0,187,185,
        1,0,0,0,188,194,3,34,17,0,189,190,3,34,17,0,190,191,5,6,0,0,191,
        192,3,36,18,0,192,194,1,0,0,0,193,188,1,0,0,0,193,189,1,0,0,0,194,
        37,1,0,0,0,19,41,50,70,75,81,87,102,113,118,124,137,140,147,155,
        168,175,183,185,193
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
    RULE_body = 4
    RULE_block = 5
    RULE_letExpr = 6
    RULE_letBindingList = 7
    RULE_letBinding = 8
    RULE_paramList = 9
    RULE_param = 10
    RULE_moduleDefinition = 11
    RULE_assignment = 12
    RULE_argList = 13
    RULE_positionalArgs = 14
    RULE_namedArgs = 15
    RULE_namedArg = 16
    RULE_expr = 17
    RULE_exprList = 18

    ruleNames =  [ "start", "statement", "moduleCallSeq", "moduleCall", 
                   "body", "block", "letExpr", "letBindingList", "letBinding", 
                   "paramList", "param", "moduleDefinition", "assignment", 
                   "argList", "positionalArgs", "namedArgs", "namedArg", 
                   "expr", "exprList" ]

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

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterStart" ):
                listener.enterStart(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitStart" ):
                listener.exitStart(self)

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
            self.state = 41
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 98448) != 0):
                self.state = 38
                self.statement()
                self.state = 43
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 44
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


        def block(self):
            return self.getTypedRuleContext(OpenSCADParser.BlockContext,0)


        def getRuleIndex(self):
            return OpenSCADParser.RULE_statement

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterStatement" ):
                listener.enterStatement(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitStatement" ):
                listener.exitStatement(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitStatement" ):
                return visitor.visitStatement(self)
            else:
                return visitor.visitChildren(self)




    def statement(self):

        localctx = OpenSCADParser.StatementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_statement)
        try:
            self.state = 50
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,1,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 46
                self.moduleCallSeq()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 47
                self.moduleDefinition()
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 48
                self.assignment()
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 49
                self.block()
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



    class ChainedLetCallContext(ModuleCallSeqContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a OpenSCADParser.ModuleCallSeqContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def letExpr(self):
            return self.getTypedRuleContext(OpenSCADParser.LetExprContext,0)

        def moduleCallSeq(self):
            return self.getTypedRuleContext(OpenSCADParser.ModuleCallSeqContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterChainedLetCall" ):
                listener.enterChainedLetCall(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitChainedLetCall" ):
                listener.exitChainedLetCall(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitChainedLetCall" ):
                return visitor.visitChainedLetCall(self)
            else:
                return visitor.visitChildren(self)


    class TerminalLetContext(ModuleCallSeqContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a OpenSCADParser.ModuleCallSeqContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def letExpr(self):
            return self.getTypedRuleContext(OpenSCADParser.LetExprContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterTerminalLet" ):
                listener.enterTerminalLet(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitTerminalLet" ):
                listener.exitTerminalLet(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitTerminalLet" ):
                return visitor.visitTerminalLet(self)
            else:
                return visitor.visitChildren(self)


    class LetWithBlockContext(ModuleCallSeqContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a OpenSCADParser.ModuleCallSeqContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def letExpr(self):
            return self.getTypedRuleContext(OpenSCADParser.LetExprContext,0)

        def block(self):
            return self.getTypedRuleContext(OpenSCADParser.BlockContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterLetWithBlock" ):
                listener.enterLetWithBlock(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitLetWithBlock" ):
                listener.exitLetWithBlock(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitLetWithBlock" ):
                return visitor.visitLetWithBlock(self)
            else:
                return visitor.visitChildren(self)


    class ModuleCallWithBlockContext(ModuleCallSeqContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a OpenSCADParser.ModuleCallSeqContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def moduleCall(self):
            return self.getTypedRuleContext(OpenSCADParser.ModuleCallContext,0)

        def block(self):
            return self.getTypedRuleContext(OpenSCADParser.BlockContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterModuleCallWithBlock" ):
                listener.enterModuleCallWithBlock(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitModuleCallWithBlock" ):
                listener.exitModuleCallWithBlock(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitModuleCallWithBlock" ):
                return visitor.visitModuleCallWithBlock(self)
            else:
                return visitor.visitChildren(self)


    class TerminalModuleCallContext(ModuleCallSeqContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a OpenSCADParser.ModuleCallSeqContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def moduleCall(self):
            return self.getTypedRuleContext(OpenSCADParser.ModuleCallContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterTerminalModuleCall" ):
                listener.enterTerminalModuleCall(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitTerminalModuleCall" ):
                listener.exitTerminalModuleCall(self)

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


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterChainedModuleCall" ):
                listener.enterChainedModuleCall(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitChainedModuleCall" ):
                listener.exitChainedModuleCall(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitChainedModuleCall" ):
                return visitor.visitChainedModuleCall(self)
            else:
                return visitor.visitChildren(self)



    def moduleCallSeq(self):

        localctx = OpenSCADParser.ModuleCallSeqContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_moduleCallSeq)
        try:
            self.state = 70
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,2,self._ctx)
            if la_ == 1:
                localctx = OpenSCADParser.ChainedModuleCallContext(self, localctx)
                self.enterOuterAlt(localctx, 1)
                self.state = 52
                self.moduleCall()
                self.state = 53
                self.moduleCallSeq()
                pass

            elif la_ == 2:
                localctx = OpenSCADParser.ChainedLetCallContext(self, localctx)
                self.enterOuterAlt(localctx, 2)
                self.state = 55
                self.letExpr()
                self.state = 56
                self.moduleCallSeq()
                pass

            elif la_ == 3:
                localctx = OpenSCADParser.ModuleCallWithBlockContext(self, localctx)
                self.enterOuterAlt(localctx, 3)
                self.state = 58
                self.moduleCall()
                self.state = 59
                self.block()
                pass

            elif la_ == 4:
                localctx = OpenSCADParser.LetWithBlockContext(self, localctx)
                self.enterOuterAlt(localctx, 4)
                self.state = 61
                self.letExpr()
                self.state = 62
                self.block()
                pass

            elif la_ == 5:
                localctx = OpenSCADParser.TerminalModuleCallContext(self, localctx)
                self.enterOuterAlt(localctx, 5)
                self.state = 64
                self.moduleCall()
                self.state = 65
                self.match(OpenSCADParser.T__0)
                pass

            elif la_ == 6:
                localctx = OpenSCADParser.TerminalLetContext(self, localctx)
                self.enterOuterAlt(localctx, 6)
                self.state = 67
                self.letExpr()
                self.state = 68
                self.match(OpenSCADParser.T__0)
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

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterModuleCall" ):
                listener.enterModuleCall(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitModuleCall" ):
                listener.exitModuleCall(self)

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
            self.state = 72
            self.match(OpenSCADParser.IDENT)
            self.state = 73
            self.match(OpenSCADParser.T__1)
            self.state = 75
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if (((_la) & ~0x3f) == 0 and ((1 << _la) & 462852) != 0):
                self.state = 74
                self.argList()


            self.state = 77
            self.match(OpenSCADParser.T__2)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class BodyContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def block(self):
            return self.getTypedRuleContext(OpenSCADParser.BlockContext,0)


        def moduleCallSeq(self):
            return self.getTypedRuleContext(OpenSCADParser.ModuleCallSeqContext,0)


        def getRuleIndex(self):
            return OpenSCADParser.RULE_body

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterBody" ):
                listener.enterBody(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitBody" ):
                listener.exitBody(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitBody" ):
                return visitor.visitBody(self)
            else:
                return visitor.visitChildren(self)




    def body(self):

        localctx = OpenSCADParser.BodyContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_body)
        try:
            self.state = 81
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [4]:
                self.enterOuterAlt(localctx, 1)
                self.state = 79
                self.block()
                pass
            elif token in [15, 16]:
                self.enterOuterAlt(localctx, 2)
                self.state = 80
                self.moduleCallSeq()
                pass
            else:
                raise NoViableAltException(self)

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

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterBlock" ):
                listener.enterBlock(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitBlock" ):
                listener.exitBlock(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitBlock" ):
                return visitor.visitBlock(self)
            else:
                return visitor.visitChildren(self)




    def block(self):

        localctx = OpenSCADParser.BlockContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_block)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 83
            self.match(OpenSCADParser.T__3)
            self.state = 87
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 98448) != 0):
                self.state = 84
                self.statement()
                self.state = 89
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 90
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

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterLetExpr" ):
                listener.enterLetExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitLetExpr" ):
                listener.exitLetExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitLetExpr" ):
                return visitor.visitLetExpr(self)
            else:
                return visitor.visitChildren(self)




    def letExpr(self):

        localctx = OpenSCADParser.LetExprContext(self, self._ctx, self.state)
        self.enterRule(localctx, 12, self.RULE_letExpr)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 92
            self.match(OpenSCADParser.LET)
            self.state = 93
            self.match(OpenSCADParser.T__1)
            self.state = 94
            self.letBindingList()
            self.state = 95
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

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterLetBindingList" ):
                listener.enterLetBindingList(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitLetBindingList" ):
                listener.exitLetBindingList(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitLetBindingList" ):
                return visitor.visitLetBindingList(self)
            else:
                return visitor.visitChildren(self)




    def letBindingList(self):

        localctx = OpenSCADParser.LetBindingListContext(self, self._ctx, self.state)
        self.enterRule(localctx, 14, self.RULE_letBindingList)
        try:
            self.state = 102
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,6,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 97
                self.letBinding()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 98
                self.letBinding()
                self.state = 99
                self.match(OpenSCADParser.T__5)
                self.state = 100
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

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterLetBinding" ):
                listener.enterLetBinding(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitLetBinding" ):
                listener.exitLetBinding(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitLetBinding" ):
                return visitor.visitLetBinding(self)
            else:
                return visitor.visitChildren(self)




    def letBinding(self):

        localctx = OpenSCADParser.LetBindingContext(self, self._ctx, self.state)
        self.enterRule(localctx, 16, self.RULE_letBinding)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 104
            self.match(OpenSCADParser.IDENT)
            self.state = 105
            self.match(OpenSCADParser.EQ)
            self.state = 106
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

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterParamList" ):
                listener.enterParamList(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitParamList" ):
                listener.exitParamList(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitParamList" ):
                return visitor.visitParamList(self)
            else:
                return visitor.visitChildren(self)




    def paramList(self):

        localctx = OpenSCADParser.ParamListContext(self, self._ctx, self.state)
        self.enterRule(localctx, 18, self.RULE_paramList)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 108
            self.param()
            self.state = 113
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==6:
                self.state = 109
                self.match(OpenSCADParser.T__5)
                self.state = 110
                self.param()
                self.state = 115
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

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterParamNoDefault" ):
                listener.enterParamNoDefault(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitParamNoDefault" ):
                listener.exitParamNoDefault(self)

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


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterParamWithDefault" ):
                listener.enterParamWithDefault(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitParamWithDefault" ):
                listener.exitParamWithDefault(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitParamWithDefault" ):
                return visitor.visitParamWithDefault(self)
            else:
                return visitor.visitChildren(self)



    def param(self):

        localctx = OpenSCADParser.ParamContext(self, self._ctx, self.state)
        self.enterRule(localctx, 20, self.RULE_param)
        try:
            self.state = 118
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,8,self._ctx)
            if la_ == 1:
                localctx = OpenSCADParser.ParamNoDefaultContext(self, localctx)
                self.enterOuterAlt(localctx, 1)
                self.state = 116
                self.match(OpenSCADParser.IDENT)
                pass

            elif la_ == 2:
                localctx = OpenSCADParser.ParamWithDefaultContext(self, localctx)
                self.enterOuterAlt(localctx, 2)
                self.state = 117
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

        def body(self):
            return self.getTypedRuleContext(OpenSCADParser.BodyContext,0)


        def paramList(self):
            return self.getTypedRuleContext(OpenSCADParser.ParamListContext,0)


        def getRuleIndex(self):
            return OpenSCADParser.RULE_moduleDefinition

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterModuleDefinition" ):
                listener.enterModuleDefinition(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitModuleDefinition" ):
                listener.exitModuleDefinition(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitModuleDefinition" ):
                return visitor.visitModuleDefinition(self)
            else:
                return visitor.visitChildren(self)




    def moduleDefinition(self):

        localctx = OpenSCADParser.ModuleDefinitionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 22, self.RULE_moduleDefinition)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 120
            self.match(OpenSCADParser.T__6)
            self.state = 121
            self.match(OpenSCADParser.IDENT)
            self.state = 122
            self.match(OpenSCADParser.T__1)
            self.state = 124
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==16:
                self.state = 123
                self.paramList()


            self.state = 126
            self.match(OpenSCADParser.T__2)
            self.state = 127
            self.body()
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

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAssignment" ):
                listener.enterAssignment(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAssignment" ):
                listener.exitAssignment(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAssignment" ):
                return visitor.visitAssignment(self)
            else:
                return visitor.visitChildren(self)




    def assignment(self):

        localctx = OpenSCADParser.AssignmentContext(self, self._ctx, self.state)
        self.enterRule(localctx, 24, self.RULE_assignment)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 129
            self.match(OpenSCADParser.IDENT)
            self.state = 130
            self.match(OpenSCADParser.EQ)
            self.state = 131
            self.expr(0)
            self.state = 132
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

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterArgList" ):
                listener.enterArgList(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitArgList" ):
                listener.exitArgList(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitArgList" ):
                return visitor.visitArgList(self)
            else:
                return visitor.visitChildren(self)




    def argList(self):

        localctx = OpenSCADParser.ArgListContext(self, self._ctx, self.state)
        self.enterRule(localctx, 26, self.RULE_argList)
        self._la = 0 # Token type
        try:
            self.state = 140
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,11,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 134
                self.positionalArgs()
                self.state = 137
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==6:
                    self.state = 135
                    self.match(OpenSCADParser.T__5)
                    self.state = 136
                    self.namedArgs()


                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 139
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

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPositionalArgs" ):
                listener.enterPositionalArgs(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPositionalArgs" ):
                listener.exitPositionalArgs(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitPositionalArgs" ):
                return visitor.visitPositionalArgs(self)
            else:
                return visitor.visitChildren(self)




    def positionalArgs(self):

        localctx = OpenSCADParser.PositionalArgsContext(self, self._ctx, self.state)
        self.enterRule(localctx, 28, self.RULE_positionalArgs)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 142
            self.expr(0)
            self.state = 147
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,12,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 143
                    self.match(OpenSCADParser.T__5)
                    self.state = 144
                    self.expr(0) 
                self.state = 149
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,12,self._ctx)

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

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterNamedArgs" ):
                listener.enterNamedArgs(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitNamedArgs" ):
                listener.exitNamedArgs(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitNamedArgs" ):
                return visitor.visitNamedArgs(self)
            else:
                return visitor.visitChildren(self)




    def namedArgs(self):

        localctx = OpenSCADParser.NamedArgsContext(self, self._ctx, self.state)
        self.enterRule(localctx, 30, self.RULE_namedArgs)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 150
            self.namedArg()
            self.state = 155
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==6:
                self.state = 151
                self.match(OpenSCADParser.T__5)
                self.state = 152
                self.namedArg()
                self.state = 157
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

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterNamedArg" ):
                listener.enterNamedArg(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitNamedArg" ):
                listener.exitNamedArg(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitNamedArg" ):
                return visitor.visitNamedArg(self)
            else:
                return visitor.visitChildren(self)




    def namedArg(self):

        localctx = OpenSCADParser.NamedArgContext(self, self._ctx, self.state)
        self.enterRule(localctx, 32, self.RULE_namedArg)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 158
            self.match(OpenSCADParser.IDENT)
            self.state = 159
            self.match(OpenSCADParser.EQ)
            self.state = 160
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

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterStringExpr" ):
                listener.enterStringExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitStringExpr" ):
                listener.exitStringExpr(self)

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


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterMultiplicativeExpr" ):
                listener.enterMultiplicativeExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitMultiplicativeExpr" ):
                listener.exitMultiplicativeExpr(self)

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

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterIdentExpr" ):
                listener.enterIdentExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitIdentExpr" ):
                listener.exitIdentExpr(self)

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


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterArrayExpr" ):
                listener.enterArrayExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitArrayExpr" ):
                listener.exitArrayExpr(self)

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


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAdditiveExpr" ):
                listener.enterAdditiveExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAdditiveExpr" ):
                listener.exitAdditiveExpr(self)

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

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterNumberExpr" ):
                listener.enterNumberExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitNumberExpr" ):
                listener.exitNumberExpr(self)

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


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterParenExpr" ):
                listener.enterParenExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitParenExpr" ):
                listener.exitParenExpr(self)

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
        _startState = 34
        self.enterRecursionRule(localctx, 34, self.RULE_expr, _p)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 175
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [17]:
                localctx = OpenSCADParser.NumberExprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx

                self.state = 163
                self.match(OpenSCADParser.NUMBER)
                pass
            elif token in [18]:
                localctx = OpenSCADParser.StringExprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 164
                self.match(OpenSCADParser.STRING)
                pass
            elif token in [16]:
                localctx = OpenSCADParser.IdentExprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 165
                self.match(OpenSCADParser.IDENT)
                pass
            elif token in [12]:
                localctx = OpenSCADParser.ArrayExprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 166
                self.match(OpenSCADParser.T__11)
                self.state = 168
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if (((_la) & ~0x3f) == 0 and ((1 << _la) & 462852) != 0):
                    self.state = 167
                    self.exprList()


                self.state = 170
                self.match(OpenSCADParser.T__12)
                pass
            elif token in [2]:
                localctx = OpenSCADParser.ParenExprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 171
                self.match(OpenSCADParser.T__1)
                self.state = 172
                self.expr(0)
                self.state = 173
                self.match(OpenSCADParser.T__2)
                pass
            else:
                raise NoViableAltException(self)

            self._ctx.stop = self._input.LT(-1)
            self.state = 185
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,17,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    self.state = 183
                    self._errHandler.sync(self)
                    la_ = self._interp.adaptivePredict(self._input,16,self._ctx)
                    if la_ == 1:
                        localctx = OpenSCADParser.MultiplicativeExprContext(self, OpenSCADParser.ExprContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 177
                        if not self.precpred(self._ctx, 7):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 7)")
                        self.state = 178
                        _la = self._input.LA(1)
                        if not(_la==8 or _la==9):
                            self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 179
                        self.expr(8)
                        pass

                    elif la_ == 2:
                        localctx = OpenSCADParser.AdditiveExprContext(self, OpenSCADParser.ExprContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 180
                        if not self.precpred(self._ctx, 6):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 6)")
                        self.state = 181
                        _la = self._input.LA(1)
                        if not(_la==10 or _la==11):
                            self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 182
                        self.expr(7)
                        pass

             
                self.state = 187
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,17,self._ctx)

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

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterExprList" ):
                listener.enterExprList(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitExprList" ):
                listener.exitExprList(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitExprList" ):
                return visitor.visitExprList(self)
            else:
                return visitor.visitChildren(self)




    def exprList(self):

        localctx = OpenSCADParser.ExprListContext(self, self._ctx, self.state)
        self.enterRule(localctx, 36, self.RULE_exprList)
        try:
            self.state = 193
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,18,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 188
                self.expr(0)
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 189
                self.expr(0)
                self.state = 190
                self.match(OpenSCADParser.T__5)
                self.state = 191
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
        self._predicates[17] = self.expr_sempred
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
         




