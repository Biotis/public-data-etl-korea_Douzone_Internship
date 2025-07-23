"""
Transform company data to a master table with metadata per row (column mapping, type, constraint, etc.).
"""

import pandas as pd

def convert_data(value, data_type, default):
    """
    Convert value based on the expected data type and default.
    """
    if pd.isna(value) or value is None:
        return default

    if 'VARCHAR' in data_type or 'CHAR' in data_type:
        max_length = int(data_type.split('(')[1].rstrip(')'))
        return str(value)[:max_length]

    if 'SMALLINT' in data_type:
        try:
            int_value = int(value)
            return int_value if int_value in [0, 1] else default
        except ValueError:
            return default

    if data_type == 'VARCHAR(8)':
        return value if len(value) == 8 and value.isdigit() else default

    return value

def transform_with_metadata(input_file, output_file):
    """
    Transform validated data to a metadata-rich master table.
    Each row describes a (column, value, type, constraint, etc.) for a company.
    """
    df = pd.read_excel(input_file, dtype=str)

    column_mapping = {
        '사업자등록번호': 'BIZRGNO',
        '고유번호': 'UNIQNO',
        '정식명칭': 'OFCLNM',
        '종목코드': 'ITMCD',
        '최종변경일자': 'LASTCHGDT',
        '업종코드': 'INDCD',
        '영문명칭': 'ENGABBR',
        '약식명칭': 'SHTNM',
        '대표자명': 'RPRSNTNM',
        '홈페이지': 'HMPG',
        '중소기업여부': 'SMBIZ_YN',
        '본지점여부': 'MAIN_BRCH_YN',
        '본지점일괄납부여부': 'MAIN_BRCH_PCKG_PYMNT_YN',
        '주소': 'ADDR',
        '전화번호': 'TELNO',
        '팩스번호': 'FAXNO',
        '설립일': 'ESTDT',
        '법인구분': 'CRPTP',
        '법인등록번호': 'CRPTNO',
        '사업자등록번호 유효성': 'BIZRGNO_VALID'
    }

    metadata = {
        '사업자등록번호': ('VARCHAR(10)', None, "1. 10자리여야 함.\n2. 유효성 검사 통과 여부 확인.", 'DART', '국세청 기준 사업자 등록 번호', ''),
        '고유번호': ('VARCHAR(20)', None, "1. 6자리인지 검사\n2. 유효성 검사 실패시 NULL", 'DART', '회사의 고유 번호', ''),
        '정식명칭': ('VARCHAR(100)', None, "1. 빈 값이 아니어야 함.", 'DART', '회사의 정식 명칭', ''),
        '종목코드': ('CHAR(6)', None, "1. 6자리, 영문+숫자 조합.", 'DART', '주식 시장에서의 종목 코드', ''),
        '최종변경일자': ('VARCHAR(8)', None, "1. 날짜 형식(YYYYMMDD)", 'DART', '정보의 최종 변경일', ''),
        '업종코드': ('VARCHAR(10)', None, "1. 10자리 이하, 영문+숫자", 'DART', '국세청 기준 업종 코드', ''),
        '영문명칭': ('VARCHAR(50)', None, "1. 영문 대문자+숫자", 'DART', '회사의 영문 약칭', ''),
        '약식명칭': ('VARCHAR(50)', None, "", 'DART', '회사의 약칭', ''),
        '대표자명': ('VARCHAR(20)', None, "1. 빈 값이 아니어야 함.", 'DART', '회사의 대표자 이름', ''),
        '중소기업여부': ('SMALLINT', None, "1. 0,1이 아닌경우 제외", '', '중소기업, 대기업 구분', '0: 중소기업, 1: 대기업'),
        '본지점여부': ('SMALLINT', None, "1. 0,1이 아닌경우 제외", '', '본점, 지점 구분', '0: 본점, 1: 지점'),
        '본지점일괄납부여부': ('SMALLINT', None, "1. 0,1이 아닌경우 제외", '', '본점에서 일괄납부 여부', '0: 미승인, 1: 승인'),
        '홈페이지': ('VARCHAR(100)', None, "1. URL 형식", 'DART', '회사의 홈페이지 주소', ''),
        '주소': ('VARCHAR(200)', None, "1. 빈 값이 아니어야 함.", 'DART', '회사의 주소', ''),
        '전화번호': ('VARCHAR(15)', None, "", 'DART', '회사의 전화번호', ''),
        '팩스번호': ('VARCHAR(15)', None, "", 'DART', '회사의 팩스번호', ''),
        '설립일': ('VARCHAR(8)', None, "1. 날짜 형식(YYYYMMDD)", 'DART', '회사의 설립일', ''),
        '법인구분': ('VARCHAR(1)', 0, "1. 0(법인), 1(개인)", '', '법인사업자 개인사업자 구분', '0: 법인, 1: 개인'),
        '법인등록번호': ('VARCHAR(20)', None, "1. 13자리 숫자", 'DART', '법인 등록 번호', ''),
        '사업자등록번호 유효성': ('VARCHAR(1)', None, "", '', '사업자 등록 번호의 유효성 여부', '1: 정상, 0: 비정상')
    }

    rows = []
    for _, company in df.iterrows():
        sequence_number = 1
        for logical_col, physical_col in column_mapping.items():
            data_type, default, constraint, source, description, code_table = metadata.get(logical_col, ('VARCHAR(50)', None, '', '', '', ''))
            value = company.get(logical_col, default)
            # Apply transformation logic
            transformed_value = convert_data(value, data_type, default)
            # Correction for corporation type
            if logical_col == '법인구분':
                bizrgno = str(company.get('사업자등록번호', ''))
                transformed_value = 0 if len(bizrgno) >= 4 and bizrgno[3] == '8' else 1

            rows.append({
                '순번': sequence_number,
                '논리컬럼명': logical_col,
                '물리컬럼명': physical_col,
                '데이터': transformed_value,
                '데이터 타입': data_type,
                '기본값': default,
                '제한조건': constraint,
                '데이터 소스': source,
                '컬럼설명': description,
                '코드 테이블': code_table
            })
            sequence_number += 1

        # Determine if it's a joint business
        rep_names = company.get('대표자명', '')
        is_cprtn = 1 if isinstance(rep_names, str) and len(rep_names.split(',')) >= 2 else 0
        rows.append({
            '순번': sequence_number,
            '논리컬럼명': '공동사업자여부',
            '물리컬럼명': 'CPRTN_PLCBIZ_YN',
            '데이터': is_cprtn,
            '데이터 타입': 'SMALLINT',
            '기본값': 0,
            '제한조건': "1. 0,1이 아닌 경우 제외",
            '데이터 소스': '',
            '컬럼설명': '개별사업장, 공동사업장 구분',
            '코드 테이블': '0: 개별사업자, 1: 공동사업자'
        })
        sequence_number += 1

        # Empty row for separation
        rows.append({col: '' for col in [
            '순번', '논리컬럼명', '물리컬럼명', '데이터', '데이터 타입', '기본값', '제한조건', '데이터 소스', '컬럼설명', '코드 테이블'
        ]})

    new_df = pd.DataFrame(rows)
    new_df.to_excel(output_file, index=False, engine="openpyxl")
    print(f"Metadata-rich master table saved to {output_file}")

# Example usage:
# transform_with_metadata('data/final.xlsx', 'data/Transformed_Data.xlsx')