# Biznum ETL DART Pipeline

A robust and modular ETL pipeline for collecting, cleaning, validating, transforming, and exporting Korean business registration data using public APIs such as **OpenDART** and **NTS (National Tax Service)**.

---

## 🎯 Project Objective

This project was developed to fulfill the following goal:

> **"To continuously collect data from various sources, including business registration numbers, and construct a unified, consistent master table through standardization and validation."**

This ETL pipeline was designed as part of a data engineering internship assignment at **Douzone Bizon** and demonstrates practical skills in public data integration, API-driven ingestion, validation, and transformation.

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
├── data/             # Input/output (sample data included)
├── src/
│   ├── config.py     # API keys and configuration
│   ├── pipeline.py   # Main ETL pipeline entry point
│   ├── collect/      # Data ingestion from OpenDART
│   ├── standardize/  # Cleaning & normalization scripts
│   ├── validate/     # NTS-based business number verification
│   ├── transform/    # Metadata enrichment and formatting
│   └── export/       # Output as CSV/Excel
└── tests/            # Unit tests for individual pipeline stages
```

---

## 🛠️ Getting Started

### 1. Install requirements

```bash
pip install -r requirements.txt
```

### 2. Configure API keys

- Copy `src/config.py.example` to `src/config.py` and enter your API keys:
    - `DART_API_KEY`: [Apply for OpenDART API Key](https://opendart.fss.or.kr/)
    - `NTS_API_KEY`: [Apply for Business Registration Validation API (data.go.kr)](https://www.data.go.kr/tcs/dss/selectApiDataDetailView.do?publicDataPk=15081808)
      
   # src/config.py (replace with your real key)
    - DART_API_KEY = "YOUR_DART_API_KEY"
    - NTS_API_KEY = "YOUR_NTS_API_KEY"

💡 Both APIs are free to use but require registration. Approval may take 1–2 business days depending on the service.


### 3. Run the pipeline

```bash
python -m src.pipeline
```

- Results will be generated in the `data/` folder.

---

## 🔄 Pipeline Flow

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

- **API keys** must be set in `src/config.py`
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

## 🛑 Caution

API credentials must not be committed to version control.

Intermediate results and output files are .gitignored by default.

This project is for educational and portfolio purposes only.

---

## 🧑‍💻 Author

Jung Seungil (정승일)
Internship Project @ Douzone Bizon
GitHub: github.com/Biotis
email: rhjung2001@gmail.com

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
