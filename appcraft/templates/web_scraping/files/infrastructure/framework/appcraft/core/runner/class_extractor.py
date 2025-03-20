import ast
from typing import Any


class RunnerClassExtractor:
    @classmethod
    def _get_base_classes(
        cls, class_name: str, class_nodes: dict[Any, Any]
    ) -> list[str]:
        """Recursively fetches base classes for a given class."""
        if class_name not in class_nodes:
            return []

        base_classes: list[str] = []
        class_node = class_nodes[class_name]

        for base in class_node.bases:
            if isinstance(base, ast.Name):
                base_classes.append(base.id)
                base_classes += cls._get_base_classes(base.id, class_nodes)
            elif isinstance(base, ast.Attribute):
                base_classes.append(base.attr)

        return base_classes

    @classmethod
    def get_class_hierarchy(cls, node: ast.Module) -> dict[Any, Any]:
        """Maps all classes in the AST to their base classes."""
        class_nodes = {
            class_node.name: class_node
            for class_node in ast.walk(node)
            if isinstance(class_node, ast.ClassDef)
        }

        hierarchy: dict[Any, Any] = {}

        for class_name, _ in class_nodes.items():
            hierarchy[class_name] = cls._get_base_classes(
                class_name, class_nodes
            )

        return hierarchy

    @classmethod
    def extract_subscript_base(
        cls, node: ast.Subscript, class_nodes: dict[Any, Any]
    ) -> list[str]:
        """\
Tries to fetch base classes if the subscript points to a known class."""
        if isinstance(node.value, ast.Name):
            class_name = node.value.id
            return cls._get_base_classes(class_name, class_nodes)
        return []


def analyze_code(code: str):
    tree = ast.parse(code)
    hierarchy = RunnerClassExtractor.get_class_hierarchy(tree)

    for node in ast.walk(tree):
        if isinstance(node, ast.Subscript):
            bases = RunnerClassExtractor.extract_subscript_base(
                node, hierarchy
            )
            print(f"Subscript found in: {ast.dump(node)}")
            print(f"Detected base classes: {bases}")
