"""
validate 패키지: 데이터 유효성 검사(Validation) 관련 모듈을 포함합니다.
예시: 사업자등록번호 등 외부 API 검증.
"""
from .validator import validate_biz_numbers

__all__ = [
    "validate_biz_numbers"
]