import re

def extract_body_part_and_goal(question: str) -> tuple[str, str]:
    """질문에서 신체 부위와 목표를 추출하는 함수"""
    question_lower = question.lower()
    
    # 신체 부위 추출
    body_parts = {
        '상체': ['상체', '팔', '어깨', '가슴', '등', '팔꿈치', '손목'],
        '하체': ['하체', '다리', '허벅지', '종아리', '발목', '무릎', '발'],
        '복부': ['복부', '배', '코어', '복근', '허리'],
        '전신': ['전신', '몸', '전체', '신체']
    }
    
    detected_body_part = "전신"
    for part, keywords in body_parts.items():
        if any(keyword in question_lower for keyword in keywords):
            detected_body_part = part
            break
    
    # 목표 추출
    goals = {
        '강화': ['강화', '근력', '힘', '튼튼'],
        '유연성': ['유연성', '스트레칭', '늘리기', '풀기'],
        '통증 완화': ['통증', '아픔', '완화', '치료', '관절'],
        '균형': ['균형', '안정성', '자세'],
        '지구력': ['지구력', '체력', '스태미나']
    }
    
    detected_goal = "기능 향상"
    for goal, keywords in goals.items():
        if any(keyword in question_lower for keyword in keywords):
            detected_goal = goal
            break
    
    return detected_body_part, detected_goal

def _analyze_question_type(question: str) -> str:
    q = question.lower()
    
    patterns = {
        "운동 루틴 추천": [
            r"(무엇|뭐|어떤).*(운동|루틴)",
            r"(운동|자세|동작).*(추천|알려줘|뭐해|좋아)",
            r"(상체|하체|복부|허리|어깨|팔|다리|무릎|목|코어).*운동"
        ],
        "방법/절차 문의": [
            r"(어떻게|하는 ?법|방법|순서|단계|프로세스)",
            r"(운동|자세|스트레칭).*자세히",
            r"바르게.*(운동|자세)"
        ],
        "부위별 통증/건강 관련": [
            r"(아프|통증|불편|결림|쑤심|삐끗|부상)",
            r"(무릎|허리|어깨|목|팔꿈치|발목|척추|손목).*문제"
        ],
        "장비/운동기구 문의": [
            r"(덤벨|밴드|짐볼|매트|바벨|벤치|기구|장비).*운동",
            r"운동.*(도구|기구|장비).*어떤.*좋아"
        ],
        "운동 효과/지속 관련": [
            r"(효과|지속|얼마나|기간|며칠|몇 주|시간).*운동",
            r"(운동|스트레칭).*언제까지.*해야"
        ],
        "운동 안전/주의사항": [
            r"(하면 안되는|주의할 점|잘못된 자세|위험|조심)",
            r"(운동|자세).*하면.*안돼"
        ],
        "일반 정보": [
            r"(정의|이론|원리|과학적 근거)",
            r"(운동|헬스|스트레칭|자세).*이란"
        ],
    }

    for category, regex_list in patterns.items():
        for pattern in regex_list:
            if re.search(pattern, q):
                return category

    return "기타 일반 문의"

TYPE_INSTRUCTIONS = {
    "운동 루틴 추천": "질문자가 원하는 신체 부위 또는 목표에 따라 4개의 운동을 표로 정리하고, 자세한 설명과 운동 가이드라인을 포함해 제공하세요.",
    "방법/절차 문의": "운동 동작을 단계별로 구분하여 안전하고 자세히 설명하세요.",
    "부위별 통증/건강 관련": "의학적 조언은 피하고, 일반적인 주의사항과 완화 운동만 추천하세요.",
    "장비/운동기구 문의": "도구별로 적절한 사용법과 안전한 운동 루틴을 설명하세요.",
    "운동 효과/지속 관련": "운동 효과가 나타나는 일반적인 기간, 빈도, 지속 방법 등을 과학적 근거에 기반해 설명하세요.",
    "운동 안전/주의사항": "자주 발생하는 실수와 그로 인한 부상 위험을 설명하고, 안전하게 운동하는 팁을 제시하세요.",
    "일반 정보": "운동과 관련된 이론, 원리, 정의 등을 쉽게 설명하세요.",
    "기타 일반 문의": "질문 내용을 바탕으로 가장 적절한 형식으로 답변을 구성하세요."
}

