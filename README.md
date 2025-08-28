# LLM-RAG Workout Assistant (Streamlit)
로컬에선 **Ollama + EEVE-Korean**, 배포는 **Azure**(예정) 기준입니다.

---

## \[ About ]

**시니어를 위한 LLM-RAG 기반 운동 자세 추천 & Q\&A 어시스턴트**

* 사용자가 입력한 조건을 바탕으로 **맞춤 운동 루틴**을 생성합니다.
* 운동 방법 매뉴얼(헬스경향,헬스조선, 국민체력100 등), 운동 프로그램 데이터(공공데이터포털)를 **FAISS 벡터 검색**으로 참조해 **증거 기반 답변**을 제공합니다.
* 한국어 대화를 기본으로 하며, **Streamlit** UI로 쉽게 실행/배포할 수 있습니다.

> 본 레포는 LangServe/Streamlit 예제를 확장하여 **로컬(LangChain+Ollama)** → **클라우드(Azure)** 전환을 목표로 합니다.

---

## \[ Intention ]

* **신뢰 가능한 운동 정보** 제공(문서 근거 + LLM 생성)
* **개인화 루틴** 자동 설계(운동 수준, 장비, 시간 제약 고려)
* **간단한 UI**로 누구나 바로 활용

---

## \[ Benefit ]

* 루틴 설계 시간 절약, **초보 진입장벽** 낮춤
* **문서 근거**로 답변 출처 확인 가능(“환자 교육 자료”, “헬스장 매뉴얼”)
* 운동 기록·진도 기반 **점진적 과부하(Progressive Overload)** 가이드(추가 예정)

---

## \[ Development period ]

* 2025-08 \~ (진행 중)
* V1: 로컬 실행/간단 RAG → V2: Azure 컨테이너 배포/로그인/DB 연동(예정)

---

## \[ Technical Skills ]

**Programming / Frameworks**
* Python, Streamlit, LangChain, FAISS, Ollama(로컬 LLM), (예정) Azure OpenAI

**Models & Embeddings**
* Chat: **EEVE-Korean-10.8B** (로컬) → (예정) Azure 관리형 LLM
* Embeddings: **BAAI/bge-m3**

**Infra / DB**

* Azure Container Apps / App Service, Azure CLI
* (예정) PostgreSQL / Supabase (사용자·세션·즐겨찾기 루틴 저장)

**Tools**
* VS Code, GitHub Actions, Docker

---

## \[ Tech Flow ]

* **RAG (Retrieval-Augmented Generation)**

  1. 문서 업로드 → 텍스트 청크 분할 → **FAISS** 인덱싱
  2. 질문 시 **유사 문서 검색** → 컨텍스트와 함께 LLM 프롬프트 구성
  3. **한국어 답변** + **참조 문서 스니펫** 반환

* **Workout Planner**

  * 목표/부위/장비/시간 입력 → 템플릿 프롬프트 → 세트·횟수·휴식 포함 루틴 제안
  * (예정) 사용자 기록 기반 강도/볼륨 조정

* **LangServe/Streamlit App**

  * 사이드바: 문서 업로드, 임베딩 생성/리셋
  * 메인: 채팅, 루틴 생성, 근거 문서 토글 표시
  * (예정) 로그인/개인화 저장

### 아키텍처(개요)

```
[사용자 브라우저]
      │  (HTTP)
      ▼
[Streamlit UI (app/main.py)]  ── 사이드바 업로드/설정, 채팅 입력/렌더
      │
      ├─(데이터 로드) core/retriever.load_datasets() → data/*.csv, *.npy
      ├─(파일 업로드) utils/data_loader.embed_file()
      │       └─ UnstructuredFileLoader → TextSplitter → bge-m3 임베딩 → FAISS
      ├─(프롬프트) core/prompt_builder.AdvancedPromptBuilder
      ▼
[RAG 체인] (선택된 데이터셋/업로드 리트리버 → 컨텍스트 구성)
      ▼
[LLM]
  ├─ (로컬) Ollama eeve-korean-10-8b @ $OLLAMA_BASE_URL
  └─ (예정) Azure OpenAI 등 관리형 LLM
      ▼
[응답 렌더] (한국어 답변 + 근거 문서 스니펫/지표)
```

핵심 포인트

- 업로드 문서는 캐시 디렉터리(`./cache`, `./.cache/embeddings`)에 보관되어 재임베딩 비용 절감
- 임베딩: `BAAI/bge-m3`, 벡터 저장: `FAISS`
- LLM은 실행 환경에 따라 로컬(Ollama) 또는 클라우드(Azure)로 스위치

