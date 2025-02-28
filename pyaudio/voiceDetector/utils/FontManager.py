import os
import tkinter as tk
import matplotlib.font_manager as fm
import matplotlib.pyplot as plt

class FontManager:
    """폰트 로딩 및 관리 클래스"""
    
    def __init__(self, font_path="./DungGeunMo.ttf"):
        """폰트 매니저 초기화"""
        self.font_path = font_path
        self.setup_fonts()
    
    def setup_fonts(self):
        """로컬 TTF 폰트 파일 직접 사용"""
        # 폰트 파일 존재 확인
        if not os.path.exists(self.font_path):
            print(f"경고: {self.font_path} 폰트 파일을 찾을 수 없습니다. 기본 폰트를 사용합니다.")
            self.font_family = 'TkDefaultFont'
            self.normal_font = (self.font_family, 10)
            self.header_font = (self.font_family, 12, 'bold')
            self.title_font = (self.font_family, 14, 'bold')
            return
            
        # Matplotlib에 폰트 등록 (버전 호환성 고려)
        font_name = os.path.splitext(os.path.basename(self.font_path))[0]  # 'DungGeunMo'
        
        try:
            # 폰트 매니저에 폰트 추가 (새로운 방식)
            fm.fontManager.addfont(self.font_path)
            # 폰트 캐시 갱신 (버전에 따라 다른 방식 사용)
            try:
                fm.fontManager._load_fontmanager()
            except:
                pass  # 지원하지 않는 버전일 경우 무시
                
        except Exception as e:
            print(f"Matplotlib 폰트 등록 오류 (무시됨): {e}")
        
        # Tkinter 폰트 설정
        try:
            # 시스템에 임시 등록 (Windows만 동작)
            if os.name == 'nt':  # Windows
                try:
                    from ctypes import windll
                    windll.gdi32.AddFontResourceW(os.path.abspath(self.font_path))
                except:
                    print("Windows 폰트 임시 등록 실패 (무시됨)")
                
            # 폰트 이름 설정
            self.font_family = font_name
            print(f"폰트 설정: {font_name}")
        except Exception as e:
            print(f"폰트 등록 오류: {e}")
            self.font_family = 'TkDefaultFont'
            
        # 폰트 크기 설정
        self.normal_font = (self.font_family, 10)
        self.header_font = (self.font_family, 12, 'bold')
        self.title_font = (self.font_family, 14, 'bold')
        
        # Matplotlib 폰트 설정
        plt.rcParams['font.family'] = 'sans-serif'
        plt.rcParams['font.sans-serif'] = [font_name, 'DejaVu Sans']
        
        print(f"폰트 설정 완료: {font_name}")