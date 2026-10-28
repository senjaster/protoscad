# Generated from C:/Users/arsbir/Documents/protoscad/src/protoscad/grammar/OpenSCAD.g4 by ANTLR 4.13.2
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
        4,1,38,256,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,2,6,7,
        6,2,7,7,7,2,8,7,8,2,9,7,9,2,10,7,10,2,11,7,11,2,12,7,12,2,13,7,13,
        2,14,7,14,2,15,7,15,2,16,7,16,2,17,7,17,2,18,7,18,2,19,7,19,1,0,
        5,0,42,8,0,10,0,12,0,45,9,0,1,0,1,0,1,1,1,1,1,1,1,1,3,1,53,8,1,1,
        2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,
        2,1,2,3,2,73,8,2,1,3,1,3,1,3,3,3,78,8,3,1,3,1,3,1,4,1,4,3,4,84,8,
        4,1,5,1,5,5,5,88,8,5,10,5,12,5,91,9,5,1,5,1,5,1,6,1,6,1,6,1,6,1,
        6,1,7,1,7,1,7,1,7,1,7,3,7,105,8,7,1,8,1,8,1,8,1,8,1,9,1,9,1,9,5,
        9,114,8,9,10,9,12,9,117,9,9,1,10,1,10,3,10,121,8,10,1,11,1,11,1,
        11,1,11,3,11,127,8,11,1,11,1,11,1,11,1,12,1,12,1,12,1,12,1,12,1,
        13,1,13,1,13,3,13,140,8,13,1,13,3,13,143,8,13,1,14,1,14,1,14,5,14,
        148,8,14,10,14,12,14,151,9,14,1,15,1,15,1,15,5,15,156,8,15,10,15,
        12,15,159,9,15,1,16,1,16,1,16,1,16,1,17,1,17,1,17,1,17,1,17,1,17,
        1,17,1,17,1,17,1,17,1,17,1,17,3,17,177,8,17,1,17,1,17,1,17,1,17,
        1,17,1,17,1,17,1,17,1,17,1,17,1,17,1,17,1,17,1,17,1,17,1,17,1,17,
        1,17,1,17,1,17,1,17,3,17,200,8,17,1,17,1,17,1,17,1,17,1,17,1,17,
        1,17,1,17,1,17,1,17,1,17,1,17,1,17,1,17,1,17,1,17,1,17,1,17,1,17,
        1,17,1,17,1,17,1,17,1,17,1,17,1,17,1,17,1,17,1,17,1,17,1,17,1,17,
        1,17,1,17,1,17,5,17,237,8,17,10,17,12,17,240,9,17,1,18,1,18,1,18,
        1,18,1,18,3,18,247,8,18,1,19,1,19,1,19,1,19,1,19,3,19,254,8,19,1,
        19,0,1,34,20,0,2,4,6,8,10,12,14,16,18,20,22,24,26,28,30,32,34,36,
        38,0,5,1,0,12,14,1,0,15,17,1,0,12,13,1,0,28,31,1,0,32,33,280,0,43,
        1,0,0,0,2,52,1,0,0,0,4,72,1,0,0,0,6,74,1,0,0,0,8,83,1,0,0,0,10,85,
        1,0,0,0,12,94,1,0,0,0,14,104,1,0,0,0,16,106,1,0,0,0,18,110,1,0,0,
        0,20,120,1,0,0,0,22,122,1,0,0,0,24,131,1,0,0,0,26,142,1,0,0,0,28,
        144,1,0,0,0,30,152,1,0,0,0,32,160,1,0,0,0,34,199,1,0,0,0,36,241,
        1,0,0,0,38,253,1,0,0,0,40,42,3,2,1,0,41,40,1,0,0,0,42,45,1,0,0,0,
        43,41,1,0,0,0,43,44,1,0,0,0,44,46,1,0,0,0,45,43,1,0,0,0,46,47,5,
        0,0,1,47,1,1,0,0,0,48,53,3,4,2,0,49,53,3,22,11,0,50,53,3,24,12,0,
        51,53,3,10,5,0,52,48,1,0,0,0,52,49,1,0,0,0,52,50,1,0,0,0,52,51,1,
        0,0,0,53,3,1,0,0,0,54,55,3,6,3,0,55,56,3,4,2,0,56,73,1,0,0,0,57,
        58,3,12,6,0,58,59,3,4,2,0,59,73,1,0,0,0,60,61,3,6,3,0,61,62,3,10,
        5,0,62,73,1,0,0,0,63,64,3,12,6,0,64,65,3,10,5,0,65,73,1,0,0,0,66,
        67,3,6,3,0,67,68,5,1,0,0,68,73,1,0,0,0,69,70,3,12,6,0,70,71,5,1,
        0,0,71,73,1,0,0,0,72,54,1,0,0,0,72,57,1,0,0,0,72,60,1,0,0,0,72,63,
        1,0,0,0,72,66,1,0,0,0,72,69,1,0,0,0,73,5,1,0,0,0,74,75,5,25,0,0,
        75,77,5,2,0,0,76,78,3,26,13,0,77,76,1,0,0,0,77,78,1,0,0,0,78,79,
        1,0,0,0,79,80,5,3,0,0,80,7,1,0,0,0,81,84,3,10,5,0,82,84,3,4,2,0,
        83,81,1,0,0,0,83,82,1,0,0,0,84,9,1,0,0,0,85,89,5,4,0,0,86,88,3,2,
        1,0,87,86,1,0,0,0,88,91,1,0,0,0,89,87,1,0,0,0,89,90,1,0,0,0,90,92,
        1,0,0,0,91,89,1,0,0,0,92,93,5,5,0,0,93,11,1,0,0,0,94,95,5,21,0,0,
        95,96,5,2,0,0,96,97,3,14,7,0,97,98,5,3,0,0,98,13,1,0,0,0,99,105,
        3,16,8,0,100,101,3,16,8,0,101,102,5,6,0,0,102,103,3,14,7,0,103,105,
        1,0,0,0,104,99,1,0,0,0,104,100,1,0,0,0,105,15,1,0,0,0,106,107,5,
        25,0,0,107,108,5,20,0,0,108,109,3,34,17,0,109,17,1,0,0,0,110,115,
        3,20,10,0,111,112,5,6,0,0,112,114,3,20,10,0,113,111,1,0,0,0,114,
        117,1,0,0,0,115,113,1,0,0,0,115,116,1,0,0,0,116,19,1,0,0,0,117,115,
        1,0,0,0,118,121,5,25,0,0,119,121,3,16,8,0,120,118,1,0,0,0,120,119,
        1,0,0,0,121,21,1,0,0,0,122,123,5,7,0,0,123,124,5,25,0,0,124,126,
        5,2,0,0,125,127,3,18,9,0,126,125,1,0,0,0,126,127,1,0,0,0,127,128,
        1,0,0,0,128,129,5,3,0,0,129,130,3,8,4,0,130,23,1,0,0,0,131,132,5,
        25,0,0,132,133,5,20,0,0,133,134,3,34,17,0,134,135,5,1,0,0,135,25,
        1,0,0,0,136,139,3,28,14,0,137,138,5,6,0,0,138,140,3,30,15,0,139,
        137,1,0,0,0,139,140,1,0,0,0,140,143,1,0,0,0,141,143,3,30,15,0,142,
        136,1,0,0,0,142,141,1,0,0,0,143,27,1,0,0,0,144,149,3,34,17,0,145,
        146,5,6,0,0,146,148,3,34,17,0,147,145,1,0,0,0,148,151,1,0,0,0,149,
        147,1,0,0,0,149,150,1,0,0,0,150,29,1,0,0,0,151,149,1,0,0,0,152,157,
        3,32,16,0,153,154,5,6,0,0,154,156,3,32,16,0,155,153,1,0,0,0,156,
        159,1,0,0,0,157,155,1,0,0,0,157,158,1,0,0,0,158,31,1,0,0,0,159,157,
        1,0,0,0,160,161,5,25,0,0,161,162,5,20,0,0,162,163,3,34,17,0,163,
        33,1,0,0,0,164,165,6,17,-1,0,165,166,7,0,0,0,166,200,3,34,17,20,
        167,200,5,26,0,0,168,200,5,27,0,0,169,200,5,22,0,0,170,200,5,23,
        0,0,171,200,5,24,0,0,172,200,5,25,0,0,173,174,5,25,0,0,174,176,5,
        2,0,0,175,177,3,26,13,0,176,175,1,0,0,0,176,177,1,0,0,0,177,178,
        1,0,0,0,178,200,5,3,0,0,179,180,5,8,0,0,180,181,3,38,19,0,181,182,
        5,9,0,0,182,200,1,0,0,0,183,184,5,8,0,0,184,200,5,9,0,0,185,186,
        5,8,0,0,186,187,3,36,18,0,187,188,5,9,0,0,188,200,1,0,0,0,189,190,
        5,21,0,0,190,191,5,2,0,0,191,192,3,14,7,0,192,193,5,3,0,0,193,194,
        3,34,17,2,194,200,1,0,0,0,195,196,5,2,0,0,196,197,3,34,17,0,197,
        198,5,3,0,0,198,200,1,0,0,0,199,164,1,0,0,0,199,167,1,0,0,0,199,
        168,1,0,0,0,199,169,1,0,0,0,199,170,1,0,0,0,199,171,1,0,0,0,199,
        172,1,0,0,0,199,173,1,0,0,0,199,179,1,0,0,0,199,183,1,0,0,0,199,
        185,1,0,0,0,199,189,1,0,0,0,199,195,1,0,0,0,200,238,1,0,0,0,201,
        202,10,21,0,0,202,203,5,11,0,0,203,237,3,34,17,21,204,205,10,19,
        0,0,205,206,7,1,0,0,206,237,3,34,17,20,207,208,10,18,0,0,208,209,
        7,2,0,0,209,237,3,34,17,19,210,211,10,17,0,0,211,212,7,3,0,0,212,
        237,3,34,17,18,213,214,10,16,0,0,214,215,7,4,0,0,215,237,3,34,17,
        17,216,217,10,15,0,0,217,218,5,34,0,0,218,237,3,34,17,16,219,220,
        10,14,0,0,220,221,5,35,0,0,221,237,3,34,17,15,222,223,10,13,0,0,
        223,224,5,18,0,0,224,225,3,34,17,0,225,226,5,19,0,0,226,227,3,34,
        17,13,227,237,1,0,0,0,228,229,10,23,0,0,229,230,5,8,0,0,230,231,
        3,34,17,0,231,232,5,9,0,0,232,237,1,0,0,0,233,234,10,22,0,0,234,
        235,5,10,0,0,235,237,5,25,0,0,236,201,1,0,0,0,236,204,1,0,0,0,236,
        207,1,0,0,0,236,210,1,0,0,0,236,213,1,0,0,0,236,216,1,0,0,0,236,
        219,1,0,0,0,236,222,1,0,0,0,236,228,1,0,0,0,236,233,1,0,0,0,237,
        240,1,0,0,0,238,236,1,0,0,0,238,239,1,0,0,0,239,35,1,0,0,0,240,238,
        1,0,0,0,241,242,3,34,17,0,242,243,5,19,0,0,243,246,3,34,17,0,244,
        245,5,19,0,0,245,247,3,34,17,0,246,244,1,0,0,0,246,247,1,0,0,0,247,
        37,1,0,0,0,248,254,3,34,17,0,249,250,3,34,17,0,250,251,5,6,0,0,251,
        252,3,38,19,0,252,254,1,0,0,0,253,248,1,0,0,0,253,249,1,0,0,0,254,
        39,1,0,0,0,20,43,52,72,77,83,89,104,115,120,126,139,142,149,157,
        176,199,236,238,246,253
    ]

