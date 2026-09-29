## 질문 1- 4번째 스크립트

1. 맥락 
- 오류가 발생하지 않는 에러를 찾아서 수정하기
2. 코드
```
df["price"] = (df["price"].astype(str)
                              .str.replace(",", "")
                              .str.replace("원", "")
                              .str.strip())
    df["price"] = pd.to_numeric(df["price"], errors="coerce")

    df["revenue"] = df["price"] * df["quantity"]

    total = df["revenue"].sum()
    avg_price = df["price"].mean()

    print(f"총 매출액: {total:,.0f}원")
    print(f"평균 단가: {avg_price:,.0f}원")
```
3. Traceback
- 에러가 발생하지 않음

4. 내가 확인한 것
- 어디 부분 코드를 수정해야 할지 확인하기 어려움
5. 요청
- buggy_4는 에러가 발생해도 오류가 발생하지 않는데 어디 부분이 잘못 된 것인지 확인하지 못하겠어
- 답변: buggy_4.py는 예외 없이 실행되지만, 결측치와 이상치를 확인하지 않고 합계와 평균을 계산해서 결과가 왜곡될 수 있는 코드예요.
코드에서 가격을 숫자로 바꾼 뒤 매출을 계산합니다. 변환할 수 없는 빈 가격은 NaN이 되고, 그 행의 매출도 NaN이 됩니다. 그런데 df["revenue"].sum()은 기본적으로 NaN을 건너뛰기 때문에, 매출을 계산할 수 없었던 행이 있다는 사실을 출력만 봐서는 알기 어렵습니다. 반대로 음수 가격과 9999999 같은 극단값은 그대로 합계에 들어갑니다. 수량에도 9999999가 하나 있어 매출이 크게 부풀 수 있습니다. 코드는 다음과 같습니다.

```
# 가격을 숫자로 정리
df["price"] = (
    df["price"].astype(str)
      .str.replace(",", "", regex=False)
      .str.replace("원", "", regex=False)
      .str.strip()
)
df["price"] = pd.to_numeric(df["price"], errors="coerce")

# FIXED: 가격과 수량 데이터 상태 및 결측 규모를 합산 전에 확인
print("=== 데이터 정보 ===")
df.info()
print("=== 가격·수량 요약 ===")
print(df[["price", "quantity"]].describe())
print("가격 결측:", df["price"].isna().sum())
print("음수 가격:", (df["price"] < 0).sum())
print("9999999 가격:", (df["price"] == 9999999).sum())
print("9999999 수량:", (df["quantity"] == 9999999).sum())

# FIXED: 결측·음수·극단값이 포함된 행은 총매출 계산에서 제외
valid = (
    df["price"].between(0, 100000, inclusive="left")
    & df["quantity"].between(0, 100000, inclusive="left")
)
df["revenue"] = df["price"] * df["quantity"]
total = df.loc[valid, "revenue"].sum()

print("제외한 행 수:", (~valid).sum())
print(f"총 매출액: {total:,.0f}원")
``` 

- 추가 질문: ```valid = (
    df["price"].between(0, 100000, inclusive="left")
    & df["quantity"].between(0, 100000, inclusive="left")
) ``` 이 부분 꼭 코드에 넣어야해?

- 답변: 가격과 수량이 정한 정상 범위에 들어오는 행을 표시합니다.
- 채택: 정상 범위를 넘어가던 부분을 표시하기 위해서 필요하다고 판단함

## 질문 2- 5번째 스크립트

1. 맥락
- 리스트 범위 벗어나는 문제 해결하기
2. 코드
```
for i in range(len(prices)):
    diff = prices[i + 1] - prices[i]
```
3. Traceback
- IndexError
4. 내가 확인한 것
- 반복문으로 범위 수정 해야함
5. 요청
- 반복문 범위를 어떻게 바꿔야하는지 알려줘
- 답변:  비교할 다음 값이 있는 곳까지만 반복하도록 range를 바꾸세요.
```
for i in range(len(prices) - 1):  # FIXED: 다음 가격이 있는 인덱스까지만 비교
    diff = prices[i + 1] - prices[i]
```

- 채택: len에서 -1을 함으로써 범위를 벗어나지 않도록 설정하므로 이대로 수정한다.