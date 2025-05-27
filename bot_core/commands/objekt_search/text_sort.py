# Re-run after notebook reset

import re, json
from typing import Optional, Dict

NAME_DATA = {
    "Seoyeon":  ["Ham", "Hamham", "Pochacco", "햄", "햄햄", "포차코", "근본", "윤통", "윤서연", "서연"],
    "Hyerin":   ["Hyebam", "RiNe", "혜밤", "리네", "혜린", "정혜린", "혀린", "정혜리더", "혜리더"],
    "Jiwoo":    ["Jyuu", "Jiwpo", "지우", "이지우", "돌맹이"],
    "Chaeyeon": ["Chaeyomi", "채연", "김채연", "수만이", "뚜마니", "뚜마닝", "쑤마닝", "뜌미닝"],
    "Yeoyeon":  ["유연", "김유연", "이대여신", "이대"],
    "Soomin":   ["Soomsoom", "수민", "김수민", "숨숨"],
    "Nakyoung": ["Naky", "나경", "김나경", "김나갱", "나키", "깜냥", "깜냥이"],
    "Yubin":    ["Yubam", "유빈", "공유빈", "유밤"],
    "Kaede":    ["Kae-chan", "Kaepyon", "edeka", "카에", "카에데", "코에데", "코에", "에데", "에데카"],
    "Dahyun":   ["Soda", "다현", "서다현", "소다", "체리소다"],
    "Kotone":   ["Tone", "코토네", "토네"],
    "Yeonji":   ["Kwak", "연지", "곽연지", "곽곽", "곽곽이", "오리"],
    "Nien":     ["니엔", "녠", "Nancy", "허니엔", "Buff Nien"],
    "Sohyun":   ["Park ssaem", "박소현", "소현", "박쌤", "백구"],
    "Xinyu":    ["Chinese Goddess", "저우신위", "신위", "여신위"],
    "Mayu":     ["Koma-san", "Komayu", "마유", "코우마 마유"],
    "Lynn":     ["Shark", "Kawalynn", "린", "카와카미 린"],
    "Joobin":   ["Binnie", "빈", "주빈", "주밤", "비니", "베이빈", "babin"],
    "Hayeon":   ["Captain", "Hexagon", "하연", "육각", "하밤"],
    "Shion":    ["Bread", "박시온", "시온", "빵시온"],
    "Chaewon":  ["Chaepup", "채원", "김채원", "딸기", "딸기공주", "왹왹", "외계인"],
    "Sullin":   ["Thai Princess", "Nùn", "설린", "태국", "태국공주"],
    "Seoah":    ["Baby (Seo)", "Aegi", "Haerin", "서아", "정서아", "아기", "아가", "서아기", "서아가", "해린", "정해린"],
    "Jiyeon":   ["Swan", "Dojoon", "지연", "지서연", "도준", "백조"],
}
alias_to_name = {}
for name, aliases in NAME_DATA.items():
    alias_to_name[name.lower()] = name
    for alias in aliases:
        alias_to_name[alias.lower()] = name
sorted_aliases = sorted(alias_to_name.keys(), key=len, reverse=True)
member_regex = re.compile("|".join(re.escape(a) for a in sorted_aliases), re.I)

season_alias_map = {}
for alias in ["a", "a1", "atom01", "atom1"]:
    season_alias_map[alias] = "Atom01"
for alias in ["b", "b1", "binary01"]:
    season_alias_map[alias] = "Binary01"
for alias in ["c", "c1", "cream01"]:
    season_alias_map[alias] = "Cream01"
for alias in ["d", "d1", "divine01"]:
    season_alias_map[alias] = "Divine01"
for alias in ["e", "e1", "ever01"]:
    season_alias_map[alias] = "Ever01"
for alias in ["aa", "a2", "atom02", "atom2"]:
    season_alias_map[alias] = "Atom02"
season_alias_map["spring25"] = "Spring25"

season_token_pattern = r"(aa|a2|a1|a|atom02|atom01|b1|b|binary01|c1|c|cream01|d1|d|divine01|e1|e|ever01|spring25)"
season_regex = re.compile(season_token_pattern, re.I)

number_digital_regex = re.compile(r"(\d{3})([ZA])?\b", re.I)

def extract(text:str) -> Dict[str, Optional[str]]:
    res = {"member": None, "season": None, "number": None, "digital": None}
    # member
    m = member_regex.search(text)
    if m:
        res["member"] = alias_to_name[m.group(0).lower()]
    # season
    s = season_regex.search(text)
    if s:
        res["season"] = season_alias_map[s.group(0).lower()]
    # number & digital
    n = number_digital_regex.search(text)
    if n:
        res["number"] = n.group(1)
        res["digital"] = (n.group(2) or "Z").upper()
    else:
        res["digital"] = "Z"
    return res


if __name__ == '__main__':
    samples = [
        "소현 B 100 a"
    ]

    for s in samples:
        print(s)
        print("  ->", json.dumps(extract_info(s), ensure_ascii=False))

