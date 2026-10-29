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
        4,1,40,281,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,2,6,7,
        6,2,7,7,7,2,8,7,8,2,9,7,9,2,10,7,10,2,11,7,11,2,12,7,12,2,13,7,13,
        2,14,7,14,2,15,7,15,2,16,7,16,2,17,7,17,2,18,7,18,2,19,7,19,2,20,
        7,20,2,21,7,21,2,22,7,22,1,0,5,0,48,8,0,10,0,12,0,51,9,0,1,0,1,0,
        1,1,1,1,1,1,1,1,3,1,59,8,1,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,
        2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,3,2,80,8,2,1,3,1,3,1,3,1,3,
        1,3,1,3,1,3,3,3,89,8,3,1,4,1,4,1,4,3,4,94,8,4,1,5,1,5,3,5,98,8,5,
        1,6,1,6,1,6,3,6,103,8,6,1,6,1,6,1,7,1,7,3,7,109,8,7,1,8,1,8,5,8,
        113,8,8,10,8,12,8,116,9,8,1,8,1,8,1,9,1,9,1,9,1,9,1,9,1,10,1,10,
        1,10,1,10,1,10,3,10,130,8,10,1,11,1,11,1,11,1,11,1,12,1,12,1,12,
        5,12,139,8,12,10,12,12,12,142,9,12,1,13,1,13,3,13,146,8,13,1,14,
        1,14,1,14,1,14,3,14,152,8,14,1,14,1,14,1,14,1,15,1,15,1,15,1,15,
        1,15,1,16,1,16,1,16,3,16,165,8,16,1,16,3,16,168,8,16,1,17,1,17,1,
        17,5,17,173,8,17,10,17,12,17,176,9,17,1,18,1,18,1,18,5,18,181,8,
        18,10,18,12,18,184,9,18,1,19,1,19,1,19,1,19,1,20,1,20,1,20,1,20,
        1,20,1,20,1,20,1,20,1,20,1,20,1,20,1,20,3,20,202,8,20,1,20,1,20,
        1,20,1,20,1,20,1,20,1,20,1,20,1,20,1,20,1,20,1,20,1,20,1,20,1,20,
        1,20,1,20,1,20,1,20,1,20,1,20,3,20,225,8,20,1,20,1,20,1,20,1,20,
        1,20,1,20,1,20,1,20,1,20,1,20,1,20,1,20,1,20,1,20,1,20,1,20,1,20,
        1,20,1,20,1,20,1,20,1,20,1,20,1,20,1,20,1,20,1,20,1,20,1,20,1,20,
        1,20,1,20,1,20,1,20,1,20,5,20,262,8,20,10,20,12,20,265,9,20,1,21,
        1,21,1,21,1,21,1,21,3,21,272,8,21,1,22,1,22,1,22,1,22,1,22,3,22,
        279,8,22,1,22,0,1,40,23,0,2,4,6,8,10,12,14,16,18,20,22,24,26,28,
        30,32,34,36,38,40,42,44,0,5,1,0,12,14,1,0,15,17,1,0,12,13,1,0,30,
        33,1,0,34,35,307,0,49,1,0,0,0,2,58,1,0,0,0,4,79,1,0,0,0,6,81,1,0,
        0,0,8,93,1,0,0,0,10,97,1,0,0,0,12,99,1,0,0,0,14,108,1,0,0,0,16,110,
        1,0,0,0,18,119,1,0,0,0,20,129,1,0,0,0,22,131,1,0,0,0,24,135,1,0,
        0,0,26,145,1,0,0,0,28,147,1,0,0,0,30,156,1,0,0,0,32,167,1,0,0,0,
        34,169,1,0,0,0,36,177,1,0,0,0,38,185,1,0,0,0,40,224,1,0,0,0,42,266,
        1,0,0,0,44,278,1,0,0,0,46,48,3,2,1,0,47,46,1,0,0,0,48,51,1,0,0,0,
        49,47,1,0,0,0,49,50,1,0,0,0,50,52,1,0,0,0,51,49,1,0,0,0,52,53,5,
        0,0,1,53,1,1,0,0,0,54,59,3,4,2,0,55,59,3,28,14,0,56,59,3,30,15,0,
        57,59,3,16,8,0,58,54,1,0,0,0,58,55,1,0,0,0,58,56,1,0,0,0,58,57,1,
        0,0,0,59,3,1,0,0,0,60,61,3,12,6,0,61,62,3,4,2,0,62,80,1,0,0,0,63,
        64,3,18,9,0,64,65,3,4,2,0,65,80,1,0,0,0,66,80,3,6,3,0,67,68,3,12,
        6,0,68,69,3,16,8,0,69,80,1,0,0,0,70,71,3,18,9,0,71,72,3,16,8,0,72,
        80,1,0,0,0,73,74,3,12,6,0,74,75,5,1,0,0,75,80,1,0,0,0,76,77,3,18,
        9,0,77,78,5,1,0,0,78,80,1,0,0,0,79,60,1,0,0,0,79,63,1,0,0,0,79,66,
        1,0,0,0,79,67,1,0,0,0,79,70,1,0,0,0,79,73,1,0,0,0,79,76,1,0,0,0,
        80,5,1,0,0,0,81,82,5,22,0,0,82,83,5,2,0,0,83,84,3,40,20,0,84,85,
        5,3,0,0,85,88,3,8,4,0,86,87,5,23,0,0,87,89,3,10,5,0,88,86,1,0,0,
        0,88,89,1,0,0,0,89,7,1,0,0,0,90,94,3,16,8,0,91,94,3,4,2,0,92,94,
        5,1,0,0,93,90,1,0,0,0,93,91,1,0,0,0,93,92,1,0,0,0,94,9,1,0,0,0,95,
        98,3,6,3,0,96,98,3,8,4,0,97,95,1,0,0,0,97,96,1,0,0,0,98,11,1,0,0,
        0,99,100,5,27,0,0,100,102,5,2,0,0,101,103,3,32,16,0,102,101,1,0,
        0,0,102,103,1,0,0,0,103,104,1,0,0,0,104,105,5,3,0,0,105,13,1,0,0,
        0,106,109,3,16,8,0,107,109,3,4,2,0,108,106,1,0,0,0,108,107,1,0,0,
        0,109,15,1,0,0,0,110,114,5,4,0,0,111,113,3,2,1,0,112,111,1,0,0,0,
        113,116,1,0,0,0,114,112,1,0,0,0,114,115,1,0,0,0,115,117,1,0,0,0,
        116,114,1,0,0,0,117,118,5,5,0,0,118,17,1,0,0,0,119,120,5,21,0,0,
        120,121,5,2,0,0,121,122,3,20,10,0,122,123,5,3,0,0,123,19,1,0,0,0,
        124,130,3,22,11,0,125,126,3,22,11,0,126,127,5,6,0,0,127,128,3,20,
        10,0,128,130,1,0,0,0,129,124,1,0,0,0,129,125,1,0,0,0,130,21,1,0,
        0,0,131,132,5,27,0,0,132,133,5,20,0,0,133,134,3,40,20,0,134,23,1,
        0,0,0,135,140,3,26,13,0,136,137,5,6,0,0,137,139,3,26,13,0,138,136,
        1,0,0,0,139,142,1,0,0,0,140,138,1,0,0,0,140,141,1,0,0,0,141,25,1,
        0,0,0,142,140,1,0,0,0,143,146,5,27,0,0,144,146,3,22,11,0,145,143,
        1,0,0,0,145,144,1,0,0,0,146,27,1,0,0,0,147,148,5,7,0,0,148,149,5,
        27,0,0,149,151,5,2,0,0,150,152,3,24,12,0,151,150,1,0,0,0,151,152,
        1,0,0,0,152,153,1,0,0,0,153,154,5,3,0,0,154,155,3,14,7,0,155,29,
        1,0,0,0,156,157,5,27,0,0,157,158,5,20,0,0,158,159,3,40,20,0,159,
        160,5,1,0,0,160,31,1,0,0,0,161,164,3,34,17,0,162,163,5,6,0,0,163,
        165,3,36,18,0,164,162,1,0,0,0,164,165,1,0,0,0,165,168,1,0,0,0,166,
        168,3,36,18,0,167,161,1,0,0,0,167,166,1,0,0,0,168,33,1,0,0,0,169,
        174,3,40,20,0,170,171,5,6,0,0,171,173,3,40,20,0,172,170,1,0,0,0,
        173,176,1,0,0,0,174,172,1,0,0,0,174,175,1,0,0,0,175,35,1,0,0,0,176,
        174,1,0,0,0,177,182,3,38,19,0,178,179,5,6,0,0,179,181,3,38,19,0,
        180,178,1,0,0,0,181,184,1,0,0,0,182,180,1,0,0,0,182,183,1,0,0,0,
        183,37,1,0,0,0,184,182,1,0,0,0,185,186,5,27,0,0,186,187,5,20,0,0,
        187,188,3,40,20,0,188,39,1,0,0,0,189,190,6,20,-1,0,190,191,7,0,0,
        0,191,225,3,40,20,20,192,225,5,28,0,0,193,225,5,29,0,0,194,225,5,
        24,0,0,195,225,5,25,0,0,196,225,5,26,0,0,197,225,5,27,0,0,198,199,
        5,27,0,0,199,201,5,2,0,0,200,202,3,32,16,0,201,200,1,0,0,0,201,202,
        1,0,0,0,202,203,1,0,0,0,203,225,5,3,0,0,204,205,5,8,0,0,205,206,
        3,44,22,0,206,207,5,9,0,0,207,225,1,0,0,0,208,209,5,8,0,0,209,225,
        5,9,0,0,210,211,5,8,0,0,211,212,3,42,21,0,212,213,5,9,0,0,213,225,
        1,0,0,0,214,215,5,21,0,0,215,216,5,2,0,0,216,217,3,20,10,0,217,218,
        5,3,0,0,218,219,3,40,20,2,219,225,1,0,0,0,220,221,5,2,0,0,221,222,
        3,40,20,0,222,223,5,3,0,0,223,225,1,0,0,0,224,189,1,0,0,0,224,192,
        1,0,0,0,224,193,1,0,0,0,224,194,1,0,0,0,224,195,1,0,0,0,224,196,
        1,0,0,0,224,197,1,0,0,0,224,198,1,0,0,0,224,204,1,0,0,0,224,208,
        1,0,0,0,224,210,1,0,0,0,224,214,1,0,0,0,224,220,1,0,0,0,225,263,
        1,0,0,0,226,227,10,21,0,0,227,228,5,11,0,0,228,262,3,40,20,21,229,
        230,10,19,0,0,230,231,7,1,0,0,231,262,3,40,20,20,232,233,10,18,0,
        0,233,234,7,2,0,0,234,262,3,40,20,19,235,236,10,17,0,0,236,237,7,
        3,0,0,237,262,3,40,20,18,238,239,10,16,0,0,239,240,7,4,0,0,240,262,
        3,40,20,17,241,242,10,15,0,0,242,243,5,36,0,0,243,262,3,40,20,16,
        244,245,10,14,0,0,245,246,5,37,0,0,246,262,3,40,20,15,247,248,10,
        13,0,0,248,249,5,18,0,0,249,250,3,40,20,0,250,251,5,19,0,0,251,252,
        3,40,20,13,252,262,1,0,0,0,253,254,10,23,0,0,254,255,5,8,0,0,255,
        256,3,40,20,0,256,257,5,9,0,0,257,262,1,0,0,0,258,259,10,22,0,0,
        259,260,5,10,0,0,260,262,5,27,0,0,261,226,1,0,0,0,261,229,1,0,0,
        0,261,232,1,0,0,0,261,235,1,0,0,0,261,238,1,0,0,0,261,241,1,0,0,
        0,261,244,1,0,0,0,261,247,1,0,0,0,261,253,1,0,0,0,261,258,1,0,0,
        0,262,265,1,0,0,0,263,261,1,0,0,0,263,264,1,0,0,0,264,41,1,0,0,0,
        265,263,1,0,0,0,266,267,3,40,20,0,267,268,5,19,0,0,268,271,3,40,
        20,0,269,270,5,19,0,0,270,272,3,40,20,0,271,269,1,0,0,0,271,272,
        1,0,0,0,272,43,1,0,0,0,273,279,3,40,20,0,274,275,3,40,20,0,275,276,
        5,6,0,0,276,277,3,44,22,0,277,279,1,0,0,0,278,273,1,0,0,0,278,274,
        1,0,0,0,279,45,1,0,0,0,23,49,58,79,88,93,97,102,108,114,129,140,
        145,151,164,167,174,182,201,224,261,263,271,278
    ]

