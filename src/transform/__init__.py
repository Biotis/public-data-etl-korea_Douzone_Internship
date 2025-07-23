"""
transform 패키지: 데이터 통합/형 변환 및 마스터 테이블 구조 변환을 담당합니다.
예시: 메타 테이블 변환, 컬럼 매핑, 타입 변환 등.
"""
from .transformer import transform_with_metadata

__all__ = [
    "transform_with_metadata"
]