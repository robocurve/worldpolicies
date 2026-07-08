"""Catalog integrity + CLI tests. Every entry is validated; malformed entries fail CI."""

from __future__ import annotations

import re

import pytest

from worldpolicies import CATALOG, Policy, by_embodiment, by_tag, catalog, get
from worldpolicies.cli import main

HF_ID = re.compile(r"^[\w.-]+/[\w.-]+$")
GH_URL = re.compile(r"^https://github\.com/[\w.-]+/[\w.-]+$")
KNOWN_METHODS = {"lora", "full-ft"}
KNOWN_METRICS = {"eval_loss", "open_loop_mse", "success_rate"}


def test_catalog_nonempty() -> None:
    assert catalog() == CATALOG
    assert len(CATALOG) >= 3


def test_names_unique() -> None:
    names = [p.name for p in CATALOG]
    assert len(names) == len(set(names))


@pytest.mark.parametrize("policy", CATALOG, ids=lambda p: p.name)
def test_entry_well_formed(policy: Policy) -> None:
    assert HF_ID.match(policy.hf_id), policy.hf_id
    assert policy.hf_id.startswith("robocurve/")
    assert HF_ID.match(policy.base_model)
    assert GH_URL.match(policy.training_repo), policy.training_repo
    assert policy.method in KNOWN_METHODS
    assert policy.eval_metric in KNOWN_METRICS
    assert policy.eval_value > 0
    assert policy.title and policy.description and policy.eval_protocol
    assert policy.embodiment and policy.trained_by
    assert policy.tags
    assert policy.hf_url == f"https://huggingface.co/{policy.hf_id}"


def test_get_and_filters() -> None:
    p = get("gr00t-n17-so101")
    assert p.embodiment == "so101"
    assert p in by_embodiment("so101")
    assert p in by_tag("gr00t")
    assert by_embodiment("nonexistent") == ()
    assert by_tag("nonexistent") == ()
    with pytest.raises(KeyError):
        get("nope")


def test_cli_list(capsys: pytest.CaptureFixture[str]) -> None:
    main(["list"])
    out = capsys.readouterr().out
    for p in CATALOG:
        assert p.hf_url in out


def test_cli_list_filters(capsys: pytest.CaptureFixture[str]) -> None:
    main(["list", "--embodiment", "yam-bimanual", "--tag", "pi05"])
    out = capsys.readouterr().out
    assert "pi05-yam" in out
    assert "gr00t-n17-so101" not in out


def test_cli_info(capsys: pytest.CaptureFixture[str]) -> None:
    main(["info", "pi05-yam"])
    out = capsys.readouterr().out
    assert "open_loop_mse = 0.00206" in out
    assert "https://huggingface.co/robocurve/pi05-yam-molmoact2" in out