class OpenSCADParser ( Parser ):

    grammarFileName = "OpenSCAD.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "';'", "'('", "')'", "'{'", "'}'", "','", 
                     "'module'", "'['", "']'", "'.'", "'^'", "'+'", "'-'", 
                     "'!'", "'*'", "'/'", "'%'", "'?'", "':'", "'='", "'let'", 
                     "'if'", "'else'", "'true'", "'false'", "'undef'", "<INVALID>", 
                     "<INVALID>", "<INVALID>", "'<'", "'<='", "'>'", "'>='", 
                     "'=='", "'!='", "'&&'", "'||'" ]

    symbolicNames = [ "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "EQ", "LET", "IF", "ELSE", "TRUE", "FALSE", "UNDEF", 
                      "IDENT", "NUMBER", "STRING", "LT", "LE", "GT", "GE", 
                      "EQEQ", "NE", "AND", "OR", "COMMENT", "BLOCK_CMT", 
                      "WS" ]

    RULE_start = 0
    RULE_statement = 1
    RULE_moduleCallSeq = 2
    RULE_ifStatement = 3
    RULE_ifBody = 4
    RULE_elseBody = 5
    RULE_moduleCall = 6
    RULE_body = 7
    RULE_block = 8
    RULE_letExpr = 9
    RULE_letBindingList = 10
    RULE_letBinding = 11
    RULE_paramList = 12
    RULE_param = 13
    RULE_moduleDefinition = 14
    RULE_assignment = 15
    RULE_argList = 16
    RULE_positionalArgs = 17
    RULE_namedArgs = 18
    RULE_namedArg = 19
    RULE_expr = 20
    RULE_range = 21
    RULE_exprList = 22

    ruleNames =  [ "start", "statement", "moduleCallSeq", "ifStatement", 
                   "ifBody", "elseBody", "moduleCall", "body", "block", 
                   "letExpr", "letBindingList", "letBinding", "paramList", 
                   "param", "moduleDefinition", "assignment", "argList", 
                   "positionalArgs", "namedArgs", "namedArg", "expr", "range", 
                   "exprList" ]

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
    IF=22
    ELSE=23
    TRUE=24
    FALSE=25
    UNDEF=26
    IDENT=27
    NUMBER=28
    STRING=29
    LT=30
    LE=31
    GT=32
    GE=33
    EQEQ=34
    NE=35
    AND=36
    OR=37
    COMMENT=38
    BLOCK_CMT=39
    WS=40

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
            self.state = 49
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 140509328) != 0):
                self.state = 46
                self.statement()
                self.state = 51
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 52
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
            self.state = 58
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,1,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 54
                self.moduleCallSeq()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 55
                self.moduleDefinition()
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 56
                self.assignment()
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 57
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



    class ChainedIfCallContext(ModuleCallSeqContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a OpenSCADParser.ModuleCallSeqContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def ifStatement(self):
            return self.getTypedRuleContext(OpenSCADParser.IfStatementContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterChainedIfCall" ):
                listener.enterChainedIfCall(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitChainedIfCall" ):
                listener.exitChainedIfCall(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitChainedIfCall" ):
                return visitor.visitChainedIfCall(self)
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
            self.state = 79
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,2,self._ctx)
            if la_ == 1:
                localctx = OpenSCADParser.ChainedModuleCallContext(self, localctx)
                self.enterOuterAlt(localctx, 1)
                self.state = 60
                self.moduleCall()
                self.state = 61
                self.moduleCallSeq()
                pass

            elif la_ == 2:
                localctx = OpenSCADParser.ChainedLetCallContext(self, localctx)
                self.enterOuterAlt(localctx, 2)
                self.state = 63
                self.letExpr()
                self.state = 64
                self.moduleCallSeq()
                pass

            elif la_ == 3:
                localctx = OpenSCADParser.ChainedIfCallContext(self, localctx)
                self.enterOuterAlt(localctx, 3)
                self.state = 66
                self.ifStatement()
                pass

            elif la_ == 4:
                localctx = OpenSCADParser.ModuleCallWithBlockContext(self, localctx)
                self.enterOuterAlt(localctx, 4)
                self.state = 67
                self.moduleCall()
                self.state = 68
                self.block()
                pass

            elif la_ == 5:
                localctx = OpenSCADParser.LetWithBlockContext(self, localctx)
                self.enterOuterAlt(localctx, 5)
                self.state = 70
                self.letExpr()
                self.state = 71
                self.block()
                pass

            elif la_ == 6:
                localctx = OpenSCADParser.TerminalModuleCallContext(self, localctx)
                self.enterOuterAlt(localctx, 6)
                self.state = 73
                self.moduleCall()
                self.state = 74
                self.match(OpenSCADParser.T__0)
                pass

            elif la_ == 7:
                localctx = OpenSCADParser.TerminalLetContext(self, localctx)
                self.enterOuterAlt(localctx, 7)
                self.state = 76
                self.letExpr()
                self.state = 77
                self.match(OpenSCADParser.T__0)
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class IfStatementContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def IF(self):
            return self.getToken(OpenSCADParser.IF, 0)

        def expr(self):
            return self.getTypedRuleContext(OpenSCADParser.ExprContext,0)


        def ifBody(self):
            return self.getTypedRuleContext(OpenSCADParser.IfBodyContext,0)


        def ELSE(self):
            return self.getToken(OpenSCADParser.ELSE, 0)

        def elseBody(self):
            return self.getTypedRuleContext(OpenSCADParser.ElseBodyContext,0)


        def getRuleIndex(self):
            return OpenSCADParser.RULE_ifStatement

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterIfStatement" ):
                listener.enterIfStatement(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitIfStatement" ):
                listener.exitIfStatement(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitIfStatement" ):
                return visitor.visitIfStatement(self)
            else:
                return visitor.visitChildren(self)




    def ifStatement(self):

        localctx = OpenSCADParser.IfStatementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_ifStatement)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 81
            self.match(OpenSCADParser.IF)
            self.state = 82
            self.match(OpenSCADParser.T__1)
            self.state = 83
            self.expr(0)
            self.state = 84
            self.match(OpenSCADParser.T__2)
            self.state = 85
            self.ifBody()
            self.state = 88
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,3,self._ctx)
            if la_ == 1:
                self.state = 86
                self.match(OpenSCADParser.ELSE)
                self.state = 87
                self.elseBody()


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class IfBodyContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def block(self):
            return self.getTypedRuleContext(OpenSCADParser.BlockContext,0)


        def moduleCallSeq(self):
            return self.getTypedRuleContext(OpenSCADParser.ModuleCallSeqContext,0)


        def getRuleIndex(self):
            return OpenSCADParser.RULE_ifBody

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterIfBody" ):
                listener.enterIfBody(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitIfBody" ):
                listener.exitIfBody(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitIfBody" ):
                return visitor.visitIfBody(self)
            else:
                return visitor.visitChildren(self)




    def ifBody(self):

        localctx = OpenSCADParser.IfBodyContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_ifBody)
        try:
            self.state = 93
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [4]:
                self.enterOuterAlt(localctx, 1)
                self.state = 90
                self.block()
                pass
            elif token in [21, 22, 27]:
                self.enterOuterAlt(localctx, 2)
                self.state = 91
                self.moduleCallSeq()
                pass
            elif token in [1]:
                self.enterOuterAlt(localctx, 3)
                self.state = 92
                self.match(OpenSCADParser.T__0)
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


    class ElseBodyContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ifStatement(self):
            return self.getTypedRuleContext(OpenSCADParser.IfStatementContext,0)


        def ifBody(self):
            return self.getTypedRuleContext(OpenSCADParser.IfBodyContext,0)


        def getRuleIndex(self):
            return OpenSCADParser.RULE_elseBody

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterElseBody" ):
                listener.enterElseBody(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitElseBody" ):
                listener.exitElseBody(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitElseBody" ):
                return visitor.visitElseBody(self)
            else:
                return visitor.visitChildren(self)




    def elseBody(self):

        localctx = OpenSCADParser.ElseBodyContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_elseBody)
        try:
            self.state = 97
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,5,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 95
                self.ifStatement()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 96
                self.ifBody()
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
        self.enterRule(localctx, 12, self.RULE_moduleCall)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 99
            self.match(OpenSCADParser.IDENT)
            self.state = 100
            self.match(OpenSCADParser.T__1)
            self.state = 102
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if (((_la) & ~0x3f) == 0 and ((1 << _la) & 1059090692) != 0):
                self.state = 101
                self.argList()


            self.state = 104
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
        self.enterRule(localctx, 14, self.RULE_body)
        try:
            self.state = 108
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [4]:
                self.enterOuterAlt(localctx, 1)
                self.state = 106
                self.block()
                pass
            elif token in [21, 22, 27]:
                self.enterOuterAlt(localctx, 2)
                self.state = 107
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
        self.enterRule(localctx, 16, self.RULE_block)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 110
            self.match(OpenSCADParser.T__3)
            self.state = 114
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 140509328) != 0):
                self.state = 111
                self.statement()
                self.state = 116
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 117
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
        self.enterRule(localctx, 18, self.RULE_letExpr)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 119
            self.match(OpenSCADParser.LET)
            self.state = 120
            self.match(OpenSCADParser.T__1)
            self.state = 121
            self.letBindingList()
            self.state = 122
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
        self.enterRule(localctx, 20, self.RULE_letBindingList)
        try:
            self.state = 129
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,9,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 124
                self.letBinding()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 125
                self.letBinding()
                self.state = 126
                self.match(OpenSCADParser.T__5)
                self.state = 127
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
        self.enterRule(localctx, 22, self.RULE_letBinding)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 131
            self.match(OpenSCADParser.IDENT)
            self.state = 132
            self.match(OpenSCADParser.EQ)
            self.state = 133
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
        self.enterRule(localctx, 24, self.RULE_paramList)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 135
            self.param()
            self.state = 140
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==6:
                self.state = 136
                self.match(OpenSCADParser.T__5)
                self.state = 137
                self.param()
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
        self.enterRule(localctx, 26, self.RULE_param)
        try:
            self.state = 145
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,11,self._ctx)
            if la_ == 1:
                localctx = OpenSCADParser.ParamNoDefaultContext(self, localctx)
                self.enterOuterAlt(localctx, 1)
                self.state = 143
                self.match(OpenSCADParser.IDENT)
                pass

            elif la_ == 2:
                localctx = OpenSCADParser.ParamWithDefaultContext(self, localctx)
                self.enterOuterAlt(localctx, 2)
                self.state = 144
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
        self.enterRule(localctx, 28, self.RULE_moduleDefinition)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 147
            self.match(OpenSCADParser.T__6)
            self.state = 148
            self.match(OpenSCADParser.IDENT)
            self.state = 149
            self.match(OpenSCADParser.T__1)
            self.state = 151
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==27:
                self.state = 150
                self.paramList()


            self.state = 153
            self.match(OpenSCADParser.T__2)
            self.state = 154
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
        self.enterRule(localctx, 30, self.RULE_assignment)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 156
            self.match(OpenSCADParser.IDENT)
            self.state = 157
            self.match(OpenSCADParser.EQ)
            self.state = 158
            self.expr(0)
            self.state = 159
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
        self.enterRule(localctx, 32, self.RULE_argList)
        self._la = 0 # Token type
        try:
            self.state = 167
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,14,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 161
                self.positionalArgs()
                self.state = 164
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==6:
                    self.state = 162
                    self.match(OpenSCADParser.T__5)
                    self.state = 163
                    self.namedArgs()


                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 166
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
        self.enterRule(localctx, 34, self.RULE_positionalArgs)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 169
            self.expr(0)
            self.state = 174
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,15,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 170
                    self.match(OpenSCADParser.T__5)
                    self.state = 171
                    self.expr(0) 
                self.state = 176
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,15,self._ctx)

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
        self.enterRule(localctx, 36, self.RULE_namedArgs)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 177
            self.namedArg()
            self.state = 182
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==6:
                self.state = 178
                self.match(OpenSCADParser.T__5)
                self.state = 179
                self.namedArg()
                self.state = 184
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
        self.enterRule(localctx, 38, self.RULE_namedArg)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 185
            self.match(OpenSCADParser.IDENT)
            self.state = 186
            self.match(OpenSCADParser.EQ)
            self.state = 187
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
        _startState = 40
        self.enterRecursionRule(localctx, 40, self.RULE_expr, _p)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 224
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,18,self._ctx)
            if la_ == 1:
                localctx = OpenSCADParser.UnaryExprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx

                self.state = 190
                _la = self._input.LA(1)
                if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 28672) != 0)):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 191
                self.expr(20)
                pass

            elif la_ == 2:
                localctx = OpenSCADParser.NumberExprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 192
                self.match(OpenSCADParser.NUMBER)
                pass

            elif la_ == 3:
                localctx = OpenSCADParser.StringExprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 193
                self.match(OpenSCADParser.STRING)
                pass

            elif la_ == 4:
                localctx = OpenSCADParser.TrueExprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 194
                self.match(OpenSCADParser.TRUE)
                pass

            elif la_ == 5:
                localctx = OpenSCADParser.FalseExprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 195
                self.match(OpenSCADParser.FALSE)
                pass

            elif la_ == 6:
                localctx = OpenSCADParser.UndefExprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 196
                self.match(OpenSCADParser.UNDEF)
                pass

            elif la_ == 7:
                localctx = OpenSCADParser.IdentExprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 197
                self.match(OpenSCADParser.IDENT)
                pass

            elif la_ == 8:
                localctx = OpenSCADParser.FunctionCallExprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 198
                self.match(OpenSCADParser.IDENT)
                self.state = 199
                self.match(OpenSCADParser.T__1)
                self.state = 201
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if (((_la) & ~0x3f) == 0 and ((1 << _la) & 1059090692) != 0):
                    self.state = 200
                    self.argList()


                self.state = 203
                self.match(OpenSCADParser.T__2)
                pass

            elif la_ == 9:
                localctx = OpenSCADParser.VectorExprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 204
                self.match(OpenSCADParser.T__7)
                self.state = 205
                self.exprList()
                self.state = 206
                self.match(OpenSCADParser.T__8)
                pass

            elif la_ == 10:
                localctx = OpenSCADParser.EmptyVectorExprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 208
                self.match(OpenSCADParser.T__7)
                self.state = 209
                self.match(OpenSCADParser.T__8)
                pass

            elif la_ == 11:
                localctx = OpenSCADParser.RangeExprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 210
                self.match(OpenSCADParser.T__7)
                self.state = 211
                self.range_()
                self.state = 212
                self.match(OpenSCADParser.T__8)
                pass

            elif la_ == 12:
                localctx = OpenSCADParser.LetExpressionContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 214
                self.match(OpenSCADParser.LET)
                self.state = 215
                self.match(OpenSCADParser.T__1)
                self.state = 216
                self.letBindingList()
                self.state = 217
                self.match(OpenSCADParser.T__2)
                self.state = 218
                self.expr(2)
                pass

            elif la_ == 13:
                localctx = OpenSCADParser.ParenExprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 220
                self.match(OpenSCADParser.T__1)
                self.state = 221
                self.expr(0)
                self.state = 222
                self.match(OpenSCADParser.T__2)
                pass


            self._ctx.stop = self._input.LT(-1)
            self.state = 263
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,20,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    self.state = 261
                    self._errHandler.sync(self)
                    la_ = self._interp.adaptivePredict(self._input,19,self._ctx)
                    if la_ == 1:
                        localctx = OpenSCADParser.ExponentExprContext(self, OpenSCADParser.ExprContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 226
                        if not self.precpred(self._ctx, 21):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 21)")
                        self.state = 227
                        self.match(OpenSCADParser.T__10)
                        self.state = 228
                        self.expr(21)
                        pass

                    elif la_ == 2:
                        localctx = OpenSCADParser.MultiplicativeExprContext(self, OpenSCADParser.ExprContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 229
                        if not self.precpred(self._ctx, 19):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 19)")
                        self.state = 230
                        _la = self._input.LA(1)
                        if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 229376) != 0)):
                            self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 231
                        self.expr(20)
                        pass

                    elif la_ == 3:
                        localctx = OpenSCADParser.AdditiveExprContext(self, OpenSCADParser.ExprContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 232
                        if not self.precpred(self._ctx, 18):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 18)")
                        self.state = 233
                        _la = self._input.LA(1)
                        if not(_la==12 or _la==13):
                            self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 234
                        self.expr(19)
                        pass

                    elif la_ == 4:
                        localctx = OpenSCADParser.RelationalExprContext(self, OpenSCADParser.ExprContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 235
                        if not self.precpred(self._ctx, 17):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 17)")
                        self.state = 236
                        _la = self._input.LA(1)
                        if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 16106127360) != 0)):
                            self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 237
                        self.expr(18)
                        pass

                    elif la_ == 5:
                        localctx = OpenSCADParser.EqualityExprContext(self, OpenSCADParser.ExprContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 238
                        if not self.precpred(self._ctx, 16):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 16)")
                        self.state = 239
                        _la = self._input.LA(1)
                        if not(_la==34 or _la==35):
                            self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 240
                        self.expr(17)
                        pass

                    elif la_ == 6:
                        localctx = OpenSCADParser.LogicalAndExprContext(self, OpenSCADParser.ExprContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 241
                        if not self.precpred(self._ctx, 15):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 15)")
                        self.state = 242
                        self.match(OpenSCADParser.AND)
                        self.state = 243
                        self.expr(16)
                        pass

                    elif la_ == 7:
                        localctx = OpenSCADParser.LogicalOrExprContext(self, OpenSCADParser.ExprContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 244
                        if not self.precpred(self._ctx, 14):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 14)")
                        self.state = 245
                        self.match(OpenSCADParser.OR)
                        self.state = 246
                        self.expr(15)
                        pass

                    elif la_ == 8:
                        localctx = OpenSCADParser.TernaryExprContext(self, OpenSCADParser.ExprContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 247
                        if not self.precpred(self._ctx, 13):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 13)")
                        self.state = 248
                        self.match(OpenSCADParser.T__17)
                        self.state = 249
                        self.expr(0)
                        self.state = 250
                        self.match(OpenSCADParser.T__18)
                        self.state = 251
                        self.expr(13)
                        pass

                    elif la_ == 9:
                        localctx = OpenSCADParser.IndexExprContext(self, OpenSCADParser.ExprContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 253
                        if not self.precpred(self._ctx, 23):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 23)")
                        self.state = 254
                        self.match(OpenSCADParser.T__7)
                        self.state = 255
                        self.expr(0)
                        self.state = 256
                        self.match(OpenSCADParser.T__8)
                        pass

                    elif la_ == 10:
                        localctx = OpenSCADParser.MemberExprContext(self, OpenSCADParser.ExprContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 258
                        if not self.precpred(self._ctx, 22):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 22)")
                        self.state = 259
                        self.match(OpenSCADParser.T__9)
                        self.state = 260
                        self.match(OpenSCADParser.IDENT)
                        pass

             
                self.state = 265
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,20,self._ctx)

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
        self.enterRule(localctx, 42, self.RULE_range)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 266
            self.expr(0)
            self.state = 267
            self.match(OpenSCADParser.T__18)
            self.state = 268
            self.expr(0)
            self.state = 271
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==19:
                self.state = 269
                self.match(OpenSCADParser.T__18)
                self.state = 270
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
        self.enterRule(localctx, 44, self.RULE_exprList)
        try:
            self.state = 278
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,22,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 273
                self.expr(0)
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 274
                self.expr(0)
                self.state = 275
                self.match(OpenSCADParser.T__5)
                self.state = 276
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
        self._predicates[20] = self.expr_sempred
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
         




