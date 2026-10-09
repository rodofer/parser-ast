import ast

NODOS_PERMITIDOS = (
    ast.Module,
    ast.Assign,
    ast.Name,
    ast.Store,
    ast.Constant,
    ast.While,
    ast.Compare,
    ast.Load,
    ast.Lt,
    ast.AugAssign,
    ast.Add
)
