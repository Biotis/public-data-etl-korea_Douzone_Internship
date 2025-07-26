"""
Main pipeline script to process business registration master data.
"""

# config에서 API키 등 환경설정 가져오기
from src.config import DART_API_KEY, NTS_API_KEY, DATA_PATH, BATCH_SIZE

from src.collect.dart_collector import extract_and_save_data
from src.proprecessing.proprecessed import standardize_company_data
from src.validate.validator import validate_biz_numbers
from src.transform.transformer import transform_with_metadata
from src.export.exporter import export_to_csv

def main():
    # 1. Data Collection
    extract_and_save_data(
        api_key=DART_API_KEY, 
        start_index=0, 
        end_index=BATCH_SIZE, 
        filename=f"{DATA_PATH}raw_dart_data.xlsx"
    )
    
    # 2. Standardization
    standardize_company_data(
        f"{DATA_PATH}raw_dart_data.xlsx", 
        f"{DATA_PATH}proprecessed_company_data.xlsx"
    )
    
    # 3. Validation
    validate_biz_numbers(
        f"{DATA_PATH}proprecessed_company_data.xlsx", 
        f"{DATA_PATH}validated_company_data.xlsx", 
        NTS_API_KEY
    )
    
    # 4. Transformation
    transform_with_metadata(
        f"{DATA_PATH}validated_company_data.xlsx", 
        f"{DATA_PATH}metadata_enriched_data.xlsx"
    )
    
    # 5. Export
    export_to_csv(
        f"{DATA_PATH}metadata_enriched_data.xlsx", 
        f"{DATA_PATH}final_output.csv"
    )

if __name__ == "__main__":
    main()