#!/usr/bin/env python3
"""Shared mall_id / base URL resolution for ref393674 score scripts."""
from __future__ import annotations

import argparse
import os
from dataclasses import dataclass

DEFAULT_REF_MALL = "ecudemo393674"
DEFAULT_TGT_MALL = "ecudemo400786"


@dataclass
class MallConfig:
    mall_id: str
    ref_base: str
    tgt_base: str

    def url(self, path: str, *, target: bool = True) -> str:
        base = self.tgt_base if target else self.ref_base
        if not path.startswith("/"):
            path = "/" + path
        return base.rstrip("/") + path


def _strip_base(value: str) -> str:
    return value.rstrip("/")


def _mall_to_base(value: str) -> str:
    value = value.strip()
    if value.startswith("http://") or value.startswith("https://"):
        return _strip_base(value)
    return f"https://{value}.cafe24.com"


def parse_mall_config(argv: list[str] | None = None) -> MallConfig:
    default_mall = os.environ.get("CAFE24_MALL_ID", DEFAULT_TGT_MALL)
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--mall-id", default=default_mall)
    parser.add_argument("--ref-base", default=os.environ.get("CAFE24_REF_BASE"))
    parser.add_argument("--tgt-base", default=os.environ.get("CAFE24_TGT_BASE"))
    parser.add_argument("--ref-mall", default=os.environ.get("CAFE24_REF_MALL", DEFAULT_REF_MALL))
    parser.add_argument("--tgt-mall", default=os.environ.get("CAFE24_TGT_MALL"))
    args, _ = parser.parse_known_args(argv)

    tgt_mall = args.tgt_mall or args.mall_id
    ref_base = _mall_to_base(args.ref_base) if args.ref_base else _mall_to_base(args.ref_mall)
    tgt_base = _mall_to_base(args.tgt_base) if args.tgt_base else _mall_to_base(tgt_mall)
    return MallConfig(mall_id=args.mall_id, ref_base=ref_base, tgt_base=tgt_base)
