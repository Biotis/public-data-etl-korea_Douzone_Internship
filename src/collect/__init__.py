"""
collect 패키지: 데이터 수집(ingest) 관련 모듈을 포함합니다.
예시: OpenDART 등 외부 API에서 기업 데이터를 수집하는 기능 제공.
"""
# dart_collector 모듈의 주요 함수 임포트
from .dart_collector import get_corp_codes, get_company_info, extract_and_save_data

__all__ = [
    "get_corp_codes",
    "get_company_info",
    "extract_and_save_data",
]