### 배포 아키텍처(Azure)

```
[Internet]
   │
   ▼
[Azure Container Apps Ingress]
   │  (TLS/HTTP)
   ▼
[컨테이너: Streamlit + App]
   - 포트: 8501 (ENV: PORT=8501)
   - ENV: OLLAMA_BASE_URL= 외부 Ollama 또는
          (전환) MODEL_PROVIDER=azure_openai 등
   - 이미지: ACR 빌드 (Dockerfile)
   │
   ├─ data/: 내장 샘플 CSV/NPY (필요 시 볼륨/스토리지 연동)
   └─ 로그/메트릭: (선택) Azure Monitor/Log Analytics
```

메모

- App Service 대안 사용 시 `WEBSITES_PORT=8501` 설정 필요
- Azure OpenAI 전환 시 엔드포인트/키 ENV 추가(`AZURE_OPENAI_ENDPOINT`, `AZURE_OPENAI_API_KEY` 등)

### 폴더 구조 및 정리(실행 기준)

```
Langserve-ollama/
  ├─ app/
  │   ├─ main.py                # Streamlit 엔트리(실행 파일)
  │   ├─ core/                  # 프롬프트/리트리버 로직
  │   ├─ ui/                    # 스타일/컴포넌트
  │   └─ utils/
  │       ├─ helpers.py
  │       └─ data_loader.py     # embed_file 등 업로드/임베딩 유틸
  ├─ data/                      # 샘플 데이터(text_ex.csv, full_data_ex.csv, embeddings_ex.npy)
  ├─ Dockerfile
  └─ startup.sh

(정리 사항)
- `app/utils/data_loader.py`로 `embed_file` 이동, `main.py`에서 임포트해 사용
- 미사용 파일 정리: `app/main copy.py`, `app/api.py` 제거
- 루트의 `app/` 디렉터리 삭제됨(실행 경로 혼동 방지)
```

---

## \[ Role ] (본인 기여)
* **RAG 파이프라인 설계**: 청크/임베딩/인덱싱/검색 파라미터 튜닝
* **LLM 프롬프트 엔지니어링**: 루틴 출력 포맷(표/JSON)과 안전가드
* **Streamlit UI/상태관리**: 업로드→인덱싱→질의까지 UX 플로우 구현
* **배포 설계**: 로컬 Ollama → **Azure Container Apps** 전환 스크립트 작성

---

## \[ Feature Implementation ]

* 문서 기반 Q\&A: PDF 업로드 후 **근거 문서 하이라이트**와 함께 답변
* 루틴 생성: 4지표(목표/부위/장비/시간)로 **표형식 루틴** 자동 생성
* 한국어 최적화: **EEVE-Korean** 로컬 모델로 빠른 응답
* (예정) 사용자 로그인/기록 DB, **TTS/STT** 안내 음성, **이모티콘/모션 그래픽** 프롬프트 생성

---

## \[ How To Use ]

### 1) 로컬 실행

```bash
# 0) 위치: 이 README가 있는 폴더(= Langserve-ollama)
cd Langserve-ollama

# 1) Python 3.10 권장, 가상환경(선택)
python3 -m venv ../venv && source ../venv/bin/activate

# 2) 의존성 설치
pip install -r requirements.txt

# 3) (선택) 로컬 Ollama 서버 URL 지정
export OLLAMA_BASE_URL="http://localhost:11434"

# 4) 앱 실행
streamlit run app/main.py
```

* 사이드바에서 문서 업로드 → **Index** 클릭(FAISS 생성)
* 채팅창에 “가슴 + 어깨 루틴 45분, 덤벨만” 같은 프롬프트 입력
* 답변 하단의 **References**에서 참조 문서 확인

### 2) Vercel (개발 테스트)

Vercel 무료 플랜 제약(장기 연결/외부 호스트 제한)으로 **프로덕션 비권장**.
개발용 배포만 사용하며, **Azure** 전환을 진행 중입니다.

---

## \[ Azure Deployment ]

### 컨테이너 빌드/푸시 (ACR 원격 빌드)

```bash
RG=rag-rg
LOC=koreacentral
ACR=ragacr$RANDOM
IMAGE=llm-rag-workout:latest

az group create -n $RG -l $LOC
az acr create -n $ACR -g $RG --sku Basic
ACR_LOGIN_SERVER=$(az acr show -n $ACR -g $RG --query loginServer -o tsv)
az acr build -r $ACR -g $RG -t $IMAGE -f Langserve-ollama/Dockerfile .
```

