"""
Validate business registration numbers using the NTS API.
"""

import pandas as pd
import requests
import json

def validate_biz_numbers(input_path, output_path, service_key):
    """
    Validate business registration numbers and update the dataframe.
    Args:
        input_path (str): Path to cleaned Excel file.
        output_path (str): Path to save validated Excel file.
        service_key (str): NTS API service key.
    """
    base_url = "https://api.odcloud.kr/api/nts-businessman/v1/status?serviceKey=" + service_key

    df = pd.read_excel(input_path, dtype={"전화번호": str, "팩스번호": str})
    df = df[df["사업자등록번호"].notna()]
    df["사업자등록번호"] = df["사업자등록번호"].astype(str).str.replace("-", "").str.zfill(10)
    df = df[df["사업자등록번호"].str.isdigit()]
    b_no_list = df["사업자등록번호"].tolist()

    batch_size = 100
    for i in range(0, len(b_no_list), batch_size):
        batch = b_no_list[i:i + batch_size]
        payload = json.dumps({"b_no": batch})
        headers = {"Content-Type": "application/json"}

        try:
            response = requests.post(
                base_url,
                data=payload,
                headers=headers,
                timeout=10
            )
            response.raise_for_status()
            result = response.json()

            if "data" not in result:
                print("No 'data' key in response:", result)
                continue

            for item in result["data"]:
                b_no = item["b_no"]
                is_valid = item.get("tax_type", "") != "국세청에 등록되지 않은 사업자등록번호입니다."
                df.loc[df["사업자등록번호"] == b_no, "사업자등록번호 유효성"] = 1 if is_valid else 0
                if not is_valid:
                    df.loc[df["사업자등록번호"] == b_no, "업종코드"] = None

        except requests.exceptions.Timeout:
            print("Request timeout.")
            continue
        except requests.exceptions.RequestException as e:
            print(f"API error: {e}")
            continue

    df.to_excel(output_path, index=False, engine="openpyxl")
    print(f"Validation results saved to {output_path}")

# Example usage:
# validate_biz_numbers('data/cleaned_company_info.xlsx', 'data/final.xlsx', 'YOUR_SERVICE_KEY')