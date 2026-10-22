Every AST tree node represents a "module call".
Every module has:
 - module name - this the name of the module to be called for this node
 - positional arguments - a list of expressions that would be passed to the module as positional arguments
 - named arguments - a list of named expressions that would be passed to the module as named arguments
 - children (other module calls). This is a list of other module calls that would be called before the current module,
   and their results would be passed to the current module as "children". Module may accept none, one or many children.
Every tree node also have a "context":
 - all modules defined in the current scope
 - all variables defined in the current scope. 
 - Scope always includes parent scope and every AST tree has one parent (except the root node)
Some modules (blocks and let expression) may extend the context:
 - Define new modules
 - Define new variables

Class TreeNode represents a node in the AST and have vields for all the above.
