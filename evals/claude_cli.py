#!/usr/bin/env python3
"""Ask a Claude model one question through the Claude Code CLI.

Both live eval modes (`run_evals.py --model` and `hallucination/run_ab.py`) used to call
the Messages API with a key they read from the environment. The plugin directory flags
that as "uses a credential from the environment", and it was true: the scripts held a key.

Now they hold nothing. `claude -p` answers with whatever login the person running it
already has in Claude Code, and this module never reads, passes or prints a credential.
What it sends is the system prompt and the question; what it keeps is the answer text and
the token counts.

The call is isolated so it measures the model and not the session around it: no tools, no
MCP servers, no slash commands, no settings files, no saved session, and a temporary
working directory so no CLAUDE.md is picked up.
"""
import json
import shutil
import subprocess
import tempfile


class CliError(RuntimeError):
    """The CLI ran and said no (not logged in, unknown model, rate limit...)."""


def command(model, system):
    """The argument list for one isolated, tool-less, one-shot call."""
    exe = shutil.which("claude")
    if not exe:
        raise CliError("the `claude` CLI is not on PATH (install Claude Code and log in)")
    return [exe, "-p", "--model", model, "--system-prompt", system,
            "--tools", "", "--output-format", "json", "--no-session-persistence",
            "--strict-mcp-config", "--disable-slash-commands", "--setting-sources", ""]


def read(stdout):
    """(text, usage) from the CLI's JSON result, in the Messages API's usage names."""
    try:
        out = json.loads(stdout)
    except ValueError as exc:
        raise CliError(f"the CLI did not answer in JSON: {stdout[:200]!r}") from exc
    if out.get("is_error"):
        raise CliError(str(out.get("result") or out.get("subtype") or "error")[:300])
    raw = out.get("usage") or {}
    usage = {"input_tokens": (raw.get("input_tokens", 0)
                              + raw.get("cache_creation_input_tokens", 0)
                              + raw.get("cache_read_input_tokens", 0)),
             "output_tokens": raw.get("output_tokens", 0),
             "stop_reason": out.get("stop_reason")}
    return out.get("result") or "", usage


def ask(model, system, user, timeout=180):
    """Send one question; return (text, usage). Raises CliError on any failure."""
    with tempfile.TemporaryDirectory(prefix="dax-evals-") as cwd:
        proc = subprocess.run(command(model, system), input=user, capture_output=True,
                              text=True, encoding="utf-8", cwd=cwd, timeout=timeout)
    if proc.returncode != 0 and not proc.stdout.strip():
        raise CliError(f"claude exited {proc.returncode}: {proc.stderr.strip()[:300]}")
    return read(proc.stdout)
