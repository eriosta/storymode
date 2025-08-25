from __future__ import annotations
import os, time, httpx
from contextlib import contextmanager
from dotenv import load_dotenv

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

def make_openai_client():
    load_dotenv()
    base_url = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
    api_key = os.getenv("OPENAI_API_KEY", "")

    class _Msgs:
        def __init__(self, client): self.client = client
        def create(self, **kwargs):
            return self.client._post("/chat/completions", json=kwargs)

    class _Chat:
        def __init__(self, client): self.completions = _Msgs(client)

    class Client:
        def __init__(self, base_url, api_key):
            self.base_url = base_url.rstrip('/')
            self.api_key = api_key
            self.chat = _Chat(self)

        def _post(self, path, json):
            headers = {"Authorization": f"Bearer {self.api_key}"}
            with httpx.Client(base_url=self.base_url, headers=headers, timeout=60.0) as s:
                r = s.post(path, json=json)
                r.raise_for_status()
                data = r.json()
                # minimal adapter for .choices[0].message.content
                class _Msg: pass
                m = _Msg(); m.content = data["choices"][0]["message"]["content"]
                class _Choice: pass
                c = _Choice(); c.message = m
                class _Resp: pass
                resp = _Resp(); resp.choices = [c]
                return resp

    return Client(base_url, api_key)
