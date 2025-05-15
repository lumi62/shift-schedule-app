# Shift Schedule App

A sleek, AI-powered chatbot that helps employees quickly retrieve their weekly shift schedule using **natural language input** — even if their name is misspelled or typed with errors!

## Features

- ✅ **Fuzzy Matching** for Employee Names (using RapidFuzz)
- ✅ **Dynamic Schedule Retrieval** from a live Google Sheet (via SheetBest API)
- ✅ **Beautiful Gradio Interface** with visual blocks
- ✅ **Color-coded Shift Blocks**:

## Tech Stack

- [Gradio](https://www.gradio.app/) – beautiful frontend UI
- [RapidFuzz](https://github.com/maxbachmann/RapidFuzz) – for fuzzy name matching
- [SheetBest](https://sheet.best/) – turns Google Sheets into a REST API
- [Python](https://www.python.org/) – the engine behind it all

## Installation

```bash
git clone https://github.com/lumi62/shift-schedule-app.git
cd shift-schedule-app
pip install -r requirements.txt
python app.py
Built By:
Lumiere
