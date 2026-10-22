grammar OpenSCAD;

start       : statement* EOF ;

// statements
statement   : moduleCallSeq
            | moduleDefinition
            | assignment
            ;

moduleCallSeq     : moduleCall moduleCallSeq       # ChainedModuleCall
                  | letExpr moduleCallSeq          # ChainedLetCall
                  | moduleCall ';'                 # TerminalModuleCall
                  | block                          # TerminalBlock
                  ;

moduleCall        : IDENT '(' argList? ')' ;

block           : '{' statement* '}' ;

letExpr : LET '(' letBindingList ')' ;
letBindingList : letBinding
               | letBinding ',' letBindingList
               ;
letBinding : IDENT '=' expr ;

// Module definition, e.g. `module SomeName(arg1, arg2=10) { ... }`
moduleDefinition : 'module' IDENT '(' argList? ')' moduleCallSeq ;

// Variable assignment
assignment  : IDENT '=' expr ';' ;

// Arguments
argList     : arg
            | arg ',' argList
            ;

arg         : IDENT '=' expr           # NamedArg
            | expr                     # PositionalArg
            ;

expr        : NUMBER                    # NumberExpr
            | STRING                    # StringExpr
            | IDENT                     # IdentExpr
            | '[' exprList? ']'         # ArrayExpr
            | expr BINARY_OP expr       # BinaryExpr
            | '(' expr ')'              # ParenExpr
            ;

// Comma-separated expression list inside an array literal, e.g. [12, var2+2, -3.2].
exprList    : expr
            | expr ',' exprList
            ;

// Lexer rules (UPPERCASE)
BINARY_OP   : '+' | '-' | '*' | '/' ;
// Must precede IDENT: for input `let` both rules match with equal length, and
// ANTLR breaks ties by rule order, so LET wins. Longer words like `letter`
// still lex as IDENT (longest-match takes precedence).
LET         : 'let' ;
IDENT       : [a-zA-Z_][a-zA-Z0-9_]* ;
NUMBER      : '-'? [0-9]+ ('.' [0-9]+)? ;
STRING      : '"' (~["\r\n])* '"' ;

// Skipped:
COMMENT     : '//' ~[\r\n]* -> skip ;
BLOCK_CMT   : '/*' .*? '*/' -> skip ;
WS          : [ \t\r\n]+ -> skip ;


// Existing issues
// - NUMBER : '-'? [0-9]+ ... breaks binary minus after whitespace-free operands. x = 1 - 2; lexes fine (- followed by space can't match NUMBER), but x = 1 -2; lexes as NUMBER(1) NUMBER(-2) and fails to parse. The usual fix is to drop '-' from NUMBER and add a '-' expr unary alternative under # UnaryExpr; then -3.2 in arrays still works.
// - All four operators sit in one expr BINARY_OP expr alternative, so * and / have the same precedence as + and - and everything is left-associative — 1 + 2 * 3 evaluates the same shape as (1 + 2) * 3. Fix by splitting into precedence tiers (expr ('*'|'/') expr level above expr ('+'|'-') expr) rather than a single BINARY_OP.
// - '[' exprList? ']' and exprList/argList are right-recursive, so recursion depth grows with list length. Harmless at realistic sizes; a (',' expr)* loop shape avoids it if you ever feed generated input.
// - STRING has no escape handling — "a\"b" can't be written.
