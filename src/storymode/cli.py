from __future__ import annotations
import os, json, typer
from rich import print
from rich.table import Table
from .extract import batch_extract
from .eval import evaluate
from .models import model_manager

app = typer.Typer(add_completion=False)

@app.command()
def extract(in_dir: str = typer.Option(..., help="Folder of .txt reports"),
            out_dir: str = typer.Option(..., help="Output folder for .json"),
            model: str = typer.Option("mistral-7b-instruct", help="Model name"),
            max_workers: int = typer.Option(4, help="Parallelism hint"),
            temperature: float = typer.Option(0.0, help="Generation temperature"),
            max_tokens: int = typer.Option(1200, help="Maximum tokens to generate")):
    """Extract structured data from radiology reports using specified model."""
    batch_extract(
        in_dir=in_dir, 
        out_dir=out_dir, 
        model=model, 
        max_workers=max_workers,
        temperature=temperature,
        max_tokens=max_tokens
    )

@app.command()
def eval(pred_dir: str = typer.Option(..., help="Folder of predicted .json"),
         ref_dir: str = typer.Option(..., help="Folder of reference .json")):
    """Evaluate extraction results against reference annotations."""
    res = evaluate(pred_dir, ref_dir)
    print(res)

@app.command()
def list_models():
    """List all available models with their configurations."""
    table = Table(title="Available Models")
    table.add_column("Model Name", style="cyan")
    table.add_column("Backend", style="green")
    table.add_column("Model Path", style="yellow")
    table.add_column("Context Window", style="blue")
    table.add_column("JSON Mode", style="magenta")
    
    for model_name, config in model_manager.MODEL_CONFIGS.items():
        table.add_row(
            model_name,
            config.backend,
            config.model_path,
            str(config.context_window),
            "✓" if config.json_mode_supported else "✗"
        )
    
    print(table)
    print("\n[bold]Usage:[/bold]")
    print("  storymode extract --in-dir data/reports --out-dir results --model mistral-7b-instruct")
    print("  storymode extract --in-dir data/reports --out-dir results --model qwen2.5-14b-instruct --temperature 0.2")

if __name__ == "__main__":
    app()
