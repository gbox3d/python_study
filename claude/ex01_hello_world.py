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
        
        api_key=os.getenv("ANTHROPIC_API_KEY")
    )

    message = client.messages.create(
        model="claude-3-sonnet-20241022",
        max_tokens=1000,
        temperature=0,
        messages=[
            {
                "role": "user",
                "content": "Hello! 간단한 인사를 해주세요."
            }
        ]
    )

    print("Claude의 응답:")
    print(message.content[0].text)

if __name__ == "__main__":
    main()