### Azure Container Apps

```bash
ENV_NAME=rag-env
APP_NAME=rag-app

az extension add -n containerapp --upgrade
az containerapp env create -g $RG -l $LOC -n $ENV_NAME
az containerapp create \
  -g $RG -n $APP_NAME \
  --environment $ENV_NAME \
  --image ${ACR_LOGIN_SERVER}/${IMAGE} \
  --ingress external --target-port 8501 \
  --registry-server ${ACR_LOGIN_SERVER} \
  --env-vars OLLAMA_BASE_URL="https://your-ngrok-url.ngrok-free.app"
```

> **App Service 대안**도 가능: `WEBSITES_PORT=8501` 설정 필수, 시작 커맨드로 `streamlit run app/main.py --server.port=8501 --server.address=0.0.0.0`.

---

## \[ Problem & Solution ]

* **문제**: Vercel 무료 플랜에서 **장기 실행·외부 호스트 연결** 제약으로 불안정
  **해결**: 컨테이너화 후 **Azure Container Apps**로 전환(인그레스/오토스케일/환경변수 관리 용이)

* **문제**: 로컬 LLM(Ollama) 의존 → 서버에서 접근 어려움
  **해결**: 배포 단계에선 **Azure OpenAI/서버형 LLM**으로 **프로바이더 스위치**(코드의 LLM 클라이언트 추상화)

---

## \[ Key Code ] (요약 스니펫)

**임베딩 & 색인 (FAISS)**

```python
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import UnstructuredFileLoader

loader = UnstructuredFileLoader(path)
docs = loader.load_and_split(text_splitter=RecursiveCharacterTextSplitter(
    chunk_size=500, chunk_overlap=50
))
emb = HuggingFaceEmbeddings(model_name="BAAI/bge-m3")
vs = FAISS.from_documents(docs, emb)
```

**질의 응답 (RAG)**

```python
from langchain_community.llms import Ollama

ollama = Ollama(model="eeve-korean-10-8b", base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"))
answer = ollama.invoke("덤벨만으로 45분 가슴/어깨 루틴 만들어줘. 세트/횟수/휴식 포함.")
```

**Streamlit 엔트리**

```python
import streamlit as st
st.set_page_config(page_title="RAG Workout Assistant", layout="wide")
# 업로드 → 인덱스 → 챗/루틴 생성 UI 구성
```

---

## \[ Roadmap ]
* [ ] 로그인/DB 연동(PostgreSQL/Supabase) — 사용자별 루틴/히스토리
* [ ] 운동 부위별 매핑 데이터 기반 bge-m3 모델 임베딩(한국어)
* [ ] Azure OpenAI 전환 및 비용/로깅/모니터링
* [ ] E2E 테스트 & GitHub Actions CI/CD

---

## \[ Requirements ]

`requirements.txt` 예시(필요에 맞게 고정):

```
streamlit==1.32.0
langchain==0.1.17
langchain-community==0.0.36
langserve==0.0.45
faiss-cpu==1.7.4
unstructured==0.12.4
sentence-transformers==2.5.1
pandas==2.0.3
numpy==1.24.3
scikit-learn==1.3.0
plotly==5.22.0
```

---

## \[ Data Samples ]

앱은 기본으로 다음 샘플 파일을 참조합니다(사이드바 "다중 데이터셋"):

- `Langserve-ollama/data/text_ex.csv`
- `Langserve-ollama/data/full_data_ex.csv`
- `Langserve-ollama/data/embeddings_ex.npy`

파일이 없거나 `embeddings_ex.npy` 로드 실패 시 텍스트 기반 검색으로 자동 폴백합니다.

---

## \[ Docker Local ]

도커로 로컬 실행하려면:

```bash
cd Langserve-ollama
docker build -t rag-workout:local -f Dockerfile .
docker run --rm -p 8501:8501 \
  -e OLLAMA_BASE_URL="http://host.docker.internal:11434" \
  rag-workout:local
```

---

## \[ License ]

이 프로젝트는 View Only Project로 자세한 내용은 LICENSE 파일을 참조하세요.

---

## \[ Demo / YouTube ]

* [(시연 영상)](https://youtu.be/4JtC5eUrYwo)

---

필요하면 **배지(버전/라이선스/배포 링크)**, **스크린샷 섹션**, **.env 예시**까지 더해줄 수 있어. 지금은 포트폴리오 스타일에 맞춰 **스토리+기술+배포**가 한눈에 보이도록 구성했어.
