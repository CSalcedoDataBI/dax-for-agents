#!/usr/bin/env python3
"""Tests for the CLI route the live evals take. Run: python -m unittest discover -s evals

Offline: nothing here starts `claude`. What is tested is the part that has to hold without
a model in the loop -- no credential reaches the command line, a CLI error is an error and
not an empty answer, and the usage names match what the run files already store.
"""
import json
import os
import sys
import unittest
from unittest import mock

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import claude_cli                                                 # noqa: E402


class Command(unittest.TestCase):
    def test_it_isolates_the_call_and_carries_no_key(self):
        with mock.patch("claude_cli.shutil.which", return_value="claude"):
            argv = claude_cli.command("claude-haiku-5-5", "be brief")
        self.assertEqual(argv[:2], ["claude", "-p"])
        self.assertEqual(argv[argv.index("--tools") + 1], "")
        for flag in ("--no-session-persistence", "--strict-mcp-config",
                     "--disable-slash-commands", "--setting-sources"):
            self.assertIn(flag, argv)
        joined = " ".join(argv).lower()
        for word in ("api_key", "api-key", "token", "secret"):
            self.assertNotIn(word, joined)

    def test_a_missing_cli_is_an_error_not_a_crash(self):
        with mock.patch("claude_cli.shutil.which", return_value=None):
            with self.assertRaises(claude_cli.CliError):
                claude_cli.command("claude-haiku-5-5", "x")


class Read(unittest.TestCase):
    def test_it_returns_the_text_and_the_api_usage_names(self):
        out = json.dumps({"result": "CALCULATE", "stop_reason": "end_turn",
                          "usage": {"input_tokens": 2, "cache_creation_input_tokens": 887,
                                    "cache_read_input_tokens": 10, "output_tokens": 3}})
        text, usage = claude_cli.read(out)
        self.assertEqual(text, "CALCULATE")
        self.assertEqual(usage, {"input_tokens": 899, "output_tokens": 3,
                                 "stop_reason": "end_turn"})

    def test_an_error_result_raises_instead_of_scoring_as_an_empty_answer(self):
        """An empty answer scores zero inventions -- the best result, for not answering."""
        out = json.dumps({"is_error": True, "result": "Not logged in"})
        with self.assertRaisesRegex(claude_cli.CliError, "Not logged in"):
            claude_cli.read(out)

    def test_output_that_is_not_json_raises(self):
        with self.assertRaises(claude_cli.CliError):
            claude_cli.read("Error: something went wrong")


class Ask(unittest.TestCase):
    def test_a_failed_run_with_no_output_raises(self):
        done = mock.Mock(returncode=1, stdout="", stderr="boom")
        with mock.patch("claude_cli.shutil.which", return_value="claude"), \
                mock.patch("claude_cli.subprocess.run", return_value=done):
            with self.assertRaisesRegex(claude_cli.CliError, "boom"):
                claude_cli.ask("claude-haiku-5-5", "s", "u")

    def test_the_question_goes_on_stdin_not_in_argv(self):
        done = mock.Mock(returncode=0, stderr="",
                         stdout=json.dumps({"result": "ok", "usage": {}}))
        with mock.patch("claude_cli.shutil.which", return_value="claude"), \
                mock.patch("claude_cli.subprocess.run", return_value=done) as run:
            self.assertEqual(claude_cli.ask("claude-haiku-5-5", "s", "the question")[0], "ok")
        self.assertEqual(run.call_args.kwargs["input"], "the question")
        self.assertNotIn("the question", run.call_args.args[0])


if __name__ == "__main__":
    unittest.main()
