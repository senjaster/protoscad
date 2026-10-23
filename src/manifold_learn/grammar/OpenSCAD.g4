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

expr        : expr ('*' | '/') expr     # MultiplicativeExpr
            | expr ('+' | '-') expr     # AdditiveExpr
            | NUMBER                    # NumberExpr
            | STRING                    # StringExpr
            | IDENT                     # IdentExpr
            | '[' exprList? ']'         # ArrayExpr
            | '(' expr ')'              # ParenExpr
            ;

// Comma-separated expression list inside an array literal, e.g. [12, var2+2, -3.2].
exprList    : expr
            | expr ',' exprList
            ;

// Lexer rules (UPPERCASE)
EQ          : '=' ;
// Must precede IDENT: for input `let` both rules match with equal length, and
// ANTLR breaks ties by rule order, so LET wins. Longer words like `letter`
// still lex as IDENT (longest-match takes precedence).
LET         : 'let' ;
IDENT       : '$'? [a-zA-Z_][a-zA-Z0-9_]* ;
NUMBER      : '-'? [0-9]+ ('.' [0-9]+)? ;
STRING      : '"' (~["\r\n])* '"' ;

// Skipped:
COMMENT     : '//' ~[\r\n]* -> skip ;
BLOCK_CMT   : '/*' .*? '*/' -> skip ;
WS          : [ \t\r\n]+ -> skip ;