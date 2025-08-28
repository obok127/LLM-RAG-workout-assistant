"""
애플리케이션 설정값들을 관리하는 모듈
"""

import os
from typing import Dict, Any

# 기본 설정값들
DEFAULT_SETTINGS = {
    # 모델 설정
    "model": {
        "name": "EEVE-Korean-Instruct-10.8B-v1.0-GGUF",
        "temperature": 0.7,
        "max_tokens": 2048,
        "top_p": 0.9,
        "top_k": 40
    },
    
    # 임베딩 설정
    "embeddings": {
        "model_name": "BAAI/bge-m3",
        "device": "cpu",
        "normalize_embeddings": True,
        "dimension": 1024
    },
    
    # 검색 설정
    "search": {
        "default_top_k": 5,
        "max_top_k": 20,
        "similarity_threshold": 0.7,
        "use_embeddings": True,
        "fallback_to_text": True
    },
    
    # UI 설정
    "ui": {
        "page_title": "AI 운동자세 어시스턴트",
        "page_icon": "🏥",
        "layout": "wide",
        "initial_sidebar_state": "expanded",
        "max_message_history": 50
    },
    
    # 데이터 설정
    "data": {
        "data_dir": "./data",
        "text_csv": "text_ex.csv",
        "full_csv": "full_data_ex.csv",
        "embeddings_npy": "embeddings_ex.npy",
        "cache_embeddings": True
    },
    
    # 로깅 설정
    "logging": {
        "level": "INFO",
        "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        "file": "app.log"
    },
    
    # 성능 설정
    "performance": {
        "enable_caching": True,
        "cache_ttl": 3600,  # 1시간
        "max_concurrent_requests": 10,
        "request_timeout": 30
    }
}

class Settings:
    """설정값을 관리하는 클래스"""
    
    def __init__(self, custom_settings: Dict[str, Any] = None):
        self.settings = DEFAULT_SETTINGS.copy()
        
        # 환경변수에서 설정값 로드
        self._load_from_env()
        
        # 사용자 정의 설정값 적용
        if custom_settings:
            self._update_settings(custom_settings)
    
    def _load_from_env(self):
        """환경변수에서 설정값을 로드하는 함수"""
        env_mappings = {
            "MODEL_TEMPERATURE": ("model", "temperature", float),
            "MODEL_MAX_TOKENS": ("model", "max_tokens", int),
            "EMBEDDINGS_MODEL": ("embeddings", "model_name", str),
            "EMBEDDINGS_DEVICE": ("embeddings", "device", str),
            "SEARCH_TOP_K": ("search", "default_top_k", int),
            "SEARCH_THRESHOLD": ("search", "similarity_threshold", float),
            "DATA_DIR": ("data", "data_dir", str),
            "LOG_LEVEL": ("logging", "level", str),
            "CACHE_TTL": ("performance", "cache_ttl", int)
        }
        
        for env_var, (section, key, type_func) in env_mappings.items():
            value = os.getenv(env_var)
            if value is not None:
                try:
                    self.settings[section][key] = type_func(value)
                except (ValueError, TypeError):
                    print(f"Warning: Invalid value for {env_var}: {value}")
    
    def _update_settings(self, custom_settings: Dict[str, Any]):
        """사용자 정의 설정값을 적용하는 함수"""
        for section, values in custom_settings.items():
            if section in self.settings:
                self.settings[section].update(values)
            else:
                self.settings[section] = values
    
    def get(self, section: str, key: str, default: Any = None) -> Any:
        """설정값을 가져오는 함수"""
        try:
            return self.settings[section][key]
        except KeyError:
            return default
    
    def set(self, section: str, key: str, value: Any):
        """설정값을 설정하는 함수"""
        if section not in self.settings:
            self.settings[section] = {}
        self.settings[section][key] = value
    
    def get_section(self, section: str) -> Dict[str, Any]:
        """섹션 전체 설정값을 가져오는 함수"""
        return self.settings.get(section, {})
    
    def get_model_settings(self) -> Dict[str, Any]:
        """모델 설정값을 가져오는 함수"""
        return self.get_section("model")
    
    def get_embeddings_settings(self) -> Dict[str, Any]:
        """임베딩 설정값을 가져오는 함수"""
        return self.get_section("embeddings")
    
    def get_search_settings(self) -> Dict[str, Any]:
        """검색 설정값을 가져오는 함수"""
        return self.get_section("search")
    
    def get_ui_settings(self) -> Dict[str, Any]:
        """UI 설정값을 가져오는 함수"""
        return self.get_section("ui")
    
    def get_data_settings(self) -> Dict[str, Any]:
        """데이터 설정값을 가져오는 함수"""
        return self.get_section("data")
    
    def get_performance_settings(self) -> Dict[str, Any]:
        """성능 설정값을 가져오는 함수"""
        return self.get_section("performance")
    
    def to_dict(self) -> Dict[str, Any]:
        """전체 설정값을 딕셔너리로 반환하는 함수"""
        return self.settings.copy()
    
    def validate(self) -> bool:
        """설정값의 유효성을 검증하는 함수"""
        try:
            # 필수 설정값 검증
            required_sections = ["model", "embeddings", "search", "ui", "data"]
            for section in required_sections:
                if section not in self.settings:
                    print(f"Error: Missing required section: {section}")
                    return False
            
            # 값 범위 검증
            if not (0 <= self.get("model", "temperature", 0) <= 2):
                print("Error: Model temperature must be between 0 and 2")
                return False
            
            if self.get("search", "default_top_k", 0) <= 0:
                print("Error: Search top_k must be positive")
                return False
            
            if not (0 <= self.get("search", "similarity_threshold", 0) <= 1):
                print("Error: Similarity threshold must be between 0 and 1")
                return False
            
            return True
            
        except Exception as e:
            print(f"Error validating settings: {e}")
            return False

# 전역 설정 인스턴스
settings = Settings()

# 편의 함수들
def get_setting(section: str, key: str, default: Any = None) -> Any:
    """전역 설정에서 값을 가져오는 편의 함수"""
    return settings.get(section, key, default)

def set_setting(section: str, key: str, value: Any):
    """전역 설정에 값을 설정하는 편의 함수"""
    settings.set(section, key, value)

def get_model_config() -> Dict[str, Any]:
    """모델 설정을 가져오는 편의 함수"""
    return settings.get_model_settings()

def get_embeddings_config() -> Dict[str, Any]:
    """임베딩 설정을 가져오는 편의 함수"""
    return settings.get_embeddings_settings()

def get_search_config() -> Dict[str, Any]:
    """검색 설정을 가져오는 편의 함수"""
    return settings.get_search_settings()

def get_ui_config() -> Dict[str, Any]:
    """UI 설정을 가져오는 편의 함수"""
    return settings.get_ui_settings() 