def generate_nori_prompt(question: str, body_part: str, goal: str = None) -> str:
    return f"""🤖 **AI 운동자세 어시스턴트: 노리입니다!**

**{body_part} 건강과 {goal or '기능 향상'}을 위한 운동 루틴을 알려드릴게요! 💪✨**

---

### 🏋️‍♀️ **운동 루틴 (총 4가지)**

| 운동 이름            | 세트 수 | 반복 횟수         |
| ------------------ | ------ | -------------- |
| [운동 1 이름]        | 3세트   | 10~15회         |
| [운동 2 이름]        | 3세트   | 양쪽 각 12~15회   |
| [운동 3 이름]        | 3세트   | 15~20회         |
| [운동 4 이름]        | 3세트   | 15초 유지 × 3    |

---

### 📌 **운동 자세 설명**

#### 🟡 [운동 1 이름]
• 단계별 동작 설명  
• 주의 사항  
• 적절한 호흡 및 속도  

#### 🟢 [운동 2 이름]
• 단계별 동작 설명  
• 주의 사항  
• 운동 효과 설명  

#### 🔵 [운동 3 이름]
• 단계별 동작 설명  
• 주의 사항  
• 운동 중 흔한 실수  

#### 🟣 [운동 4 이름]
• 단계별 동작 설명  
• 주의 사항  
• 어떤 사람에게 특히 추천되는지  

---

### ⏱️ **운동 가이드라인**

• 각 운동 후 **1분 휴식**  
• 세트 사이에는 **조금 더 긴 휴식**  
• **통증이 느껴지면 즉시 중지하고 무리하지 않기**  
• 운동 전에는 가볍게 스트레칭 또는 의사 상담 권장  
• 가능한 한 **매일 규칙적인 루틴으로 반복**하기  

---

**지금의 작은 실천이 내일의 건강을 만듭니다. 🌱  
노리와 함께 천천히, 하지만 꾸준히 해봐요!  
화이팅입니다! 💪🌟**
"""

