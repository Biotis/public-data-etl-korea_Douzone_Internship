"""
Standardize raw company data for further processing.
Homepage field is thoroughly cleaned: invalid values removed, whitespace stripped,
converted to lowercase, and common patterns like "CO.KR" are merged.
If homepage is present and does not start with http(s), "https://" is prepended.
"""

import pandas as pd
import re

def clean_homepage(x):
    """
    Clean homepage field:
    - Remove invalid/meaningless values or if Korean present.
    - Remove all spaces, convert to lowercase.
    - Merge common split patterns, e.g. "co.kr", "com", etc.
    - If not starting with http(s)://, prepend "https://".
    """
    if not x or pd.isna(x):
        return None

    s = str(x).strip()

    # Remove if contains Korean or is in invalid set
    invalid_homepage_values = {
        'no', 'none', 'na', '-', 'n/a', 'null', '_', '.', ',', 'www', 'www.', 'https://', 'http://', 'www.9'
    }
    if re.search(r'[가-힣]', s) or s.lower() in invalid_homepage_values:
        return None

    # Remove all whitespaces and convert to lowercase
    s = re.sub(r'\s+', '', s).lower()

    # Merge common split domain patterns (e.g., "dsplantco.kr" from "dsplantco.kr", or "dsplantco.kr" from "dsplantco.kr")
    # Also, join things like "dsplantco.kr" from "dsplant co. kr" or "dsplant co.kr"
    # Remove trailing dot if any
    s = s.strip('.')

    # Handle split cases like "dsplant co.kr" or "dsplant co. kr"
    # Join "co.kr", "com", "net", etc. if they are separated by space/dot
    # Patterns to join: "co.kr", "com", "net", "or.kr", "go.kr", "ac.kr", "co.jp", "co.uk" etc.
    # We'll look for endings like "co.kr", "com" etc. at the end and merge if space or dot separated
    # E.g., "dsplant co kr" -> "dsplantco.kr"
    #       "dsplant co. kr" -> "dsplantco.kr"
    s = re.sub(
        r'([a-z0-9]+)[\s\.]*(co\.kr|com|net|or\.kr|go\.kr|ac\.kr|co\.jp|co\.uk)$',
        r'\1.\2',
        s
    )

    # Remove repeating dots
    s = re.sub(r'\.{2,}', '.', s)

    # Remove leading dots
    s = s.lstrip('.')

    # Prepend protocol if not present
    if not (s.startswith('http://') or s.startswith('https://')):
        s = 'https://' + s

    return s

def standardize_company_data(input_path, output_path):
    """
    Standardize raw company data and save the cleaned file.
    Args:
        input_path (str): Path to the input Excel file.
        output_path (str): Path to save the cleaned Excel file.
    """
    df = pd.read_excel(input_path, dtype=str)
    df = df.where(pd.notnull(df), None)

    # Standardize business registration number: keep only numbers and only 10-digit ones
    df['사업자등록번호'] = df['사업자등록번호'].apply(lambda x: re.sub(r'[^0-9]', '', str(x)) if x else None)
    df = df[df['사업자등록번호'].notna() & df['사업자등록번호'].apply(lambda x: len(str(x)) == 10)].copy()

    # Homepage cleaning (using improved cleaning logic)
    df['홈페이지'] = df['홈페이지'].apply(clean_homepage)

    # Standardize corporation number: only digits, 13-digit
    df['법인등록번호'] = df['법인등록번호'].apply(lambda x: re.sub(r'[^0-9]', '', str(x)) if x else None)
    df['법인등록번호'] = df['법인등록번호'].apply(lambda x: x if x and len(str(x)) == 13 else None)

    # Standardize date fields: only digits, 8-digit
    for col in ['설립일', '최종변경일자']:
        df[col] = df[col].apply(lambda x: re.sub(r'[^0-9]', '', str(x)) if x else None)
        df[col] = df[col].apply(lambda x: x if x and len(str(x)) == 8 else None)

    # Standardize phone/fax: only digits, 9~11-digit
    for col in ['전화번호', '팩스번호']:
        df[col] = df[col].apply(lambda x: re.sub(r'[^0-9]', '', str(x)) if not pd.isna(x) else None)
        df[col] = df[col].apply(lambda x: x if x and len(str(x)) in [9, 10, 11] else None)

    # Corporate type: 4th digit in 사업자등록번호 is 8 → 0 (corporation), else 1 (individual)
    df['법인구분'] = df['사업자등록번호'].apply(lambda x: 0 if x and str(x)[3] == '8' else 1)

    # Normalize representative name
    def normalize_representative_name(name):
        if not name or pd.isna(name):
            return None
        name = re.sub(r'\(.*?\)', '', name).strip()
        name = re.sub(r'(대표이사|ceo|사장|이사|회장|대리인)', '', name, flags=re.IGNORECASE).strip()
        names = re.split(r'[,/]', name)
        clean_names = []
        for n in names:
            n = n.strip()
            if re.match(r'^[가-힣\s]+$', n):
                n = ''.join(n.split())
            clean_names.append(n)
        return ', '.join(filter(None, clean_names))
    df['대표자명'] = df['대표자명'].apply(normalize_representative_name)

    # Determine joint business owner
    def check_joint_business_owner(name):
        if not name or pd.isna(name):
            return 0
        if ',' in name:
            return 1
        parts = name.split()
        if all(re.match(r'^[A-Za-z]+$', part) for part in parts):
            return 0 if len(parts) == 2 else 1
        if re.match(r'^[가-힣]{2,4}$', name):
            return 0
        return 1 if len(parts) > 1 else 0
    df['공동사업자여부'] = df['대표자명'].apply(check_joint_business_owner)

    # Add other columns as None
    df['본지점여부'] = None
    df['본지점일괄납부여부'] = None
    df['중소기업여부'] = None
    df['사업자등록번호 유효성'] = None

    # Set column types explicitly
    df = df.astype({
        '사업자등록번호': 'string',
        '고유번호': 'string',
        '정식명칭': 'string',
        '종목코드': 'string',
        '최종변경일자': 'string',
        '업종코드': 'string',
        '영문명칭': 'string',
        '약식명칭': 'string',
        '대표자명': 'string',
        '홈페이지': 'string',
        '주소': 'string',
        '전화번호': 'string',
        '팩스번호': 'string',
        '설립일': 'string',
        '법인구분': 'string',
        '법인등록번호': 'string',
        '사업자등록번호 유효성': 'string',
        '공동사업자여부': 'Int16',
        '본지점여부': 'Int16',
        '본지점일괄납부여부': 'Int16',
        '중소기업여부': 'Int16',
        '사업자등록번호 유효성': 'Int16'
    })

    df.to_excel(output_path, index=False, engine='openpyxl')
    print(f"Cleaned data saved to {output_path}")

# Example usage:
# standardize_company_data('data/raw_dart_data.xlsx', 'data/standardized_company_data.xlsx')