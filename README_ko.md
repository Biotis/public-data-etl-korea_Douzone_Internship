# 📊 Biznum ETL DART Pipeline

한국 기업의 마스터 데이터를 수집, 정제, 검증, 변환하는 **End-to-End ETL 파이프라인**입니다.  
OpenDART 및 국세청(NTS)의 공공 API를 활용해 구축되었으며, 더존비즈온에서의 데이터 엔지니어링 인턴십 중 수행한 프로젝트입니다.

이 파이프라인은 현실 세계의 공공 데이터를 일관된 포맷으로 정리하여 **분석과 후속 활용이 가능한 구조화된 데이터셋**으로 변환하는 데 목적이 있습니다.

---

## 📌 프로젝트 목표

이 프로젝트는 다음과 같은 기능을 갖춘 **모듈형 ETL 시스템**을 만드는 데 중점을 두었습니다:

- 기업 관련 데이터 (사업자등록번호, 회사명, 홈페이지 주소 등) **지속적 수집**
- 출처별로 상이한 필드 값 **정리 및 표준화**
- 국세청 API를 통해 **사업자등록번호 유효성 검증**
- **메타데이터 추가**를 통해 활용성 향상
- **CSV / Excel 형식의 구조화된 결과물 생성**

> ✅ 목표는 **비정형적이고 불완전한 공공 데이터를 신뢰할 수 있는 형태로 전환**하는 실용적인 ETL 시스템 구축입니다.

---

## ⚙️ 주요 기능

| 기능 | 설명 |
|------|------|
| 🏢 **OpenDART 수집** | OpenDART API로 기업 마스터 데이터를 수집합니다. |
| 🧼 **데이터 표준화** | 회사명, 등록번호, 홈페이지 주소, 대표자명 등의 필드를 정제합니다. |
| ✅ **사업자번호 검증** | 국세청 API를 통해 등록번호의 유효성을 확인합니다. |
| 🧠 **메타데이터 추가** | 태그 및 파생 필드 등을 추가하여 활용도를 높입니다. |
| 📤 **구조화된 내보내기** | 최종 결과를 `.csv`, `.xlsx` 형식으로 저장합니다. |

---

## 🗂️ 폴더 구조

biznum-etl-dart/
├── README.md
├── requirements.txt
├── .gitignore
├── data/ # 입력 및 출력 파일 (샘플 포함)
├── src/
│ ├── config.py # API 키 및 설정
│ ├── pipeline.py # 전체 ETL 실행 스크립트
│ ├── collect/ # OpenDART 수집 모듈
│ ├── standardize/ # 데이터 정제 및 표준화
│ ├── validate/ # 사업자번호 검증
│ ├── transform/ # 메타데이터 추가
│ └── export/ # 최종 결과물 저장
└── tests/ # 유닛 테스트

yaml
복사
편집

---

## 🚀 빠른 시작

### 1. 라이브러리 설치

```bash
pip install -r requirements.txt
2. API 키 설정
bash
# 설정 파일 복사 후 편집
cp src/config.py.example src/config.py
python
# src/config.py 예시
DART_API_KEY = "YOUR_DART_API_KEY"
NTS_API_KEY = "YOUR_NTS_API_KEY"
🔑 OpenDART API 키 신청

🔑 국세청 사업자등록번호 검증 API 신청 (data.go.kr)

💡 두 API 모두 무료로 제공되며, 승인까지 1~2 영업일이 소요될 수 있습니다.

3. 파이프라인 실행
bash
python -m src.pipeline
결과물은 data/ 폴더에 저장됩니다.

🔄 ETL 흐름 요약
단계	설명	출력 파일
Collect	기업 원시 데이터 수집	data/raw_dart_data.xlsx
Standardize	필드 정제 및 표준화	data/standardized_company_data.xlsx
Validate	사업자번호 검증	data/validated_company_data.xlsx
Transform	메타데이터 추가	data/metadata_enriched_data.xlsx
Export	최종 데이터 저장	data/final_output.csv

🧪 테스트
단위 테스트는 tests/ 디렉토리에 구성되어 있습니다.

예시:

tests/test_standardize.py: 홈페이지 URL 정규화, 이름 클렌징 등

bash
복사
편집
PYTHONPATH=./src pytest tests
📁 샘플 데이터
data/ 폴더에는 100개 기업의 샘플 처리 결과가 포함되어 있습니다.

실제 API 키 및 민감한 데이터는 포함되어 있지 않습니다.

💡 주요 함수 요약
경로	설명
collect/extract_and_save_data	기업 마스터 데이터 수집 및 저장
standardize/standardize_company_data	필드 정리, 홈페이지/이름 표준화
validate/validate_biz_numbers	사업자등록번호 API 검증
transform/transform_with_metadata	태그, 파생 필드 등 추가
export/export_to_csv	최종 결과 CSV 저장

📝 참고 사항
API 키는 src/config.py에 직접 설정해야 합니다.

.gitignore에는 중간 처리 결과와 민감 데이터가 포함되어 있습니다.

이 프로젝트는 더존비즈온 인턴십 과제로 진행되었습니다.

👨‍💻 작성자
정승일 (Jung Seungil)
데이터 엔지니어링 인턴 @ Douzone Bizon

GitHub: github.com/Biotis

Email: rhjung2001@gmail.com

⚠️ 디스클레이머
이 저장소는 포트폴리오 및 학습 목적으로 제작되었습니다.
실제 서비스 운영용으로 사용하기 전에는 검토 및 검증이 필요합니다.

📬 연락하기
채용, 협업, 코드 리뷰 목적 등으로 프로젝트를 검토하신다면
아래 이메일 또는 GitHub 이슈를 통해 자유롭게 연락 주세요.

📮 rhjung2001@gmail.com
🌐 github.com/Biotis
