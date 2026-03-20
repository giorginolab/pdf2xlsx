from __future__ import annotations

import sys
import tempfile
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

import gradio as gr
import pandas as pd

from pdf2xlsx.converter import HEADER_ROW, extract_table_rows, extract_tables_to_xlsx


def convert_pdf_to_xlsx(
    pdf_file: str | None,
    start: float,
    end_enabled: bool,
    end: float,
) -> tuple[str, str | None, pd.DataFrame]:
    if not pdf_file:
        return "Upload a PDF to begin.", None, _build_preview_dataframe([])

    pdf_path = Path(pdf_file)
    start_page = int(start)
    end_page = int(end) if end_enabled else None

    if end_page is not None and end_page < start_page:
        return (
            "End page must be greater than or equal to start page.",
            None,
            _build_preview_dataframe([]),
        )

    output_dir = Path(tempfile.mkdtemp(prefix="pdf2xlsx-gradio-"))
    output_path = output_dir / f"{pdf_path.stem}.xlsx"
    rows = extract_table_rows(pdf_path, start=start_page, end=end_page)

    row_count = extract_tables_to_xlsx(pdf_path, output_path, start=start_page, end=end_page)
    preview = _build_preview_dataframe(rows[:50])
    return f"Wrote {row_count} row(s) to {output_path.name}.", str(output_path), preview


def build_app() -> gr.Blocks:
    with gr.Blocks(title="pdf2xlsx") as app:
        gr.Markdown("# pdf2xlsx")
        gr.Markdown("Upload a PDF and extract its tables into a single XLSX workbook.")

        with gr.Row():
            pdf_file = gr.File(label="PDF", file_types=[".pdf"], type="filepath")

        with gr.Row():
            start = gr.Number(label="Start Page", value=0, minimum=0, precision=0)
            end_enabled = gr.Checkbox(label="Set End Page", value=False)
            end = gr.Number(label="End Page", value=0, minimum=0, precision=0)

        convert = gr.Button("Convert", variant="primary")
        status = gr.Textbox(label="Status", interactive=False)
        download = gr.File(label="XLSX Output")
        preview = gr.Dataframe(label="Preview", interactive=False, wrap=True)

        convert.click(
            fn=convert_pdf_to_xlsx,
            inputs=[pdf_file, start, end_enabled, end],
            outputs=[status, download, preview],
        )

    return app


def main() -> None:
    build_app().launch()


def _preview_headers(rows: list[list[Any]]) -> list[str]:
    max_width = max((len(row) for row in rows), default=len(HEADER_ROW))
    data_column_count = max(max_width - 3, 1)
    return [*HEADER_ROW[:3], *[f"Data{i}" for i in range(1, data_column_count + 1)]]


def _build_preview_dataframe(rows: list[list[Any]]) -> pd.DataFrame:
    normalized_rows = [["" if value is None else value for value in row] for row in rows]
    headers = _preview_headers(normalized_rows)
    padded_rows = [[*row, *([""] * (len(headers) - len(row)))] for row in normalized_rows]
    return pd.DataFrame(padded_rows, columns=headers)


demo = build_app()


if __name__ == "__main__":
    main()
