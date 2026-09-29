# -*- coding: utf-8 -*-
"""
buggy_4.py  ―  총 매출액 집계 (에러 없이 '조용히' 틀리는 스크립트)

이 스크립트는 에러 없이 잘 돌아가고, 그럴듯한 숫자를 출력한다.
하지만 그 숫자는 '틀렸다'.

[과제] 이 스크립트는 예외를 던지지 않는다. 대신
       (1) info()/describe()로 데이터 상태를 먼저 세어 보고
       (2) '무엇이 틀렸는지 어떻게 알아챘는지'를 서술한 뒤
       (3) 결측 규모를 보고하고 처리 방법을 선택·적용하여
           올바른 총매출을 산출하라.
       (힌트: 가격 결측은 몇 건인가? 음수 가격과 9999999 같은 값은 정상인가?)
"""
import pandas as pd

def main():
    df = pd.read_csv("dirty_sales.csv", encoding="utf-8")

    # price를 숫자로 바꾼다 (빈 값은 NaN이 된다 — 그런데 그 규모를 확인하지 않았다)
    df["price"] = (df["price"].astype(str)
                              .str.replace(",", "")
                              .str.replace("원", "")
                              .str.strip())
    df["price"] = pd.to_numeric(df["price"], errors="coerce")

    print("=== 데이터 정보 ===")
    df.info()
    print("=== 가격, 수량 요약 ===")
    print(df[["price","quantity"]].describe())
    print("가격 결측:", df["price"].isna().sum())
    print("음수 가격:", (df["price"] < 0).sum())
    print("9999999 가격:", (df["price"] == 9999999).sum())
    print("9999999 수량:", (df["quantity"] == 9999999).sum())
    #FIXED: info(), describe()를 이용해서 데이터 상태를 먼저 확인

    valid = (
        df["price"].notna()
        & (df["price"] >= 0)
        & (df["price"] != 9999999)
        & (df["quantity"] != 9999999)
    )

    df["revenue"] = df["price"] * df["quantity"]
    total = df.loc[valid, "revenue"].sum()
    avg_price = df.loc[valid, "price"].mean()

    print("제외한 행 수:", (~valid).sum())
    print(f"총 매출액: {total:,.0f}원")
    print(f"평균 단가: {avg_price:,.0f}원")
    # FIXED: 결측·음수·9999999 가격과 비정상 수량 행은 합계에서 제외

if __name__ == "__main__":
    main()
