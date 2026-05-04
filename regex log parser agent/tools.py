from langchain_core.tools import tool


@tool
def redos_safety_reminder() -> str:
    """Catastrophic backtracking warning."""
    return (
        "ReDoS: nested quantifiers + overlapping branches can explode on hostile input.\n"
        "Prefer possessive/atomic groups where supported, or limit input length in pipelines.\n"
        "Test with worst-case synthetic lines in a sandbox."
    )


@tool
def grep_vs_pcre_hint() -> str:
    """Engine differences."""
    return (
        "grep -E (ERE) vs PCRE vs ripgrep: syntax differs for +? (), word boundaries, etc.\n"
        "Always say which engine you targeted; validate with `grep`/`rg --pcre2` as appropriate."
    )


def get_regex_log_tools():
    return [redos_safety_reminder, grep_vs_pcre_hint]