# 고도화된 프롬프트 엔지니어링
class AdvancedPromptBuilder:
    def __init__(self):
        self.base_system_prompt = """당신은 운동 프로그램 전문 AI 어시스턴트입니다.
사용자의 질문에 대해 정확하고 유용한 운동 정보를 제공하는 것이 목표입니다."""
        
        self.data_type_instructions = {
            "실제 데이터": "운동 프로그램 데이터를 바탕으로 구체적이고 실용적인 운동 정보를 제공하세요."
        }
        
    def build_rag_prompt(self, context, question, data_types=None, confidence_threshold=0.7):
        specific_instructions = []
        if data_types:
            for dt in data_types:
                if dt in self.data_type_instructions:
                    specific_instructions.append(self.data_type_instructions[dt])
        
        confidence_instruction = self._get_confidence_instruction(confidence_threshold)
        question_type = self._analyze_question_type(question)
        type_instruction = self._get_type_specific_instruction(question_type)
        
        # 신체 부위와 목표 추출
        body_part, goal = extract_body_part_and_goal(question)
        
        prompt = f"""{self.base_system_prompt}

**현재 상황:**
- 검색된 데이터 유형: {', '.join(data_types) if data_types else '일반'}
- 질문 유형: {question_type}
- 추출된 신체 부위: {body_part}
- 추출된 목표: {goal}

**특별 지시사항:**
{chr(10).join(f"• {inst}" for inst in specific_instructions)}

**답변 구조 (운동 추천 시):**
1. **인사말**: "🤖 **AI 운동자세 어시스턴트: 노리입니다!**"
2. **목표 제시**: "{body_part} 건강과 {goal}을 위한 운동 루틴을 알려드릴게요! 💪✨"
3. **운동 루틴 테이블**: 4개 운동을 표 형태로 정리 (운동 이름, 세트 수, 반복 횟수)
4. **운동 자세 설명**: 각 운동별로 **별도 단락**으로 구분하여 설명 (운동명 (도구) 형식으로 제목 작성, 그 아래에 글머리표(•)를 사용한 단계별 설명을 각각 **새 줄**로 구분)
5. **운동 가이드라인**: 휴식, 주의사항, 안전 수칙
6. **격려 메시지**: "지금의 작은 실천이 내일의 건강을 만듭니다. 🌱 노리와 함께 천천히, 하지만 꾸준히 해봐요! 화이팅입니다! 💪🌟"

**운동 다양성 지침:**
- 정확히 4개의 운동만 추천
- 다양한 운동 도구 활용 (맨몸, 덤벨, 밴드, 짐볼, 바벨 등)
- 다양한 운동 방법 포함 (근력, 지구력, 유연성, 균형)
- 상체/하체/코어 균형 고려
- 초급/중급/고급 난이도 혼합
- 실내/실외 운동 옵션 제공

**답변 가이드라인:**
1. **정확성**: 제공된 문서의 정보만을 사용하여 답변
2. **투명성**: 정보의 출처와 신뢰도를 명확히 표시
3. **완전성**: 질문의 모든 측면을 다루되, 없는 정보는 명시
4. **안전성**: 특히 운동/건강 관련 조언 시 안전 주의사항 포함
5. **실용성**: 구체적이고 실행 가능한 정보 제공

**신뢰도 처리:**
{confidence_instruction}

**질문 유형별 대응:**
{type_instruction}

**참고 문서:**
{context}

**사용자 질문:**
{question}

**답변:**"""
        return prompt
    
    def _analyze_question_type(self, question):
        # 새로운 정교한 질문 분석 함수 사용
        return _analyze_question_type(question)
    
    def _get_confidence_instruction(self, threshold):
        if threshold >= 0.8:
            return "매우 높은 신뢰도의 정보만 사용하여 확신있게 답변하세요."
        elif threshold >= 0.6:
            return "적절한 신뢰도의 정보를 바탕으로 답변하되, 불확실한 부분은 명시하세요."
        else:
            return "낮은 신뢰도의 정보도 참고하되, 반드시 신뢰도 수준을 표시하세요."
    
    def _get_type_specific_instruction(self, question_type):
        # 새로운 정교한 타입별 지침 사용
        if question_type == "운동 루틴 추천":
            return "당신은 'AI 운동자세 어시스턴트: 노리'라는 건강한 AI 코치입니다. 특정 신체 부위 운동 질문에 대해 아래 형식을 정확히 따라 답변하세요: 1) '🤖 **AI 운동자세 어시스턴트: 노리입니다!**'로 시작, 2) 목표 제시, 3) 4개 운동을 표 형태로 정리 (운동 이름, 세트 수, 반복 횟수), 4) 각 운동별로 **별도 단락**으로 구분하여 설명 (운동명 (도구) 형식으로 제목 작성, 그 아래에 글머리표(•)를 사용한 단계별 설명을 각각 **새 줄**로 구분), 5) 운동 가이드라인 (휴식, 주의사항), 6) '지금의 작은 실천이 내일의 건강을 만듭니다. 🌱 노리와 함께 천천히, 하지만 꾸준히 해봐요! 화이팅입니다! 💪🌟'로 마무리. **중요**: 각 운동 설명은 반드시 별도 단락으로 구분하고, 각 단계는 새 줄로 나누어 작성하세요. 중장년층도 이해하기 쉬운 표현을 사용하고, 맨몸 위주로 안전하고 따라하기 쉬운 운동을 제공하세요."
        else:
            return TYPE_INSTRUCTIONS.get(question_type, "명확하고 도움이 되는 답변을 제공하세요.") 
