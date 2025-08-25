from __future__ import annotations
import os, json, typer
from rich import print
from .extract import batch_extract
from .eval import evaluate

app = typer.Typer(add_completion=False)

@app.command()
def extract(in_dir: str = typer.Option(..., help="Folder of .txt reports"),
            out_dir: str = typer.Option(..., help="Output folder for .json"),
            model: str = typer.Option("gpt-4o-mini", help="Model name"),
            max_workers: int = typer.Option(4, help="Parallelism hint")):
    batch_extract(in_dir=in_dir, out_dir=out_dir, model=model, max_workers=max_workers)

@app.command()
def eval(pred_dir: str = typer.Option(..., help="Folder of predicted .json"),
         ref_dir: str = typer.Option(..., help="Folder of reference .json")):
    res = evaluate(pred_dir, ref_dir)
    print(res)

if __name__ == "__main__":
    app()
