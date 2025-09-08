import anthropic
import os
import sys

def main():
    # Windows 콘솔 인코딩 설정
    sys.stdout.reconfigure(encoding='utf-8')
    
    API_KEY = os.getenv("ANTHROPIC_API_KEY")
    if not API_KEY:
        raise ValueError("Please set the ANTHROPIC_API_KEY environment variable.")
    
    client = anthropic.Anthropic(
        api_key=API_KEY
    )
    
    try:
        # 사용 가능한 모델 목록 가져오기
        models = client.models.list()
        
        print("사용 가능한 Claude 모델 목록:")
        print("-" * 50)
        
        for model in models.data:
            print(f"모델 ID: {model.id}")
            
            # 속성이 있는지 확인 후 출력
            if hasattr(model, 'created'):
                print(f"생성일: {model.created}")
            if hasattr(model, 'owned_by'):
                print(f"소유자: {model.owned_by}")
            if hasattr(model, 'display_name') and model.display_name:
                print(f"표시명: {model.display_name}")
            if hasattr(model, 'type'):
                print(f"타입: {model.type}")
                
            print("-" * 30)
            
    except Exception as e:
        print(f"모델 목록을 가져오는 중 오류 발생: {e}")
        print("\n알려진 Claude 모델들:")
        known_models = [
            "claude-3-haiku-20240307",
            "claude-3-sonnet-20240229", 
            "claude-3-opus-20240229",
            "claude-3-5-sonnet-20240620",
            "claude-3-5-haiku-20241022"
        ]
        for model in known_models:
            print(f"- {model}")

if __name__ == "__main__":
    main()