"""
Validate business registration numbers using the NTS API.
"""

import pandas as pd
import requests
import json
import time

def validate_biz_numbers(input_path, output_path, service_key):
    """
    Validate business registration numbers and update the dataframe.
    Args:
        input_path (str): Path to cleaned Excel file.
        output_path (str): Path to save validated Excel file.
        service_key (str): NTS API service key.
    """
    base_url = f"https://api.odcloud.kr/api/nts-businessman/v1/status?serviceKey={service_key}"

    df = pd.read_excel(input_path, dtype={"전화번호": str, "팩스번호": str})
    df = df[df["사업자등록번호"].notna()]
    df["사업자등록번호"] = df["사업자등록번호"].astype(str).str.replace("-", "").str.zfill(10)
    df = df[df["사업자등록번호"].str.isdigit()]
    b_no_list = df["사업자등록번호"].tolist()

    batch_size = 100
    max_retries = 3
    failed_batches = []

    for i in range(0, len(b_no_list), batch_size):
        batch = b_no_list[i:i + batch_size]
        payload = json.dumps({"b_no": batch})
        headers = {"Content-Type": "application/json"}

        for attempt in range(1, max_retries + 1):
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
                    print(f"[경고] 응답에 'data' 키 없음 (batch {i}-{i + batch_size})")
                    failed_batches.append(batch)
                    break

                for item in result["data"]:
                    b_no = item["b_no"]
                    is_valid = item.get("tax_type", "") != "국세청에 등록되지 않은 사업자등록번호입니다."
                    df.loc[df["사업자등록번호"] == b_no, "사업자등록번호 유효성"] = 1 if is_valid else 0
                    if not is_valid:
                        df.loc[df["사업자등록번호"] == b_no, "업종코드"] = None

                time.sleep(0.5)  # 요청 간 딜레이
                break  # 성공했으면 retry loop 탈출

            except requests.exceptions.Timeout:
                print(f"[재시도 {attempt}/{max_retries}] 요청 시간 초과 (batch {i}-{i + batch_size})")
                time.sleep(1)
            except requests.exceptions.RequestException as e:
                print(f"[재시도 {attempt}/{max_retries}] API 오류: {e}")
                time.sleep(1)
        else:
            # 재시도 모두 실패
            print(f"[오류] 요청 실패: batch {i}-{i + batch_size} → 로그 저장")
            failed_batches.append(batch)

    # 실패한 배치 로그 저장
    if failed_batches:
        with open("failed_batches.log", "a", encoding="utf-8") as log_file:
            for batch in failed_batches:
                log_file.write(f"Failed batch: {batch}\n")
        print(f"[완료] 실패한 요청 {len(failed_batches)}건 → failed_batches.log에 기록됨")

    # 최종 저장
    df.to_excel(output_path, index=False, engine="openpyxl")
    print(f"Validation results saved to {output_path}")

# Example usage:
# validate_biz_numbers('data/cleaned_company_info.xlsx', 'data/final_validated.xlsx', 'YOUR_SERVICE_KEY')
