import ast


class CodeAnalyzer:
    def __init__(self, code):
        self.code = code

    def analyze(self):
        tree = ast.parse(self.code)

        issues = []
        risk_score = 0

        loop_count = self.count_loops(tree)
        depth = self.max_depth(tree)

        # 🔥 Rules
        if depth > 4:
            issues.append(f"Deep nesting: {depth}")
            risk_score += depth * 2

        if loop_count > 3:
            issues.append(f"Too many loops: {loop_count}")
            risk_score += loop_count * 2

        return {
            "risk_score": risk_score,
            "issues": issues
        }

    def count_loops(self, node):
        count = 0
        for child in ast.walk(node):
            if isinstance(child, (ast.For, ast.While)):
                count += 1
        return count

    def max_depth(self, node, level=0):
        children = list(ast.iter_child_nodes(node))
        if not children:
            return level
        return max(self.max_depth(child, level + 1) for child in children)
