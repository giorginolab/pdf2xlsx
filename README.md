# pdf2xlsx

Extract tables from a PDF and write them into a single XLSX worksheet.

## Install

```bash
uv sync
```

## Usage

```bash
uv run pdf2xlsx input.pdf
uv run pdf2xlsx input.pdf --output tables.xlsx --start 0 --end 1
```

## Gradio App

```bash
uv run pdf2xlsx-gradio
```
