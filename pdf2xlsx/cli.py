from __future__ import annotations

from pathlib import Path
from typing import Annotated

import typer

from .converter import extract_tables_to_xlsx

app = typer.Typer(
    add_completion=False,
    help="Extract tables from a PDF file and write them to an XLSX workbook.",
)


@app.command()
def main(
    pdf_path: Annotated[
        Path,
        typer.Argument(
            ...,
            exists=True,
            dir_okay=False,
            readable=True,
            resolve_path=True,
            help="Path to the source PDF.",
        ),
    ],
    output_path: Annotated[
        Path | None,
        typer.Option(
            "--output",
            "-o",
            dir_okay=False,
            resolve_path=True,
            help="Destination XLSX path. Defaults to <pdf-stem>.xlsx.",
        ),
    ] = None,
    start: Annotated[
        int,
        typer.Option("--start", min=0, help="Start page index for extraction."),
    ] = 0,
    end: Annotated[
        int | None,
        typer.Option(
            "--end",
            min=0,
            help="End page index for extraction. Omit to process through the end.",
        ),
    ] = None,
) -> None:
    if end is not None and end < start:
        raise typer.BadParameter("--end must be greater than or equal to --start.")

    destination = output_path or pdf_path.with_suffix(".xlsx")
    row_count = extract_tables_to_xlsx(pdf_path, destination, start=start, end=end)

    typer.echo(f"Wrote {row_count} row(s) to {destination}")


if __name__ == "__main__":
    app()
