import argparse
import asyncio
import json

import pytest

from property_eval import cli
from property_eval.models import Event, Prefix


def arguments(tmp_path, *, timeout=2):
    manifest = tmp_path / "manifest.json"
    manifest.write_text(
        json.dumps(
            {
                "jobs": [
                    {"id": "first", "case": "012", "cutoff": 1},
                    {"id": "second", "case": "012", "cutoff": 1},
                    {"id": "third", "case": "012", "cutoff": 1},
                ]
            }
        )
    )
    return argparse.Namespace(
        manifest=manifest,
        source=tmp_path,
        output=tmp_path / "results",
        concurrency=2,
        max_tokens=100,
        timeout=timeout,
        model="mock",
        env_file=None,
        dry_run=False,
    )


def install_prefix(monkeypatch):
    monkeypatch.setenv("OPENROUTER_API_KEY", "test-only")
    monkeypatch.setattr(
        cli,
        "load_prefix",
        lambda *args: Prefix(
            case_id="property-012",
            cutoff=1,
            source_sha256="test",
            events=[
                Event(
                    id="001",
                    timestamp="2026-01-01",
                    channel="Note",
                    sender="Staff",
                    recipient="Tenant",
                    text="Dishwasher broken.",
                )
            ],
        ),
    )


def response(body):
    content = {
        "mentions": {"mentions": []},
        "links": {"links": []},
        "records": {"records": [], "gaps": []},
    }[body["response_format"]["json_schema"]["name"]]
    return {
        "choices": [
            {
                "finish_reason": "stop",
                "message": {"content": json.dumps(content)},
            }
        ]
    }


def test_parallel_bound_and_failure_retention(tmp_path, monkeypatch):
    install_prefix(monkeypatch)
    active = peak = calls = 0

    async def complete(*args):
        nonlocal active, peak, calls
        calls += 1
        number = calls
        active += 1
        peak = max(active, peak)
        try:
            await asyncio.sleep(0.01)
            if number == 1:
                raise ValueError("malformed provider response")
            return response(args[-1])
        finally:
            active -= 1

    monkeypatch.setattr(cli, "complete", complete)
    args = arguments(tmp_path)
    assert asyncio.run(cli.run(args)) == 1
    results = json.loads((args.output / "summary.json").read_text())["results"]
    assert peak == 2
    assert [r["status"] for r in results] == ["error", "valid", "valid"]
    assert all((args.output / r["id"] / "input.json").exists() for r in results)
    assert all("test-only" not in f.read_text() for f in args.output.rglob("*.json"))


def test_timeout_recorded_for_every_job(tmp_path, monkeypatch):
    install_prefix(monkeypatch)

    async def complete(*args):
        await asyncio.sleep(1)

    monkeypatch.setattr(cli, "complete", complete)
    args = arguments(tmp_path, timeout=0.01)
    assert asyncio.run(cli.run(args)) == 1
    results = json.loads((args.output / "summary.json").read_text())["results"]
    assert len(results) == 3
    assert all(r["error_type"] == "TimeoutError" for r in results)


def test_existing_run_is_not_overwritten(tmp_path, monkeypatch):
    install_prefix(monkeypatch)
    args = arguments(tmp_path)
    args.output.mkdir()
    marker = args.output / "keep.txt"
    marker.write_text("original")
    with pytest.raises(FileExistsError):
        asyncio.run(cli.run(args))
    assert marker.read_text() == "original"
