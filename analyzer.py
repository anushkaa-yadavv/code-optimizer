import ast
from radon.complexity import cc_visit

class CodeAnalyzer:
    def __init__(self, code):
        self.code = code
        self.tree = ast.parse(code)
        self.issues = []

        self.long_functions = 0
        self.deep_nesting = 0
        self.loop_count = 0
        self.complexity_score = 0

    def analyze(self):
        self.check_long_functions()
        self.check_nested_depth()
        self.check_loops()
        self.check_complexity()

        risk_score = self.calculate_risk_score()

        return {
            "risk_score": risk_score,
            "issues": self.issues
        }

    def check_long_functions(self):
        for node in ast.walk(self.tree):
            if isinstance(node, ast.FunctionDef):
                if len(node.body) > 20:
                    self.long_functions += 1
                    self.issues.append(f"Long function: {node.name}")

    def check_nested_depth(self):
        def depth(node, level=0):
            if not hasattr(node, 'body'):
                return level
            return max([depth(child, level+1) for child in node.body] + [level])

        self.deep_nesting = depth(self.tree)

        if self.deep_nesting > 3:
            self.issues.append(f"Deep nesting: {self.deep_nesting}")

    def check_loops(self):
        self.loop_count = sum(isinstance(n, (ast.For, ast.While)) for n in ast.walk(self.tree))

        if self.loop_count > 3:
            self.issues.append(f"Too many loops: {self.loop_count}")

    def check_complexity(self):
        try:
            results = cc_visit(self.code)
            if results:
                max_c = max(r.complexity for r in results)
                self.complexity_score = max_c
                if max_c > 8:
                    self.issues.append(f"High complexity: {max_c}")
        except:
            pass

    def calculate_risk_score(self):
        score = 0

        score += self.long_functions * 10

        if self.deep_nesting > 2:
            score += (self.deep_nesting - 2) * 5

        if self.loop_count > 2:
            score += (self.loop_count - 2) * 5

        if self.complexity_score > 5:
            score += (self.complexity_score - 5) * 3

        return min(score, 100)