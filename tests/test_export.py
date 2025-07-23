import pandas as pd
from export.exporter import export_to_csv

def test_export_to_csv(tmp_path):
    input_fp = tmp_path / "input.xlsx"
    output_fp = tmp_path / "output.csv"
    data = {
        "사업자등록번호": ["3128134722"],
        "고유번호": ["00434003"],
        "정식명칭": ["다코"],
    }
    pd.DataFrame(data).to_excel(input_fp, index=False)
    export_to_csv(input_fp, output_fp)
    out = pd.read_csv(output_fp, dtype=str)
    assert out['사업자등록번호'].iloc[0] == '3128134722'
    assert out['고유번호'].iloc[0] == '00434003'
    assert out['정식명칭'].iloc[0] == '다코'