from langchain_core.tools import tool


@tool
def compose_v2_basics() -> str:
    """Docker Compose file shape (v2+)."""
    return (
        "Top-level keys often include: services, networks, volumes.\n"
        "Per service: image or build, ports, environment or env_file, depends_on, networks, volumes.\n"
        "Use explicit image tags; avoid 'latest' in anything serious."
    )


@tool
def compose_security_nudge() -> str:
    """Common hardening reminders for local/dev compose."""
    return (
        "Do not commit real secrets; use .env (gitignored) or a secret manager in prod.\n"
        "Bind ports to 127.0.0.1 if you do not need LAN exposure.\n"
        "Run as non-root in images when the base image allows."
    )


def get_compose_tools():
    return [compose_v2_basics, compose_security_nudge]
