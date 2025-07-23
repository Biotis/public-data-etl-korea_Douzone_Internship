# Biznum ETL DART Pipeline

A robust ETL pipeline for collecting, cleaning, validating, transforming, and exporting Korean business registration master data, using public APIs (e.g., OpenDART).  
This project is designed to demonstrate practical data engineering skills and reproducible, testable ETL pipelines.

---

## 🚀 Features

- **Data Collection**: Download corporate master data from OpenDART API.
- **Standardization**: Clean and standardize company information (registration numbers, homepage, representative names, etc).
- **Validation**: Validate business registration numbers using the National Tax Service (NTS) API.
- **Transformation**: Enrich and map data using metadata for analytics or reporting.
- **Export**: Output results in Excel or CSV for downstream tasks.

---

## 🗂️ Project Structure

```
.
├── README.md
├── requirements.txt
├── .gitignore
├── data/            # Input/output (sample) files
├── src/
│   ├── config.py
│   ├── pipeline.py  # Main pipeline script
│   ├── collect/
│   ├── standardize/
│   ├── validate/
│   ├── transform/
│   └── export/
└── tests/           # Unit tests for each ETL stage
```

---

## 🛠️ Getting Started

### 1. Install requirements

```bash
pip install -r requirements.txt
```

### 2. Set API keys

- Copy `src/config.py.example` to `src/config.py` and enter your API keys:
    - `DART_API_KEY`: OpenDART API Key
    - `NTS_API_KEY`: National Tax Service API Key

### 3. Run the pipeline

```bash
python -m src.pipeline
```

- Results will be generated in the `data/` folder.

---

## 🏗️ Pipeline Flow

1. **Collect**: Download raw master data from OpenDART (to `data/raw_dart_data.xlsx`)
2. **Standardize**: Clean and normalize fields (to `data/standardized_company_data.xlsx`)
3. **Validate**: Check validity of business numbers (to `data/validated_company_data.xlsx`)
4. **Transform**: Enrich or map columns using metadata (to `data/metadata_enriched_data.xlsx`)
5. **Export**: Output as final CSV (`data/final_output.csv`)

---

## 🧹 Example Data

- Sample processed files (100 records) are provided in `data/`.
- Actual API keys and real-world data are not included for privacy.

---

## 🧪 Testing

Unit tests are provided in the `tests/` directory.

# Run tests

```bash
PYTHONPATH=./src pytest tests
```

Example test file: `tests/test_standardize.py`

---

## 💡 Key ETL Functions

- `collect/extract_and_save_data`: Download and save company master data
- `standardize/standardize_company_data`: Clean fields, homepage, names, etc.
- `validate/validate_biz_numbers`: Check business number validity via API
- `transform/transform_with_metadata`: Apply enrichment or mapping
- `export/export_to_csv`: Save results for downstream use

---

## 📝 Notes

- **API keys** must be set in `src/config.py` (do not commit real keys).
- Intermediate and output files are ignored by `.gitignore`.
- This project was used to complete an assigned task during an internship at Douzone Bizon

---

## 📈 Example Usage

```python
from src.standardize.standardizer import standardize_company_data

standardize_company_data(
    "data/raw_dart_data.xlsx", "data/standardized_company_data.xlsx"
)
```

---

## 🤝 License

Copyright (c) 2025 Jung Seungil

This project was created as part of an internship at Douzone Bizon.

All rights reserved.

This codebase is intended for educational and portfolio demonstration purposes only.  
You may view and reference this project for learning or evaluation,  
but reproduction, distribution, modification, or use in any commercial or production environment  
is strictly prohibited without prior written permission from the author.

Unauthorized commercial use is not allowed under any circumstances.
