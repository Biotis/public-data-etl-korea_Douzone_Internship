import pandas as pd
from standardize.standardizer import standardize_company_data

def test_standardization_basic(tmp_path):
    df = pd.DataFrame({
        '고유번호': ['00434003'],
        '정식명칭': ['다코'],
        '종목코드': [None],
        '최종변경일자': ['20170630'],
        '업종코드': ['25931'],
        '영문명칭': ['Daco corporation'],
        '약식명칭': ['다코'],
        '대표자명': ['김상규'],
        '홈페이지': ['DSPLANT CO. KR'],
        '주소': ['충청남도 천안시 청당동 419-12'],
        '전화번호': ['041-565-1800'],
        '팩스번호': ['041-563-6808'],
        '설립일': ['19970611'],
        '사업자등록번호': ['3128134722'],
        '법인구분': ['E'],
        '법인등록번호': ['1615110021778']
    })
    # 모든 문자열 컬럼을 명시적으로 str로 변환
    for col in ['고유번호', '전화번호', '팩스번호', '사업자등록번호', '법인등록번호']:
        df[col] = df[col].astype(str)
    input_fp = tmp_path / "input.xlsx"
    output_fp = tmp_path / "output.xlsx"
    df.to_excel(input_fp, index=False)
    standardize_company_data(input_fp, output_fp)
    out = pd.read_excel(output_fp, dtype=str)
    assert out['홈페이지'].iloc[0] == "https://dsplant.co.kr"
    assert str(out['사업자등록번호'].iloc[0]).isdigit() and len(str(out['사업자등록번호'].iloc[0])) == 10
    assert out['전화번호'].iloc[0] == '0415651800'
    assert out['설립일'].iloc[0] == '19970611'
    assert str(out['법인등록번호'].iloc[0]).isdigit() and len(str(out['법인등록번호'].iloc[0])) == 13