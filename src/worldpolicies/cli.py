"""``worldpolicies`` CLI: list and inspect catalogued checkpoints."""

from __future__ import annotations

import argparse

from .catalog import CATALOG, get


def _cmd_list(args: argparse.Namespace) -> None:
    policies = CATALOG
    if args.embodiment:
        policies = tuple(p for p in policies if p.embodiment == args.embodiment)
    if args.tag:
        policies = tuple(p for p in policies if args.tag in p.tags)
    for p in policies:
        print(
            f"{p.name:16}  {p.embodiment:13}  {p.method:8}  "
            f"{p.eval_metric}={p.eval_value:g}  {p.hf_url}"
        )


def _cmd_info(args: argparse.Namespace) -> None:
    p = get(args.name)
    print(f"{p.title}\n")
    print(p.description + "\n")
    rows = [
        ("hf", p.hf_url),
        ("base model", p.base_model),
        ("embodiment", p.embodiment),
        ("method", p.method),
        ("framework", p.framework),
        ("eval", f"{p.eval_metric} = {p.eval_value:g} ({p.eval_protocol})"),
        ("training code", p.training_repo),
        ("trained by", p.trained_by),
        ("tags", ", ".join(p.tags)),
    ]
    for k, v in rows:
        print(f"  {k:14} {v}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="worldpolicies",
        description="Robocurve's registry of published robot-policy checkpoints.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_list = sub.add_parser("list", help="list catalogued policies")
    p_list.add_argument("--embodiment", help="filter by embodiment key")
    p_list.add_argument("--tag", help="filter by tag")
    p_list.set_defaults(func=_cmd_list)

    p_info = sub.add_parser("info", help="show one policy in detail")
    p_info.add_argument("name", help="policy short key")
    p_info.set_defaults(func=_cmd_info)

    return parser


def main(argv: list[str] | None = None) -> None:
    args = build_parser().parse_args(argv)
    args.func(args)
