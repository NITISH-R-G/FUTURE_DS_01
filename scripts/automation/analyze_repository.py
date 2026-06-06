import os
import json
import fnmatch
import re


def analyze_repository():
    print("Starting repository analysis...")
    state = {
        "files": [],
        "directories": [],
        "languages": {},
        "frameworks": [],
        "databases": [],
        "env_vars": [],
    }

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
    ]

    for root, dirs, files in os.walk("."):
        # Filter directories
        dirs[:] = [
            d for d in dirs if not any(fnmatch.fnmatch(d, p) for p in ignore_patterns)
        ]

        rel_dir = os.path.relpath(root, ".")
        if rel_dir != ".":
            state["directories"].append(rel_dir)

        for file in files:
            if any(fnmatch.fnmatch(file, p) for p in ignore_patterns):
                continue

            filepath = os.path.relpath(os.path.join(root, file), ".")
            state["files"].append(filepath)

            # Basic language detection by extension
            ext = os.path.splitext(file)[1].lower()
            if ext:
                state["languages"][ext] = state["languages"].get(ext, 0) + 1

            # Check for specific files to detect frameworks/DBs/env
            if file == "package.json":
                try:
                    with open(filepath, "r") as f:
                        data = json.load(f)
                        deps = {
                            **data.get("dependencies", {}),
                            **data.get("devDependencies", {}),
                        }
                        if "react" in deps:
                            state["frameworks"].append("React")
                        if "express" in deps:
                            state["frameworks"].append("Express")
                        if "pg" in deps or "mongoose" in deps:
                            state["databases"].append("Detected via package.json")
                except:
                    pass
            elif file == "requirements.txt":
                try:
                    with open(filepath, "r") as f:
                        content = f.read().lower()
                        if "django" in content:
                            state["frameworks"].append("Django")
                        if "flask" in content:
                            state["frameworks"].append("Flask")
                        if "psycopg2" in content:
                            state["databases"].append("PostgreSQL (psycopg2)")
                except:
                    pass
            elif ".env.example" in file or ".env.sample" in file:
                try:
                    with open(filepath, "r") as f:
                        for line in f:
                            if "=" in line and not line.startswith("#"):
                                var_name = line.split("=")[0].strip()
                                if var_name not in state["env_vars"]:
                                    state["env_vars"].append(var_name)
                except:
                    pass

            # Look for Dockerfile for deployment clues
            elif file == "Dockerfile":
                state["frameworks"].append("Docker")

    # Deduplicate lists
    state["frameworks"] = list(set(state["frameworks"]))
    state["databases"] = list(set(state["databases"]))

    with open("repo_state.json", "w") as f:
        json.dump(state, f, indent=2)

    print("Repository analysis complete. State saved to repo_state.json")


if __name__ == "__main__":
    analyze_repository()
