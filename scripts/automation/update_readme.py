import json
import os
from datetime import datetime, timezone


def update_readme():
    print("Updating README.md...")

    try:
        with open("repo_state.json", "r") as f:
            state = json.load(f)
    except FileNotFoundError:
        print("repo_state.json not found. Run analyze_repository.py first.")
        return

    readme_content = f"""# Autonomous Repository Analysis

> This repository is self-documenting. The architecture, state, and dependency graphs are automatically generated and updated via GitHub Actions.
> Last updated: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}

![CI/CD](https://github.com/{os.environ.get('GITHUB_REPOSITORY', 'user/repo')}/actions/workflows/ci-cd.yml/badge.svg)
![Auto-Doc](https://github.com/{os.environ.get('GITHUB_REPOSITORY', 'user/repo')}/actions/workflows/repo-automation.yml/badge.svg)

## Project Overview
This repository features an automated documentation and analysis system that continuously maps its own architecture, dependencies, and codebase structure.

## Technology Stack

### Languages Detected
"""
    for lang, count in state.get("languages", {}).items():
        readme_content += f"- **{lang}**: {count} files\n"

    readme_content += "\n### Frameworks & Libraries\n"
    for fw in state.get("frameworks", []):
        readme_content += f"- {fw}\n"

    if not state.get("frameworks"):
        readme_content += "- None detected explicitly yet.\n"

    readme_content += "\n### Databases\n"
    for db in state.get("databases", []):
        readme_content += f"- {db}\n"
    if not state.get("databases"):
        readme_content += "- None detected explicitly yet.\n"

    readme_content += "\n## System Architecture\n\n```mermaid\n"
    try:
        with open("docs/diagrams/architecture.mmd", "r") as f:
            readme_content += f.read()
    except FileNotFoundError:
        readme_content += "graph TD;\n    Repo[Repository] --> Unknown;\n"
    readme_content += "```\n\n"

    readme_content += "## Dependency Map\n\n```mermaid\n"
    try:
        with open("docs/diagrams/dependencies.mmd", "r") as f:
            readme_content += f.read()
    except FileNotFoundError:
        readme_content += "graph LR;\n    Repo[Repository] --> Unknown;\n"
    readme_content += "```\n\n"

    readme_content += """## Environment Variables
The following environment variables were detected in sample `.env` files:
"""
    for env in state.get("env_vars", []):
        readme_content += f"- `{env}`\n"
    if not state.get("env_vars"):
        readme_content += "- None detected explicitly yet.\n"

    readme_content += """
## Repository Structure

```
.
"""
    # Simple top level structure
    for d in state.get("directories", []):
        if d != "." and not "/" in d:
            readme_content += f"├── {d}/\n"
    readme_content += "```\n\n"

    readme_content += """## Setup Instructions
1. Clone the repository.
2. Ensure you have Python 3.10+ installed.
3. (Optional) Create a virtual environment: `python -m venv venv && source venv/bin/activate`
4. Install requirements: `pip install -r scripts/automation/requirements.txt`
5. Run the automation scripts locally if desired.

## Deployment Instructions
This system is purely automated via GitHub Actions. There is no active server to deploy.
1. Commit the `.github/workflows/` directory to your repository.
2. Ensure the `OPENAI_API_KEY` secret is configured in your repository settings to enable the AI agent.
3. Push to `main` to trigger the CI/CD and automation pipelines.

## API Documentation
Currently, this repository operates locally and via GitHub Actions without exposing external APIs.

## Changelog Summaries
View the repository's commit history for granular updates. The AI agent will automatically summarize PR changes.

## Status Badges
![CI/CD](https://github.com/user/repo/actions/workflows/ci-cd.yml/badge.svg)
![Auto-Doc](https://github.com/user/repo/actions/workflows/repo-automation.yml/badge.svg)

## Contribution Guide
To contribute:
1. Make your changes.
2. The GitHub Actions workflows will automatically analyze the repository.
3. The README and architecture diagrams will be regenerated and committed back to your PR or `main`.
4. The AI Documentation Agent will review your PR and provide summaries.
"""

    with open("README.md", "w") as f:
        f.write(readme_content)

    print("README.md updated successfully.")


if __name__ == "__main__":
    update_readme()