class OpenSCADParser ( Parser ):

    grammarFileName = "OpenSCAD.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "';'", "'('", "')'", "'{'", "'}'", "','", 
                     "'module'", "'['", "']'", "'.'", "'^'", "'+'", "'-'", 
                     "'!'", "'*'", "'/'", "'%'", "'?'", "':'", "'='", "'let'", 
                     "'true'", "'false'", "'undef'", "<INVALID>", "<INVALID>", 
                     "<INVALID>", "'<'", "'<='", "'>'", "'>='", "'=='", 
                     "'!='", "'&&'", "'||'" ]

    symbolicNames = [ "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "EQ", "LET", "TRUE", "FALSE", "UNDEF", "IDENT", "NUMBER", 
                      "STRING", "LT", "LE", "GT", "GE", "EQEQ", "NE", "AND", 
                      "OR", "COMMENT", "BLOCK_CMT", "WS" ]

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
    RULE_range = 18
    RULE_exprList = 19

    ruleNames =  [ "start", "statement", "moduleCallSeq", "moduleCall", 
                   "body", "block", "letExpr", "letBindingList", "letBinding", 
                   "paramList", "param", "moduleDefinition", "assignment", 
                   "argList", "positionalArgs", "namedArgs", "namedArg", 
                   "expr", "range", "exprList" ]

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
    T__13=14
    T__14=15
    T__15=16
    T__16=17
    T__17=18
    T__18=19
    EQ=20
    LET=21
    TRUE=22
    FALSE=23
    UNDEF=24
    IDENT=25
    NUMBER=26
    STRING=27
    LT=28
    LE=29
    GT=30
    GE=31
    EQEQ=32
    NE=33
    AND=34
    OR=35
    COMMENT=36
    BLOCK_CMT=37
    WS=38

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
            self.state = 43
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 35651728) != 0):
                self.state = 40
                self.statement()
                self.state = 45
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 46
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
            self.state = 52
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,1,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 48
                self.moduleCallSeq()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 49
                self.moduleDefinition()
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 50
                self.assignment()
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 51
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
            self.state = 72
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,2,self._ctx)
            if la_ == 1:
                localctx = OpenSCADParser.ChainedModuleCallContext(self, localctx)
                self.enterOuterAlt(localctx, 1)
                self.state = 54
                self.moduleCall()
                self.state = 55
                self.moduleCallSeq()
                pass

            elif la_ == 2:
                localctx = OpenSCADParser.ChainedLetCallContext(self, localctx)
                self.enterOuterAlt(localctx, 2)
                self.state = 57
                self.letExpr()
                self.state = 58
                self.moduleCallSeq()
                pass

            elif la_ == 3:
                localctx = OpenSCADParser.ModuleCallWithBlockContext(self, localctx)
                self.enterOuterAlt(localctx, 3)
                self.state = 60
                self.moduleCall()
                self.state = 61
                self.block()
                pass

            elif la_ == 4:
                localctx = OpenSCADParser.LetWithBlockContext(self, localctx)
                self.enterOuterAlt(localctx, 4)
                self.state = 63
                self.letExpr()
                self.state = 64
                self.block()
                pass

            elif la_ == 5:
                localctx = OpenSCADParser.TerminalModuleCallContext(self, localctx)
                self.enterOuterAlt(localctx, 5)
                self.state = 66
                self.moduleCall()
                self.state = 67
                self.match(OpenSCADParser.T__0)
                pass

            elif la_ == 6:
                localctx = OpenSCADParser.TerminalLetContext(self, localctx)
                self.enterOuterAlt(localctx, 6)
                self.state = 69
                self.letExpr()
                self.state = 70
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
            self.state = 74
            self.match(OpenSCADParser.IDENT)
            self.state = 75
            self.match(OpenSCADParser.T__1)
            self.state = 77
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if (((_la) & ~0x3f) == 0 and ((1 << _la) & 266367236) != 0):
                self.state = 76
                self.argList()


            self.state = 79
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
            self.state = 83
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [4]:
                self.enterOuterAlt(localctx, 1)
                self.state = 81
                self.block()
                pass
            elif token in [21, 25]:
                self.enterOuterAlt(localctx, 2)
                self.state = 82
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
            self.state = 85
            self.match(OpenSCADParser.T__3)
            self.state = 89
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 35651728) != 0):
                self.state = 86
                self.statement()
                self.state = 91
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 92
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
            self.state = 94
            self.match(OpenSCADParser.LET)
            self.state = 95
            self.match(OpenSCADParser.T__1)
            self.state = 96
            self.letBindingList()
            self.state = 97
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
            self.state = 104
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,6,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 99
                self.letBinding()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 100
                self.letBinding()
                self.state = 101
                self.match(OpenSCADParser.T__5)
                self.state = 102
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
            self.state = 106
            self.match(OpenSCADParser.IDENT)
            self.state = 107
            self.match(OpenSCADParser.EQ)
            self.state = 108
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
            self.state = 110
            self.param()
            self.state = 115
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==6:
                self.state = 111
                self.match(OpenSCADParser.T__5)
                self.state = 112
                self.param()
                self.state = 117
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
            self.state = 120
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,8,self._ctx)
            if la_ == 1:
                localctx = OpenSCADParser.ParamNoDefaultContext(self, localctx)
                self.enterOuterAlt(localctx, 1)
                self.state = 118
                self.match(OpenSCADParser.IDENT)
                pass

            elif la_ == 2:
                localctx = OpenSCADParser.ParamWithDefaultContext(self, localctx)
                self.enterOuterAlt(localctx, 2)
                self.state = 119
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
            self.state = 122
            self.match(OpenSCADParser.T__6)
            self.state = 123
            self.match(OpenSCADParser.IDENT)
            self.state = 124
            self.match(OpenSCADParser.T__1)
            self.state = 126
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==25:
                self.state = 125
                self.paramList()


            self.state = 128
            self.match(OpenSCADParser.T__2)
            self.state = 129
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
            self.state = 131
            self.match(OpenSCADParser.IDENT)
            self.state = 132
            self.match(OpenSCADParser.EQ)
            self.state = 133
            self.expr(0)
            self.state = 134
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
            self.state = 142
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,11,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 136
                self.positionalArgs()
                self.state = 139
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==6:
                    self.state = 137
                    self.match(OpenSCADParser.T__5)
                    self.state = 138
                    self.namedArgs()


                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 141
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
            self.state = 144
            self.expr(0)
            self.state = 149
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,12,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 145
                    self.match(OpenSCADParser.T__5)
                    self.state = 146
                    self.expr(0) 
                self.state = 151
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
            self.state = 152
            self.namedArg()
            self.state = 157
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==6:
                self.state = 153
                self.match(OpenSCADParser.T__5)
                self.state = 154
                self.namedArg()
                self.state = 159
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
            self.state = 160
            self.match(OpenSCADParser.IDENT)
            self.state = 161
            self.match(OpenSCADParser.EQ)
            self.state = 162
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


    class UndefExprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a OpenSCADParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def UNDEF(self):
            return self.getToken(OpenSCADParser.UNDEF, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterUndefExpr" ):
                listener.enterUndefExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitUndefExpr" ):
                listener.exitUndefExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitUndefExpr" ):
                return visitor.visitUndefExpr(self)
            else:
                return visitor.visitChildren(self)


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


    class TrueExprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a OpenSCADParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def TRUE(self):
            return self.getToken(OpenSCADParser.TRUE, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterTrueExpr" ):
                listener.enterTrueExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitTrueExpr" ):
                listener.exitTrueExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitTrueExpr" ):
                return visitor.visitTrueExpr(self)
            else:
                return visitor.visitChildren(self)


    class EmptyVectorExprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a OpenSCADParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterEmptyVectorExpr" ):
                listener.enterEmptyVectorExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitEmptyVectorExpr" ):
                listener.exitEmptyVectorExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitEmptyVectorExpr" ):
                return visitor.visitEmptyVectorExpr(self)
            else:
                return visitor.visitChildren(self)


    class RelationalExprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a OpenSCADParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(OpenSCADParser.ExprContext)
            else:
                return self.getTypedRuleContext(OpenSCADParser.ExprContext,i)

        def LT(self):
            return self.getToken(OpenSCADParser.LT, 0)
        def LE(self):
            return self.getToken(OpenSCADParser.LE, 0)
        def GT(self):
            return self.getToken(OpenSCADParser.GT, 0)
        def GE(self):
            return self.getToken(OpenSCADParser.GE, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterRelationalExpr" ):
                listener.enterRelationalExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitRelationalExpr" ):
                listener.exitRelationalExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitRelationalExpr" ):
                return visitor.visitRelationalExpr(self)
            else:
                return visitor.visitChildren(self)


    class RangeExprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a OpenSCADParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def range_(self):
            return self.getTypedRuleContext(OpenSCADParser.RangeContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterRangeExpr" ):
                listener.enterRangeExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitRangeExpr" ):
                listener.exitRangeExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitRangeExpr" ):
                return visitor.visitRangeExpr(self)
            else:
                return visitor.visitChildren(self)


    class UnaryExprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a OpenSCADParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def expr(self):
            return self.getTypedRuleContext(OpenSCADParser.ExprContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterUnaryExpr" ):
                listener.enterUnaryExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitUnaryExpr" ):
                listener.exitUnaryExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitUnaryExpr" ):
                return visitor.visitUnaryExpr(self)
            else:
                return visitor.visitChildren(self)


    class LogicalAndExprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a OpenSCADParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(OpenSCADParser.ExprContext)
            else:
                return self.getTypedRuleContext(OpenSCADParser.ExprContext,i)

        def AND(self):
            return self.getToken(OpenSCADParser.AND, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterLogicalAndExpr" ):
                listener.enterLogicalAndExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitLogicalAndExpr" ):
                listener.exitLogicalAndExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitLogicalAndExpr" ):
                return visitor.visitLogicalAndExpr(self)
            else:
                return visitor.visitChildren(self)


    class IndexExprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a OpenSCADParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(OpenSCADParser.ExprContext)
            else:
                return self.getTypedRuleContext(OpenSCADParser.ExprContext,i)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterIndexExpr" ):
                listener.enterIndexExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitIndexExpr" ):
                listener.exitIndexExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitIndexExpr" ):
                return visitor.visitIndexExpr(self)
            else:
                return visitor.visitChildren(self)


    class FalseExprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a OpenSCADParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def FALSE(self):
            return self.getToken(OpenSCADParser.FALSE, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterFalseExpr" ):
                listener.enterFalseExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitFalseExpr" ):
                listener.exitFalseExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitFalseExpr" ):
                return visitor.visitFalseExpr(self)
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


    class LogicalOrExprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a OpenSCADParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(OpenSCADParser.ExprContext)
            else:
                return self.getTypedRuleContext(OpenSCADParser.ExprContext,i)

        def OR(self):
            return self.getToken(OpenSCADParser.OR, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterLogicalOrExpr" ):
                listener.enterLogicalOrExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitLogicalOrExpr" ):
                listener.exitLogicalOrExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitLogicalOrExpr" ):
                return visitor.visitLogicalOrExpr(self)
            else:
                return visitor.visitChildren(self)


    class FunctionCallExprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a OpenSCADParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def IDENT(self):
            return self.getToken(OpenSCADParser.IDENT, 0)
        def argList(self):
            return self.getTypedRuleContext(OpenSCADParser.ArgListContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterFunctionCallExpr" ):
                listener.enterFunctionCallExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitFunctionCallExpr" ):
                listener.exitFunctionCallExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitFunctionCallExpr" ):
                return visitor.visitFunctionCallExpr(self)
            else:
                return visitor.visitChildren(self)


    class EqualityExprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a OpenSCADParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(OpenSCADParser.ExprContext)
            else:
                return self.getTypedRuleContext(OpenSCADParser.ExprContext,i)

        def EQEQ(self):
            return self.getToken(OpenSCADParser.EQEQ, 0)
        def NE(self):
            return self.getToken(OpenSCADParser.NE, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterEqualityExpr" ):
                listener.enterEqualityExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitEqualityExpr" ):
                listener.exitEqualityExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitEqualityExpr" ):
                return visitor.visitEqualityExpr(self)
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


    class MemberExprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a OpenSCADParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def expr(self):
            return self.getTypedRuleContext(OpenSCADParser.ExprContext,0)

        def IDENT(self):
            return self.getToken(OpenSCADParser.IDENT, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterMemberExpr" ):
                listener.enterMemberExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitMemberExpr" ):
                listener.exitMemberExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitMemberExpr" ):
                return visitor.visitMemberExpr(self)
            else:
                return visitor.visitChildren(self)


    class ExponentExprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a OpenSCADParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(OpenSCADParser.ExprContext)
            else:
                return self.getTypedRuleContext(OpenSCADParser.ExprContext,i)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterExponentExpr" ):
                listener.enterExponentExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitExponentExpr" ):
                listener.exitExponentExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitExponentExpr" ):
                return visitor.visitExponentExpr(self)
            else:
                return visitor.visitChildren(self)


    class LetExpressionContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a OpenSCADParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def LET(self):
            return self.getToken(OpenSCADParser.LET, 0)
        def letBindingList(self):
            return self.getTypedRuleContext(OpenSCADParser.LetBindingListContext,0)

        def expr(self):
            return self.getTypedRuleContext(OpenSCADParser.ExprContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterLetExpression" ):
                listener.enterLetExpression(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitLetExpression" ):
                listener.exitLetExpression(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitLetExpression" ):
                return visitor.visitLetExpression(self)
            else:
                return visitor.visitChildren(self)


    class VectorExprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a OpenSCADParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def exprList(self):
            return self.getTypedRuleContext(OpenSCADParser.ExprListContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterVectorExpr" ):
                listener.enterVectorExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitVectorExpr" ):
                listener.exitVectorExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitVectorExpr" ):
                return visitor.visitVectorExpr(self)
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


    class TernaryExprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a OpenSCADParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(OpenSCADParser.ExprContext)
            else:
                return self.getTypedRuleContext(OpenSCADParser.ExprContext,i)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterTernaryExpr" ):
                listener.enterTernaryExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitTernaryExpr" ):
                listener.exitTernaryExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitTernaryExpr" ):
                return visitor.visitTernaryExpr(self)
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
            self.state = 199
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,15,self._ctx)
            if la_ == 1:
                localctx = OpenSCADParser.UnaryExprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx

                self.state = 165
                _la = self._input.LA(1)
                if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 28672) != 0)):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 166
                self.expr(20)
                pass

            elif la_ == 2:
                localctx = OpenSCADParser.NumberExprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 167
                self.match(OpenSCADParser.NUMBER)
                pass

            elif la_ == 3:
                localctx = OpenSCADParser.StringExprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 168
                self.match(OpenSCADParser.STRING)
                pass

            elif la_ == 4:
                localctx = OpenSCADParser.TrueExprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 169
                self.match(OpenSCADParser.TRUE)
                pass

            elif la_ == 5:
                localctx = OpenSCADParser.FalseExprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 170
                self.match(OpenSCADParser.FALSE)
                pass

            elif la_ == 6:
                localctx = OpenSCADParser.UndefExprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 171
                self.match(OpenSCADParser.UNDEF)
                pass

            elif la_ == 7:
                localctx = OpenSCADParser.IdentExprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 172
                self.match(OpenSCADParser.IDENT)
                pass

            elif la_ == 8:
                localctx = OpenSCADParser.FunctionCallExprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 173
                self.match(OpenSCADParser.IDENT)
                self.state = 174
                self.match(OpenSCADParser.T__1)
                self.state = 176
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if (((_la) & ~0x3f) == 0 and ((1 << _la) & 266367236) != 0):
                    self.state = 175
                    self.argList()


                self.state = 178
                self.match(OpenSCADParser.T__2)
                pass

            elif la_ == 9:
                localctx = OpenSCADParser.VectorExprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 179
                self.match(OpenSCADParser.T__7)
                self.state = 180
                self.exprList()
                self.state = 181
                self.match(OpenSCADParser.T__8)
                pass

            elif la_ == 10:
                localctx = OpenSCADParser.EmptyVectorExprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 183
                self.match(OpenSCADParser.T__7)
                self.state = 184
                self.match(OpenSCADParser.T__8)
                pass

            elif la_ == 11:
                localctx = OpenSCADParser.RangeExprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 185
                self.match(OpenSCADParser.T__7)
                self.state = 186
                self.range_()
                self.state = 187
                self.match(OpenSCADParser.T__8)
                pass

            elif la_ == 12:
                localctx = OpenSCADParser.LetExpressionContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 189
                self.match(OpenSCADParser.LET)
                self.state = 190
                self.match(OpenSCADParser.T__1)
                self.state = 191
                self.letBindingList()
                self.state = 192
                self.match(OpenSCADParser.T__2)
                self.state = 193
                self.expr(2)
                pass

            elif la_ == 13:
                localctx = OpenSCADParser.ParenExprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 195
                self.match(OpenSCADParser.T__1)
                self.state = 196
                self.expr(0)
                self.state = 197
                self.match(OpenSCADParser.T__2)
                pass


            self._ctx.stop = self._input.LT(-1)
            self.state = 238
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,17,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    self.state = 236
                    self._errHandler.sync(self)
                    la_ = self._interp.adaptivePredict(self._input,16,self._ctx)
                    if la_ == 1:
                        localctx = OpenSCADParser.ExponentExprContext(self, OpenSCADParser.ExprContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 201
                        if not self.precpred(self._ctx, 21):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 21)")
                        self.state = 202
                        self.match(OpenSCADParser.T__10)
                        self.state = 203
                        self.expr(21)
                        pass

                    elif la_ == 2:
                        localctx = OpenSCADParser.MultiplicativeExprContext(self, OpenSCADParser.ExprContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 204
                        if not self.precpred(self._ctx, 19):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 19)")
                        self.state = 205
                        _la = self._input.LA(1)
                        if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 229376) != 0)):
                            self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 206
                        self.expr(20)
                        pass

                    elif la_ == 3:
                        localctx = OpenSCADParser.AdditiveExprContext(self, OpenSCADParser.ExprContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 207
                        if not self.precpred(self._ctx, 18):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 18)")
                        self.state = 208
                        _la = self._input.LA(1)
                        if not(_la==12 or _la==13):
                            self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 209
                        self.expr(19)
                        pass

                    elif la_ == 4:
                        localctx = OpenSCADParser.RelationalExprContext(self, OpenSCADParser.ExprContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 210
                        if not self.precpred(self._ctx, 17):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 17)")
                        self.state = 211
                        _la = self._input.LA(1)
                        if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 4026531840) != 0)):
                            self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 212
                        self.expr(18)
                        pass

                    elif la_ == 5:
                        localctx = OpenSCADParser.EqualityExprContext(self, OpenSCADParser.ExprContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 213
                        if not self.precpred(self._ctx, 16):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 16)")
                        self.state = 214
                        _la = self._input.LA(1)
                        if not(_la==32 or _la==33):
                            self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 215
                        self.expr(17)
                        pass

                    elif la_ == 6:
                        localctx = OpenSCADParser.LogicalAndExprContext(self, OpenSCADParser.ExprContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 216
                        if not self.precpred(self._ctx, 15):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 15)")
                        self.state = 217
                        self.match(OpenSCADParser.AND)
                        self.state = 218
                        self.expr(16)
                        pass

                    elif la_ == 7:
                        localctx = OpenSCADParser.LogicalOrExprContext(self, OpenSCADParser.ExprContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 219
                        if not self.precpred(self._ctx, 14):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 14)")
                        self.state = 220
                        self.match(OpenSCADParser.OR)
                        self.state = 221
                        self.expr(15)
                        pass

                    elif la_ == 8:
                        localctx = OpenSCADParser.TernaryExprContext(self, OpenSCADParser.ExprContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 222
                        if not self.precpred(self._ctx, 13):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 13)")
                        self.state = 223
                        self.match(OpenSCADParser.T__17)
                        self.state = 224
                        self.expr(0)
                        self.state = 225
                        self.match(OpenSCADParser.T__18)
                        self.state = 226
                        self.expr(13)
                        pass

                    elif la_ == 9:
                        localctx = OpenSCADParser.IndexExprContext(self, OpenSCADParser.ExprContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 228
                        if not self.precpred(self._ctx, 23):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 23)")
                        self.state = 229
                        self.match(OpenSCADParser.T__7)
                        self.state = 230
                        self.expr(0)
                        self.state = 231
                        self.match(OpenSCADParser.T__8)
                        pass

                    elif la_ == 10:
                        localctx = OpenSCADParser.MemberExprContext(self, OpenSCADParser.ExprContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 233
                        if not self.precpred(self._ctx, 22):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 22)")
                        self.state = 234
                        self.match(OpenSCADParser.T__9)
                        self.state = 235
                        self.match(OpenSCADParser.IDENT)
                        pass

             
                self.state = 240
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,17,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.unrollRecursionContexts(_parentctx)
        return localctx


    class RangeContext(ParserRuleContext):
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
            return OpenSCADParser.RULE_range

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterRange" ):
                listener.enterRange(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitRange" ):
                listener.exitRange(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitRange" ):
                return visitor.visitRange(self)
            else:
                return visitor.visitChildren(self)




    def range_(self):

        localctx = OpenSCADParser.RangeContext(self, self._ctx, self.state)
        self.enterRule(localctx, 36, self.RULE_range)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 241
            self.expr(0)
            self.state = 242
            self.match(OpenSCADParser.T__18)
            self.state = 243
            self.expr(0)
            self.state = 246
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==19:
                self.state = 244
                self.match(OpenSCADParser.T__18)
                self.state = 245
                self.expr(0)


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
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
        self.enterRule(localctx, 38, self.RULE_exprList)
        try:
            self.state = 253
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,19,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 248
                self.expr(0)
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 249
                self.expr(0)
                self.state = 250
                self.match(OpenSCADParser.T__5)
                self.state = 251
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
                return self.precpred(self._ctx, 21)
         

            if predIndex == 1:
                return self.precpred(self._ctx, 19)
         

            if predIndex == 2:
                return self.precpred(self._ctx, 18)
         

            if predIndex == 3:
                return self.precpred(self._ctx, 17)
         

            if predIndex == 4:
                return self.precpred(self._ctx, 16)
         

            if predIndex == 5:
                return self.precpred(self._ctx, 15)
         

            if predIndex == 6:
                return self.precpred(self._ctx, 14)
         

            if predIndex == 7:
                return self.precpred(self._ctx, 13)
         

            if predIndex == 8:
                return self.precpred(self._ctx, 23)
         

            if predIndex == 9:
                return self.precpred(self._ctx, 22)
         




