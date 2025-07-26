Biznum ETL DART Pipeline

OpenDART와 국세청(NTS)의 공공 API를 활용해서, 한국 기업의 마스터 데이터를 수집하고 표준화, 검증, 변환하는 End-to-End ETL 파이프라인입니다.이 프로젝트는 더존비즈온에서 인턴으로 근무하며 진행했던 과제로, 실제 공공 데이터를 깔끔하고 일관된 형식으로 가공해 분석이나 후속 처리에 활용할 수 있도록 구성했습니다.

📌 프로젝트 목표

이 파이프라인의 목표는 다음과 같았습니다:

기업 관련 정보(사업자등록번호, 상호명, 홈페이지 등)를 자동으로 수집

서로 다른 출처의 필드를 정리하고 표준화

국세청 API를 활용해 사업자등록번호 유효성 확인

정제된 데이터에 메타데이터를 추가해서 정보 보강

최종 데이터를 구조화된 포맷(CSV, Excel)으로 내보내기

실제 환경에서 제공되는 공공 데이터를 안정적으로 처리할 수 있는 실용적인 ETL 시스템을 만들어보는 데 중점을 뒀습니다.

⚙️ 주요 기능

OpenDART 수집: OpenDART API를 통해 기업 마스터 데이터를 수집

데이터 표준화: 상호명, 사업자번호, 홈페이지 주소 등을 정제

사업자번호 검증: 국세청(NTS) API로 유효성 체크

메타데이터 보강: 파생 필드, 태그 등 추가 정보 포함

구조화된 결과물 생성: .csv, .xlsx 형태로 저장

🗂️ 폴더 구조

biznum-etl-dart/
├── README.md
├── requirements.txt
├── .gitignore
├── data/ # 입력 및 출력 데이터 저장 (샘플 포함)
├── src/
│   ├── config.py     # API 키 및 설정 파일
│   ├── pipeline.py   # 전체 파이프라인 실행 스크립트
│   ├── collect/      # OpenDART 수집 모듈
│   ├── standardize/  # 정제 및 표준화 로직
│   ├── validate/     # 국세청 API로 유효성 검증
│   ├── transform/    # 메타데이터 추가
│   └── export/       # 결과물 파일로 저장
└── tests/            # 각 모듈별 테스트 코드

🚀 빠르게 실행해보기

1. 필요한 패키지 설치

pip install -r requirements.txt

2. API 키 설정

src/config.py.example 파일을 복사해서 src/config.py로 만들고, 아래 항목에 본인의 키를 입력합니다:

DART_API_KEY: OpenDART 키 신청

NTS_API_KEY: 사업자등록 유효성 검증 API 신청 (data.go.kr)

# src/config.py 예시
DART_API_KEY = "YOUR_DART_API_KEY"
NTS_API_KEY = "YOUR_NTS_API_KEY"

💡 두 API 모두 무료지만, 승인까지 1~2일 정도 걸릴 수 있습니다.

3. 파이프라인 실행

python -m src.pipeline

실행 결과는 data/ 폴더에 생성됩니다.

🔄 ETL 흐름 요약

Collect: 원시 데이터 → data/raw_dart_data.xlsx

Standardize: 정제된 데이터 → data/standardized_company_data.xlsx

Validate: 검증된 데이터 → data/validated_company_data.xlsx

Transform: 메타데이터 포함 데이터 → data/metadata_enriched_data.xlsx

Export: 최종 .csv → data/final_output.csv

🧹 예제 데이터

data/ 폴더에 샘플 처리 데이터(100건 기준)가 들어 있습니다.

실제 API 키와 실데이터는 포함되어 있지 않습니다.

🤮 테스트

각 모듈별로 단위 테스트 코드를 tests/ 폴더에 작성해두었습니다.

예시:
tests/test_standardize.py → 홈페이지 정제, 기업명 정리 테스트 포함

테스트 실행

PYTHONPATH=./src pytest tests

💡 주요 ETL 함수 정리

collect/extract_and_save_data: 기업 데이터 수집 및 저장

standardize/standardize_company_data: 기업명, 홈페이지, 등록번호 정제

validate/validate_biz_numbers: 사업자번호 유효성 확인

transform/transform_with_metadata: 메타정보 추가 처리

export/export_to_csv: 최종 데이터 .csv 저장

📝 기타 참고 사항

API 키는 src/config.py에 직접 입력해야 합니다

.gitignore에 의해 중간 파일과 결과물은 깃에 올라가지 않습니다

더존비즈온 인턴십 기간 중 수행했던 과제를 기반으로 만들었습니다

🤖 작성자 소개

정승일 (Jung Seungil)데이터 엔지니어링 인턴 @ 더존비즈온

GitHub: github.com/Biotis

Email: rhjung2001@gmail.com

⚠️ 참고 및 주의

이 저장소는 포트폴리오 및 개인 학습 목적의 예시로 공개된 것입니다.

📬 Contact

채용 또는 협업 제안은 GitHub 또는 이메일로 편하게 연락 주세요.

