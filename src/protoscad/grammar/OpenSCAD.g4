grammar OpenSCAD;

start       : statement* EOF ;

// statements
statement   : moduleCallSeq
            | moduleDefinition
            | assignment
            | block
            ;

// A chain of module calls. Each call's body is either the continuation
// (another chained call), an explicit block, or nothing (terminal).
moduleCallSeq     : moduleCall moduleCallSeq       # ChainedModuleCall
                  | letExpr moduleCallSeq          # ChainedLetCall
                  | moduleCall block               # ModuleCallWithBlock
                  | letExpr block                  # LetWithBlock
                  | moduleCall ';'                 # TerminalModuleCall
                  | letExpr ';'                    # TerminalLet
                  ;

moduleCall        : IDENT '(' argList? ')' ;

// A scope: the body of a module definition or module invocation. It is either
// an explicit `{ ... }` block or a chained module-call sequence (the
// brace-less form).
body        : block
            | moduleCallSeq
            ;

// Bare `{ ... }` block. Transparent: the visitor splices its statements into
// the enclosing scope rather than creating a block node.
block       : '{' statement* '}' ;

letExpr : LET '(' letBindingList ')' ;
letBindingList : letBinding
               | letBinding ',' letBindingList
               ;
letBinding : IDENT EQ expr ;

// Module parameter list, e.g. `module Foo(a, b=2) { ... }`.
// Each parameter is either a bare name (no default) or a `letBinding`
// (name with a default value). A bare name is not a valid call argument,
// so this is separate from argList.
paramList   : param (',' param)* ;
param       : IDENT                  # ParamNoDefault
            | letBinding             # ParamWithDefault
            ;

// Module definition, e.g. `module SomeName(arg1, arg2=10) { ... }`
moduleDefinition : 'module' IDENT '(' paramList? ')' body ;

// Variable assignment
assignment  : IDENT EQ expr ';' ;

// Arguments
// Positional arguments must precede named arguments; mixing in reverse order is a syntax error.
// The explicit ',' before namedArgs anchors the boundary, letting ANTLR resolve it without a predicate.
argList     : positionalArgs (',' namedArgs)?
            | namedArgs
            ;

positionalArgs : expr (',' expr)* ;

namedArgs   : namedArg (',' namedArg)* ;

namedArg    : IDENT EQ expr ;

// Expressions. In ANTLR left-recursive rules the FIRST alternative binds
// tightest, so the ladder below is ordered from tightest (indexing) to
// loosest (ternary), matching OpenSCAD: `!a && b`, `-2^2 == -4`,
// `a < b == c < d`, `x ? y : x ? z : w`.
expr
    : expr '[' expr ']'                        # IndexExpr
    | expr '.' IDENT                           # MemberExpr
    | <assoc=right> expr '^' expr              # ExponentExpr
    | ('+' | '-' | '!') expr                   # UnaryExpr
    | expr ('*' | '/' | '%') expr              # MultiplicativeExpr
    | expr ('+' | '-') expr                    # AdditiveExpr
    | expr ('<' | '<=' | '>' | '>=') expr      # RelationalExpr
    | expr ('==' | '!=') expr                  # EqualityExpr
    | expr '&&' expr                           # LogicalAndExpr
    | expr '||' expr                           # LogicalOrExpr
    | <assoc=right> expr '?' expr ':' expr     # TernaryExpr
    | NUMBER                                   # NumberExpr
    | STRING                                   # StringExpr
    | TRUE                                     # TrueExpr
    | FALSE                                    # FalseExpr
    | UNDEF                                    # UndefExpr
    | IDENT                                    # IdentExpr
    | IDENT '(' argList? ')'                   # FunctionCallExpr
    | '[' exprList ']'                         # VectorExpr
    | '[' ']'                                  # EmptyVectorExpr
    | '[' range ']'                            # RangeExpr
    | LET '(' letBindingList ')' expr          # LetExpression
    | '(' expr ')'                             # ParenExpr
    ;

// [start:end] or [start:step:end]; the end is inclusive.
range : expr ':' expr (':' expr)? ;

// Comma-separated expression list inside a vector literal, e.g. [12, var2+2, -3.2].
exprList    : expr
            | expr ',' exprList
            ;

// Lexer rules (UPPERCASE)
EQ          : '=' ;
// Keyword rules must precede IDENT: for a keyword both rules match with
// equal length and ANTLR breaks ties by rule order, so the keyword wins.
// Longer words like `letter` still lex as IDENT (longest-match wins).
LET         : 'let' ;
TRUE        : 'true' ;
FALSE       : 'false' ;
UNDEF       : 'undef' ;
IDENT       : '$'? [a-zA-Z_][a-zA-Z0-9_]* ;
NUMBER      : [0-9]+ ('.' [0-9]+)? ([eE] [+-]? [0-9]+)? ;
// Escape sequences are decoded after lexing (values.unescape_string).
STRING      : '"' ( '\\' . | ~["\\\r\n] )* '"' ;
LT          : '<' ;
LE          : '<=' ;
GT          : '>' ;
GE          : '>=' ;
EQEQ        : '==' ;
NE          : '!=' ;
AND         : '&&' ;
OR          : '||' ;

// Skipped:
COMMENT     : '//' ~[\r\n]* -> skip ;
BLOCK_CMT   : '/*' .*? '*/' -> skip ;
WS          : [ \t\r\n]+ -> skip ;
