"""
Module for collecting company data from OpenDART API.
"""

import requests
import xmltodict
import pandas as pd
import zipfile
import io
import os

def get_corp_codes(api_key: str):
    """
    Download and parse the corpCode.xml file from OpenDART API.
    Args:
        api_key (str): OpenDART API key.
    Returns:
        list: List of company information dictionaries.
    """
    url = f"https://opendart.fss.or.kr/api/corpCode.xml?crtfc_key={api_key}"
    response = requests.get(url)
    response.raise_for_status()

    with zipfile.ZipFile(io.BytesIO(response.content)) as zf:
        with zf.open('CORPCODE.xml') as xml_file:
            xml_content = xml_file.read().decode('utf-8')
            data = xmltodict.parse(xml_content)
    return data['result']['list']

def get_company_info(api_key: str, corp_code: str):
    """
    Extract key company information from the company.xml file.
    Args:
        api_key (str): OpenDART API key
        corp_code (str): Company unique code
    Returns:
        dict: Company info
    """
    url = f"https://opendart.fss.or.kr/api/company.xml?crtfc_key={api_key}&corp_code={corp_code}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        xml_data = xmltodict.parse(response.content)
        return {
            'induty_code': xml_data['result'].get('induty_code'),
            'corp_name_eng': xml_data['result'].get('corp_name_eng'),
            'stock_name': xml_data['result'].get('stock_name'),
            'ceo_nm': xml_data['result'].get('ceo_nm'),
            'hm_url': xml_data['result'].get('hm_url'),
            'adres': xml_data['result'].get('adres'),
            'phn_no': xml_data['result'].get('phn_no'),
            'fax_no': xml_data['result'].get('fax_no'),
            'est_dt': xml_data['result'].get('est_dt'),
            'bizr_no': xml_data['result'].get('bizr_no'),
            'corp_cls': xml_data['result'].get('corp_cls'),
            'jurir_no': xml_data['result'].get('jurir_no')
        }
    except Exception as e:
        print(f"Error fetching company info for {corp_code}: {e}")
        return None

def extract_and_save_data(api_key: str, start_index: int, end_index: int, filename: str = "company_info.csv"):
    """
    Extracts a range of company info and saves to a CSV file.
    """
    corp_codes = get_corp_codes(api_key)
    data_list = []

    for index, company in enumerate(corp_codes[start_index:end_index], start=start_index):
        try:
            corp_code = company['corp_code']
            corp_name = company['corp_name']
            stock_code = company['stock_code']
            modify_date = company['modify_date']

            company_info = get_company_info(api_key, corp_code)
            if company_info:
                data_list.append({
                    '고유번호': corp_code,
                    '정식명칭': corp_name,
                    '종목코드': stock_code,
                    '최종변경일자': modify_date,
                    '업종코드': company_info['induty_code'],
                    '영문명칭': company_info['corp_name_eng'],
                    '약식명칭': company_info['stock_name'],
                    '대표자명': company_info['ceo_nm'],
                    '홈페이지': company_info['hm_url'],
                    '주소': company_info['adres'],
                    '전화번호': company_info['phn_no'],
                    '팩스번호': company_info['fax_no'],
                    '설립일': company_info['est_dt'],
                    '사업자등록번호': company_info['bizr_no'],
                    '법인구분': company_info['corp_cls'],
                    '법인등록번호': company_info['jurir_no']
                })
        except Exception as e:
            print(f"Error processing company {index}: {e}")

    df = pd.DataFrame(data_list)
    # df.to_csv(filename, index=False, encoding='utf-8-sig')
    df.to_excel(filename, index=False, engine='openpyxl')
    print(f"Saved to {filename}")

# Example usage (remove or comment out in production)
# extract_and_save_data(api_key="YOUR_DART_API_KEY", start_index=0, end_index=10, filename="company_info_sample.csv")