import json
import os


def generate_mermaid_diagram():
    print("Generating Mermaid diagrams...")
    os.makedirs("docs/diagrams", exist_ok=True)

    try:
        with open("repo_state.json", "r") as f:
            state = json.load(f)
    except FileNotFoundError:
        print("repo_state.json not found. Run analyze_repository.py first.")
        return

    # 1. Architecture Diagram (Basic mapping of detected tech)
    arch_mermaid = "graph TD;\n"
    arch_mermaid += "    Repo[Repository] --> Frameworks;\n"
    arch_mermaid += "    Repo --> Databases;\n"
    for fw in state.get("frameworks", []):
        arch_mermaid += f"    Frameworks --> {fw.replace(' ', '_')};\n"
    for db in state.get("databases", []):
        arch_mermaid += f"    Databases --> {db.replace(' ', '_').replace('(', '').replace(')', '')};\n"

    with open("docs/diagrams/architecture.mmd", "w") as f:
        f.write(arch_mermaid)

    # 2. Dependency Graph from knowledge graph
    try:
        with open("knowledge_graph.json", "r") as f:
            kg = json.load(f)

        dep_mermaid = "graph LR;\n"
        # Extract edges
        for link in kg.get("links", []):
            source = (
                link.get("source", "")
                .replace("-", "_")
                .replace(".", "_")
                .replace("/", "_")
            )
            target = (
                link.get("target", "")
                .replace("-", "_")
                .replace(".", "_")
                .replace("/", "_")
            )
            if source and target:
                dep_mermaid += f"    {source} --> {target};\n"

        with open("docs/diagrams/dependencies.mmd", "w") as f:
            f.write(dep_mermaid)

        # 3. Data flow and interactive diagrams
        data_flow_mermaid = "graph TD;\n"
        data_flow_mermaid += "  subgraph CI_CD\n    CI[GitHub Actions] --> Scripts[Automation Scripts];\n  end\n"
        data_flow_mermaid += "  subgraph Output\n    Scripts --> Readme[README.md];\n    Scripts --> Docs[docs/];\n  end\n"
        with open("docs/diagrams/data_flow.mmd", "w") as f:
            f.write(data_flow_mermaid)

        interactive_svg = "<html><body><h1>Interactive Architecture Map</h1><p>Placeholder for deep-linked interactive SVG showing service maps. In a production environment this would parse repo_state.json and output d3.js or similar visual graphs with file path links.</p></body></html>"
        with open("docs/diagrams/interactive_map.html", "w") as f:
            f.write(interactive_svg)

    except FileNotFoundError:
        print("knowledge_graph.json not found. Skipping dependency diagram.")

    print("Diagrams generated in docs/diagrams/")


if __name__ == "__main__":
    generate_mermaid_diagram()
