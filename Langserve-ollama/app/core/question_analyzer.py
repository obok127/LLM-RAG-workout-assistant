import re
from typing import Dict, List, Tuple

class QuestionAnalyzer:
    """질문 분석 및 분류를 담당하는 클래스"""
    
    def __init__(self):
        self.body_parts = {
            '상체': ['상체', '팔', '어깨', '가슴', '등', '팔꿈치', '손목'],
            '하체': ['하체', '다리', '허벅지', '종아리', '발목', '무릎', '발'],
            '복부': ['복부', '배', '코어', '복근', '허리'],
            '전신': ['전신', '몸', '전체', '신체']
        }
        
        self.goals = {
            '강화': ['강화', '근력', '힘', '튼튼'],
            '유연성': ['유연성', '스트레칭', '늘리기', '풀기'],
            '통증 완화': ['통증', '아픔', '완화', '치료', '관절'],
            '균형': ['균형', '안정성', '자세'],
            '지구력': ['지구력', '체력', '스태미나']
        }
        
        self.question_patterns = {
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
    
    def extract_body_part_and_goal(self, question: str) -> Tuple[str, str]:
        """질문에서 신체 부위와 목표를 추출하는 함수"""
        question_lower = question.lower()
        
        # 신체 부위 추출
        detected_body_part = "전신"
        for part, keywords in self.body_parts.items():
            if any(keyword in question_lower for keyword in keywords):
                detected_body_part = part
                break
        
        # 목표 추출
        detected_goal = "기능 향상"
        for goal, keywords in self.goals.items():
            if any(keyword in question_lower for keyword in keywords):
                detected_goal = goal
                break
        
        return detected_body_part, detected_goal
    
    def analyze_question_type(self, question: str) -> str:
        """질문 타입을 분석하는 함수"""
        q = question.lower()
        
        for category, regex_list in self.question_patterns.items():
            for pattern in regex_list:
                if re.search(pattern, q):
                    return category
        
        return "기타 일반 문의"
    
    def get_question_complexity(self, question: str) -> str:
        """질문의 복잡도를 분석하는 함수"""
        word_count = len(question.split())
        
        if word_count <= 5:
            return "단순"
        elif word_count <= 15:
            return "보통"
        else:
            return "복잡"
    
    def extract_keywords(self, question: str) -> List[str]:
        """질문에서 키워드를 추출하는 함수"""
        # 기본적인 키워드 추출 (실제로는 더 정교한 NLP 사용 가능)
        stop_words = ['이', '가', '을', '를', '의', '에', '에서', '로', '으로', '와', '과', '도', '만', '은', '는', '이', '그', '저', '어떤', '무엇', '어떻게', '왜', '언제', '어디서']
        
        words = question.lower().split()
        keywords = [word for word in words if word not in stop_words and len(word) > 1]
        
        return keywords
    
    def analyze_sentiment(self, question: str) -> str:
        """질문의 감정을 분석하는 함수 (기본 구현)"""
        positive_words = ['좋아', '추천', '도움', '효과', '강화', '개선']
        negative_words = ['아프', '통증', '문제', '부상', '위험', '조심']
        
        question_lower = question.lower()
        
        positive_count = sum(1 for word in positive_words if word in question_lower)
        negative_count = sum(1 for word in negative_words if word in question_lower)
        
        if positive_count > negative_count:
            return "긍정적"
        elif negative_count > positive_count:
            return "부정적"
        else:
            return "중립적"
    
    def get_analysis_summary(self, question: str) -> Dict:
        """질문에 대한 종합 분석 결과를 반환하는 함수"""
        body_part, goal = self.extract_body_part_and_goal(question)
        question_type = self.analyze_question_type(question)
        complexity = self.get_question_complexity(question)
        keywords = self.extract_keywords(question)
        sentiment = self.analyze_sentiment(question)
        
        return {
            "body_part": body_part,
            "goal": goal,
            "question_type": question_type,
            "complexity": complexity,
            "keywords": keywords,
            "sentiment": sentiment,
            "word_count": len(question.split())
        } 