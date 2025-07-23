import pandas as pd

def mock_validate_biz_numbers(input_path, output_path, service_key):
    df = pd.read_excel(input_path, dtype=str)
    df['사업자등록번호 유효성'] = 1
    df.to_excel(output_path, index=False)

def test_validate_biz_numbers(tmp_path, monkeypatch):
    from validate import validator
    monkeypatch.setattr(validator, "validate_biz_numbers", mock_validate_biz_numbers)
    input_fp = tmp_path / "input.xlsx"
    output_fp = tmp_path / "output.xlsx"
    data = {
        "사업자등록번호": ["3128134722"],
        "고유번호": ["00434003"],
        "정식명칭": ["다코"],
        "사업자등록번호 유효성": [None]
    }
    pd.DataFrame(data).to_excel(input_fp, index=False)
    validator.validate_biz_numbers(input_fp, output_fp, service_key="dummy")
    out = pd.read_excel(output_fp, dtype=str)
    assert out['사업자등록번호 유효성'].iloc[0] == "1"