from manifold_learn.ast.module_definition import ModuleDefinition
from manifold_learn.ast.tree_node import TreeNode


class TreeEvaluator:

    def __init__(self, builtin_modules: list[ModuleDefinition]):
        self._builtin_modules = builtin_modules

    def make_root_node(self) -> TreeNode:
        return TreeNode(
            module="root",
            positional_args=[],
            named_args={},
            _modules={module.name: module for module in self._builtin_modules}
        )

    def eval_tree(self, node: TreeNode):
        root = self.make_root_node()
        root.add_child(node)
        return self._eval_node(node)

    def _eval_node(self, node: TreeNode):
        module_name = node.module
        print(module_name)
        module_def = node.get_module(module_name)
        bound_parameters = module_def.bind_parameters(node.positional_args, node.named_args)
        scope = node.make_parameter_scope(bound_parameters)
        args = {
            name: scope.eval_variable(name)
            for name
            in module_def.parameters.keys()
        }
        children = [self._eval_node(child) for child in node.children]
        return module_def.eval(args, children)
