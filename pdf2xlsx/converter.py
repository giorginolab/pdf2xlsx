from __future__ import annotations

from pathlib import Path
from typing import Any

import xlsxwriter
from pdf2docx import Converter


def extract_tables_to_xlsx(
    pdf_path: Path | str,
    output_path: Path | str,
    *,
    start: int = 0,
    end: int | None = None,
) -> int:
    """Extract PDF tables and write flattened rows to a single XLSX worksheet."""
    source = Path(pdf_path)
    destination = Path(output_path)
    destination.parent.mkdir(parents=True, exist_ok=True)

    converter = Converter(str(source))
    try:
        tables = converter.extract_tables(start=start, end=end)
    finally:
        converter.close()

    rows = [row for table in tables for row in table]

    with xlsxwriter.Workbook(str(destination)) as workbook:
        worksheet = workbook.add_worksheet("Tables")

        for row_num, data in enumerate(rows):
            worksheet.write_row(row_num, 0, _normalize_row(data))

    return len(rows)


def _normalize_row(row: list[Any]) -> list[Any]:
    return ["" if value is None else value for value in row]
