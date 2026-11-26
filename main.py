# -*- coding: utf-8 -*-
"""기록 CSV 를 읽어 분류별로 묶어 보는 프로그램.

실행
    python3 main.py

주의
    이 코드는 어딘가 고장나 있습니다. 어디가 왜 고장났는지 찾는 것이
    13주차의 첫 번째 일입니다. 고치기 전에 「명세」부터 복원하세요.
"""
import csv

import config


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


def 정제(행들, 설정):
    """쓸 수 없는 행을 걸러 내고 (날짜, 분류, 수치) 목록으로 바꾼다."""
    남김 = []
    버림 = {"수치가 비어 있음": 0, "숫자가 아님": 0, "범위 밖": 0}

    for 행 in 행들:
        분류 = 행[설정["분류열"]]
        원값 = 행[설정["수치열"]]

        if 원값 is None or 원값.strip() == "":
            버림["수치가 비어 있음"] += 1
            continue

        try:
            값 = int(원값)
        except ValueError:
            버림["숫자가 아님"] += 1
            continue

        if 값 < 0 or 값 >= 설정["최댓값"]:
            버림["범위 밖"] += 1
            continue

        남김.append((행[설정["날짜열"]], 분류, 값))

    return 남김, 버림


def 분석하고_출력하기(남김, 설정):
    """분류별 합계 · 건수 · 최댓값과 전체 평균을 화면에 찍는다."""
    단위 = 설정["단위"]

    print()
    print("[분류별 합계]")
    합계 = {}
    for 날짜, 분류, 값 in 남김:
        if 분류 not in 합계:
            합계[분류] = 0
        합계[분류] = 합계[분류] + 값
    for 분류 in sorted(합계, key=lambda k: -합계[k]):
        print("  %-12s %10s %s" % (분류, format(합계[분류], ","), 단위))

    print()
    print("[분류별 건수]")
    건수 = {}
    for 날짜, 분류, 값 in 남김:
        if 분류 not in 건수:
            건수[분류] = 0
        건수[분류] = 건수[분류] + 1
    for 분류 in sorted(건수, key=lambda k: -건수[k]):
        print("  %-12s %10s 건" % (분류, format(건수[분류], ",")))

    print()
    print("[분류별 최댓값]")
    최대 = {}
    for 날짜, 분류, 값 in 남김:
        if 분류 not in 최대:
            최대[분류] = 값
        if 값 > 최대[분류]:
            최대[분류] = 값
    for 분류 in sorted(최대, key=lambda k: -최대[k]):
        print("  %-12s %10s %s" % (분류, format(최대[분류], ","), 단위))

    print()
    if len(남김) > 0:
        전체합 = 0
        for 날짜, 분류, 값 in 남김:
            전체합 = 전체합 + 값
        print("전체 평균: %.1f %s" % (전체합 / len(남김), 단위))
    else:
        print("전체 평균: 분석할 행이 없습니다")


def main():
    설정 = config.설정()
    print("=== %s 분석 ===" % 설정["이름"])

    행들 = 읽기(설정["파일"])
    print("읽은 행 수: %d" % len(행들))

    남김, 버림 = 정제(행들, 설정)
    print("분석할 행 수: %d" % len(남김))
    print("버린 행 수: %d  (%s)" % (
        sum(버림.values()),
        " · ".join("%s %d" % (k, v) for k, v in 버림.items())))

    분석하고_출력하기(남김, 설정)


if __name__ == "__main__":
    main()
