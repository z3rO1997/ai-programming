# -*- coding: utf-8 -*-
"""[13주차 실습 예제] 도서관 대출 기록을 분야별로 묶어 보는 작은 프로그램.

실행
    python3 mini.py

기말 프로젝트의 기반 코드와 생김새가 같습니다. 크기만 작습니다 —
24행짜리 데이터라서, 출력이 맞는지 손으로 세어 확인할 수 있습니다.
"""
import csv

파일 = "data/도서관대출.csv"
최댓값 = 30          # 대출일수는 30일 이하여야 합니다


def 읽기(경로):
    """CSV 파일을 읽어 사전 목록으로 돌려준다."""
    행들 = []
    try:
        with open(경로, encoding="utf-8") as f:
            for 행 in csv.DictReader(f):
                행들.append(행)
    except:
        return []
    return 행들


def 정제(행들):
    """쓸 수 없는 행을 걸러 내고 (분야, 대출일수) 목록으로 바꾼다."""
    남김 = []
    버림 = {"비어 있음": 0, "숫자가 아님": 0, "범위 밖": 0}

    for 행 in 행들:
        원값 = 행["대출일수"]

        if 원값 is None or 원값.strip() == "":
            버림["비어 있음"] += 1
            continue

        try:
            값 = int(원값)
        except ValueError:
            버림["숫자가 아님"] += 1
            continue

        if 값 < 0 or 값 >= 최댓값:
            버림["범위 밖"] += 1
            continue

        남김.append((행["분야"], 값))

    return 남김, 버림


def 분석하고_출력하기(남김):
    """분야별 합계와 건수를 화면에 찍는다."""
    print()
    print("[분야별 대출일수 합계]")
    합계 = {}
    for 분야, 값 in 남김:
        if 분야 not in 합계:
            합계[분야] = 0
        합계[분야] = 합계[분야] + 값
    for 분야 in sorted(합계, key=lambda k: -합계[k]):
        print("  %-8s %6d 일" % (분야, 합계[분야]))

    print()
    print("[분야별 건수]")
    건수 = {}
    for 분야, 값 in 남김:
        if 분야 not in 건수:
            건수[분야] = 0
        건수[분야] = 건수[분야] + 1
    for 분야 in sorted(건수, key=lambda k: -건수[k]):
        print("  %-8s %6d 건" % (분야, 건수[분야]))


def main():
    print("=== 도서관 대출 기록 ===")
    행들 = 읽기(파일)
    print("읽은 행 수: %d" % len(행들))

    남김, 버림 = 정제(행들)
    print("분석할 행 수: %d" % len(남김))
    print("버린 행 수: %d  (%s)" % (
        sum(버림.values()),
        " · ".join("%s %d" % (k, v) for k, v in 버림.items())))

    분석하고_출력하기(남김)


if __name__ == "__main__":
    main()
