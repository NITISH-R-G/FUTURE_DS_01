import os
import json
import networkx as nx
from networkx.readwrite import json_graph
import fnmatch


def build_knowledge_graph():
    print("Building knowledge graph...")
    G = nx.DiGraph()

    ignore_patterns = [
        ".git*",
        "__pycache__",
        "node_modules",
        "venv",
        ".venv",
        "env",
        "build",
        "dist",
        "docs/diagrams",
        "*.json",
        "*.md",
    ]

    for root, dirs, files in os.walk("."):
        dirs[:] = [
            d for d in dirs if not any(fnmatch.fnmatch(d, p) for p in ignore_patterns)
        ]

        for file in files:
            if any(fnmatch.fnmatch(file, p) for p in ignore_patterns):
                continue

            filepath = os.path.relpath(os.path.join(root, file), ".")
            G.add_node(filepath, type="file")

            # Very basic dependency extraction for Python (import statements)
            if filepath.endswith(".py"):
                try:
                    with open(filepath, "r") as f:
                        for line in f:
                            if line.startswith("import ") or line.startswith("from "):
                                parts = line.split()
                                if len(parts) > 1:
                                    module = parts[1].split(".")[0]
                                    G.add_node(module, type="module")
                                    G.add_edge(filepath, module, relation="imports")
                except Exception as e:
                    print(f"Error reading {filepath}: {e}")

    data = json_graph.node_link_data(G)
    with open("knowledge_graph.json", "w") as f:
        json.dump(data, f, indent=2)

    print("Knowledge graph built. Saved to knowledge_graph.json")


if __name__ == "__main__":
    build_knowledge_graph()
