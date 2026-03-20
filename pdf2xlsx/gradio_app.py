from __future__ import annotations

import tempfile
from pathlib import Path

import gradio as gr

from .converter import extract_tables_to_xlsx


def convert_pdf_to_xlsx(
    pdf_file: str | None,
    start: float,
    end_enabled: bool,
    end: float,
) -> tuple[str, str | None]:
    if not pdf_file:
        return "Upload a PDF to begin.", None

    pdf_path = Path(pdf_file)
    start_page = int(start)
    end_page = int(end) if end_enabled else None

    if end_page is not None and end_page < start_page:
        return "End page must be greater than or equal to start page.", None

    output_dir = Path(tempfile.mkdtemp(prefix="pdf2xlsx-gradio-"))
    output_path = output_dir / f"{pdf_path.stem}.xlsx"

    row_count = extract_tables_to_xlsx(
        pdf_path,
        output_path,
        start=start_page,
        end=end_page,
    )

    return f"Wrote {row_count} row(s) to {output_path.name}.", str(output_path)


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

        convert.click(
            fn=convert_pdf_to_xlsx,
            inputs=[pdf_file, start, end_enabled, end],
            outputs=[status, download],
        )

    return app


def main() -> None:
    build_app().launch()


if __name__ == "__main__":
    main()
