from langchain_core.tools import tool


@tool
def github_actions_matrix_basics() -> str:
    """Matrix vs reusable workflows — short."""
    return (
        "GitHub Actions:\n"
        "- matrix: version × OS for tests\n"
        "- reusable workflows for DRY deploy\n"
        "- environments + protection rules for prod\n"
        "Validate syntax in GitHub docs; YAML is easy to mis-indent."
    )


@tool
def ci_secrets_hygiene() -> str:
    """Secrets in CI."""
    return (
        "Never echo secrets; use OIDC to cloud where possible.\n"
        "Least-privilege deploy keys; rotate on incident.\n"
        "Fork PRs: do not run untrusted workflows with secrets without approval gates."
    )


def get_devops_tools():
    return [github_actions_matrix_basics, ci_secrets_hygiene]
