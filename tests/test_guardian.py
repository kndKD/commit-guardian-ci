import io
import json
import os
import sys
from contextlib import redirect_stdout

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from guardian.cli import main
from guardian.llm import suggest_via_llm
from guardian.scoring import check


def _run_cli(args):
    buf = io.StringIO()
    with redirect_stdout(buf):
        code = main(args)
    return code, buf.getvalue()


def test_compliant_feat():
    r = check("feat: add login endpoint")
    assert r["compliant"] and r["score"] == 85


def test_non_compliant():
    r = check("added stuff")
    assert not r["compliant"] and r["score"] == 20
    assert r["suggestion"] == "feat: added stuff"


def test_empty():
    r = check("")
    assert not r["compliant"] and r["score"] == 0


def test_scope_and_breaking():
    r = check("feat(api)!: change login response shape")
    assert r["compliant"]


def test_short_subject_flagged():
    r = check("fix: typo")
    assert not r["compliant"]
    assert any("short" in i for i in r["issues"])


def test_llm_disabled_by_default():
    assert suggest_via_llm("added stuff") is None


def test_long_subject_flagged():
    r = check("feat: " + "improve the login flow for returning users " * 3)
    assert not r["compliant"]
    assert any("long" in i for i in r["issues"])


def test_type_only_no_subject():
    r = check("feat:")
    assert not r["compliant"]
    assert r["suggestion"] == "feat: describe the change"


def test_cli_json_output():
    code, out = _run_cli(["--json", "feat: add login endpoint"])
    assert code == 0
    data = json.loads(out)
    assert data[0]["score"] == 85 and data[0]["compliant"]


def test_cli_quiet_hides_compliant():
    code, out = _run_cli(["--quiet", "feat: add login endpoint"])
    assert code == 0 and out == ""


def test_cli_quiet_shows_non_compliant():
    code, out = _run_cli(["--quiet", "added stuff"])
    assert code == 1 and "added stuff" in out


def test_cli_no_input_is_usage_error():
    code, _out = _run_cli([])
    assert code == 2
