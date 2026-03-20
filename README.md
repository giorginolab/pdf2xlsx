---
title: pdf2xlsx
emoji: 📄
colorFrom: blue
colorTo: green
sdk: gradio
sdk_version: 5.23.3
python_version: "3.13"
app_file: gradio_app/app.py
fullWidth: true
short_description: Extract PDF tables to XLSX with preview.
---

# pdf2xlsx

Extract tables from a PDF and write them into a single XLSX worksheet. A wrapper around https://github.com/ArtifexSoftware/pdf2docx.

Outputs all tables detected in the PDF, prepending each row by table ID, row ID, and number of columns. Data follows, as text (text-to-number-to-excel in all locales would be a nightmare).


## Usage

After clone...

```bash
uv sync
uv run pdf2xlsx input.pdf
uv run pdf2xlsx input.pdf --output tables.xlsx --start 0 --end 1
```

## Usage without install

```bash
uv run --with https://github.com/giorginolab/pdf2xlsx.git pdf2xlsx
```

## Gradio App

```bash
uv run --extra gradio python gradio_app/app.py
```

## Live App 

Here: https://huggingface.co/spaces/tonigi/pdf2xlsx
