from __future__ import annotations

from pathlib import Path
from typing import Any

import xlsxwriter
from pdf2docx import Converter

HEADER_ROW = ["TableID", "RowID", "Columns", "Data"]


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

    rows = extract_table_rows(source, start=start, end=end)

    with xlsxwriter.Workbook(str(destination)) as workbook:
        worksheet = workbook.add_worksheet("Tables")
        worksheet.write_row(0, 0, HEADER_ROW)

        for row_num, data in enumerate(rows, start=1):
            worksheet.write_row(row_num, 0, _normalize_row(data))

    return len(rows)


def extract_table_rows(
    pdf_path: Path | str,
    *,
    start: int = 0,
    end: int | None = None,
) -> list[list[Any]]:
    """Extract flattened table rows with metadata for downstream consumers."""
    source = Path(pdf_path)

    converter = Converter(str(source))
    try:
        tables = converter.extract_tables(start=start, end=end)
    finally:
        converter.close()

    rows: list[list[Any]] = []
    for table_number, table in enumerate(tables, start=1):
        column_count = max((len(row) for row in table), default=0)
        for row_id, row in enumerate(table, start=1):
            rows.append([table_number, row_id, column_count, *_normalize_row(row)])
    return rows


def _normalize_row(row: list[Any]) -> list[Any]:
    return ["" if value is None else value for value in row]
