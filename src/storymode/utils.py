from __future__ import annotations
import os, time
from contextlib import contextmanager

class Timer:
    def __init__(self): self.start = None; self.elapsed_ms = 0.0
    def __enter__(self):
        self.start = time.time(); return self
    def __exit__(self, *exc):
        self.elapsed_ms = (time.time() - self.start) * 1000.0

def read_txt(fp: str) -> str:
    with open(fp, 'r', encoding='utf-8') as f: return f.read()

def dump_json(obj, fp: str):
    import orjson
    with open(fp, 'wb') as f:
        f.write(orjson.dumps(obj, option=orjson.OPT_INDENT_2))
