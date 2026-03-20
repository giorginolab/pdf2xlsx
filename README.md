---
title: pdf2xlsx
emoji: 📄
colorFrom: blue
colorTo: green
sdk: gradio
sdk_version: 5.23.3
python_version: "3.13"
app_file: app.py
fullWidth: true
short_description: Extract PDF tables into XLSX with downloadable output and preview.
---

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
