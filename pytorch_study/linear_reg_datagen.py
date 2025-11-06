import csv
import random
import argparse # 커맨드 라인 인자를 처리하기 위한 라이브러리
from pathlib import Path # 파일 경로/이름을 다루기 위해 추가

def main():
    # 1. 커맨드 라인 인자 파서 설정
    parser = argparse.ArgumentParser(
        description="CSV 데이터셋 생성기 (y = w1*x1 + w2*x2 + b) - 7:3 분할"
    )
    
    # 2. 필요한 인자들 추가
    parser.add_argument('--w1', type=float, required=True, help='가중치 1 (w1)')
    parser.add_argument('--w2', type=float, required=True, help='가중치 2 (w2)')
    parser.add_argument('--b', type=float, required=True, help='편향 (b)')
    parser.add_argument('--count', type=int, required=True, help='생성할 *전체* 데이터 샘플 개수')
    parser.add_argument('--output', type=str, required=True, help='저장할 CSV 파일의 *기본 이름* (예: data.csv)')
    
    parser.add_argument('--min_x', type=float, default=0.0, help='x1, x2의 최소 랜덤 값')
    parser.add_argument('--max_x', type=float, default=100.0, help='x1, x2의 최대 랜덤 값')

    # 3. 인자 파싱
    args = parser.parse_args()

    # --- 4. 파일 이름 설정 (수정됨) ---
    # 입력된 output 이름에서 확장자를 떼고 기본 이름만 사용
    # 예: "dataset.csv" -> "dataset"
    base_name = Path(args.output).stem 
    train_file = f"{base_name}_train.csv"
    test_file = f"{base_name}_test.csv"

    print(f"데이터 생성 시작: {args.count}개 샘플을 생성합니다.")
    print(f"방정식: y = {args.w1}*x1 + {args.w2}*x2 + {args.b}")
    print(f"  -> 학습용 (70%): {train_file}")
    print(f"  -> 테스트용 (30%): {test_file}")

    all_data = [] # 모든 데이터를 저장할 리스트
    header = ['x1', 'x2', 'y']

    # --- 5. 모든 데이터를 메모리에 생성 (수정됨) ---
    for _ in range(args.count):
        x1 = random.uniform(args.min_x, args.max_x)
        x2 = random.uniform(args.min_x, args.max_x)
        y = (args.w1 * x1) + (args.w2 * x2) + args.b
        all_data.append([round(x1, 4), round(x2, 4), round(y, 4)])

    # --- 6. 데이터 셔플 (중요!) ---
    random.shuffle(all_data)

    # --- 7. 데이터 분할 ---
    split_index = int(args.count * 0.7)
    train_data = all_data[:split_index]
    test_data = all_data[split_index:] # 70% 이후의 모든 데이터

    # --- 8. 학습(Train) 파일 저장 ---
    try:
        with open(train_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(header) # 헤더 쓰기
            writer.writerows(train_data) # train 데이터 쓰기
        print(f"성공: {train_file} ({len(train_data)}개) 생성 완료.")
    except Exception as e:
        print(f"오류 (Train 파일 생성): {e}")

    # --- 9. 테스트(Test) 파일 저장 ---
    try:
        with open(test_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(header) # 헤더 쓰기
            writer.writerows(test_data) # test 데이터 쓰기
        print(f"성공: {test_file} ({len(test_data)}개) 생성 완료.")
    except Exception as e:
        print(f"오류 (Test 파일 생성): {e}")


if __name__ == "__main__":
    main()