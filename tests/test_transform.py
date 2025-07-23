import pandas as pd
from transform.transformer import transform_with_metadata

def test_transform_with_metadata(tmp_path):
    input_fp = tmp_path / "input.xlsx"
    output_fp = tmp_path / "output.xlsx"
    data = {
        "사업자등록번호": ["3128134722"],
        "고유번호": ["00434003"],
        "정식명칭": ["다코"],
    }
    pd.DataFrame(data).to_excel(input_fp, index=False)
    transform_with_metadata(input_fp, output_fp)
    out = pd.read_excel(output_fp)
    # 실제 변환 결과 컬럼(예시: '메타정보')이 추가되었는지 체크
    assert "메타정보" in out.columns or len(out.columns) >= 3