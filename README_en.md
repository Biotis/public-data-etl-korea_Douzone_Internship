# Biznum ETL DART Pipeline

An end-to-end ETL pipeline designed to collect, preprocessing, validate, and transform Korean corporate master data using public APIs, including OpenDART and the National Tax Service (NTS).  
This project was built as part of a data engineering internship at **Douzone Bizon**, with a focus on integrating real-world public data into a consistent and clean format for downstream analytics.

---

## Project Goal

The main objective was to create a modular pipeline that could:

- Continuously ingest company-related data (e.g., registration numbers, names, websites)  
- Clean and normalize key fields across different sources  
- Validate business registration numbers via the NTS API  
- Enrich the cleaned dataset with useful metadata  
- Export the final results in a structured format (CSV/Excel)

The broader purpose was to practice building practical ETL systems that deal with inconsistent real-world public data, while maintaining reliability and reusability.

---

## Key Features

- **OpenDART Ingestion**: Pulls corporate master data via OpenDART API
- **Data Preprocessing**: Cleans raw fields like company names, registration numbers, URLs, and representative names
- **Business Number Validation**: Cross-checks each registration number against the NTS API
- **Metadata Enrichment**: Adds supplementary info (e.g., derived fields, tags) to enhance usability
- **Structured Export**: Outputs final results into `.csv` and `.xlsx` formats

---

## Folder Structure

```
biznum-etl-dart/
├── README.md
├── requirements.txt
├── .gitignore
├── data/ # ETL Output Data files (sample data included)
├── src/
│ ├── config.py     # API credentials and settings
│ ├── pipeline.py   # ETL orchestrator
│ ├── collect/      # Data ingestion logic (OpenDART)
│ ├── preprocessing/  # Cleaning and normalization modules
│ ├── validate/     # Business number verification (NTS)
│ ├── transform/    # Metadata enrichment logic
│ └── export/       # Exporting results to file
└── tests/          # Unit tests for individual modules
```

---

## Quick Start

### 1. Install requirements

```bash
pip install -r requirements.txt
```

### 2. Set up API keys

- Copy `src/config.py.example` to `src/config.py` and enter your API keys:
    - `DART_API_KEY`: [Apply for OpenDART API Key](https://opendart.fss.or.kr/)
    - `NTS_API_KEY`: [Apply for Business Registration Validation API (data.go.kr)](https://www.data.go.kr/tcs/dss/selectApiDataDetailView.do?publicDataPk=15081808)
      
   ## src/config.py (replace with your real key)
    - `DART_API_KEY = "YOUR_DART_API_KEY"`
    - `NTS_API_KEY = "YOUR_NTS_API_KEY"`

- Both APIs are free to use but require registration. Approval may take 1–2 business days depending on the service.


### 3. Run the pipeline

```bash
python -m src.pipeline
```

- Results will be generated in the `data/` folder.

---

## ETL Flow Overview

1. **Collect**: Raw data saved to data/raw_dart_data.xlsx
2. **preprocessing**: Cleaned output in data/preprocessed_company_data.xlsx
3. **Validate**: Verified results in data/validated_company_data.xlsx
4. **Transform**: Metadata enriched at data/metadata_enriched_data.xlsx
5. **Export**: Final .csv saved to data/final_output.csv

---

## Example Data

- Sample processed files (100 records) are provided in `data/`.
- Actual API keys are not included for privacy.

---

## Testing

Unit tests are provided in the `tests/` directory.

Example:
`tests/test_preprocessing.py` contains test cases for homepage normalization, phone number cleanup, etc.

# Run tests

```bash
PYTHONPATH=./src pytest tests
```

## Key ETL Functions

- `collect/extract_and_save_data`: Download and save company master data
- `preprocessing/preprocessed_company_data`: Clean fields, homepage, names, etc.
- `validate/validate_biz_numbers`: Check business number validity via API
- `transform/transform_with_metadata`: Apply enrichment or mapping
- `export/export_to_csv`: Save results for downstream use

---

## Notes

- **API keys** must be set in `src/config.py`.
- This project was used to complete an assigned task during an internship at Douzone Bizon.
- This repository is for portfolio and learning purposes only.

---

## About the Author

Jung Seungil (정승일)

Email: rhjung2001@gmail.com

---

## Contact

If you have any questions, feel free to reach out my email.

---
