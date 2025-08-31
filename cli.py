import typer
from pathlib import Path
import argparse
from core_logic import receive_paths

app = typer.Typer()

@app.command()
def main(
        input_path: Path = typer.Argument(..., help="Folder with PDFs"),
        output_path: Path = typer.Argument(..., help="Where to save output")
):
    receive_paths(input_path, output_path)

if __name__ == "__main__":
    app()
