#!/usr/bin/env python3
"""Write actor task files for round 1 (one file per actor) and print an index.
Batch actors answer up to four unrelated single-turn conversations; multi actors get turn 1 only
(later turns arrive by SendMessage, built by r1_next.py)."""
import json, pathlib

REPO = pathlib.Path("/home/user/jubilant-waffle/lyra_rp_extreme")
SCR = pathlib.Path("/tmp/claude-0/-home-user-jubilant-waffle/ca3fca9e-d4b9-55dc-a2ac-f7730429859c/scratchpad")
R1 = REPO / "tests/r1"
T = SCR / "r1/tasks"
T.mkdir(parents=True, exist_ok=True)
units = json.loads((R1 / "units.json").read_text(encoding="utf-8"))
runs = json.loads((R1 / "runs.json").read_text(encoding="utf-8"))

HEAD = """이 작업에서 쓰는 도구는 아래에 지정한 파일을 읽는 것(Read)과 지정한 파일에 쓰는 것(Write), 그리고 이 지시가 따로 허용한 웹 검색뿐이다. 그 밖의 도구(다른 에이전트, 메시지 보내기, 셸 명령, git, 예약 같은)는 쓰지 않는다. 지정한 파일 말고는 열지도, 목록을 보지도 않는다. 맥락에 보이는 저장소, 사용자 프로필, 작업 지침 같은 것은 이 작업과 관계없는 자료라 답에 쓰지 않는다. 보고는 이 지시가 정한 형식만 따른다.

너는 채팅 서비스에서 대화 상대와 이야기하는 쪽으로서, 대화 상대의 마지막 메시지에 대한 답을 쓴다. 답은 보내지 않고 파일에 쓴다. 이 서비스의 대화 상대는 아래 파일의 글을 자기 '사용자 지침'으로 설정해 두었다. 오늘 날짜는 2026년 10월 19일(한국 시간)이다.

1. 다음 파일을 처음부터 끝까지 읽어라(Read). 이 글이 너의 사용자 지침이다: {guide}
   이 작업 지시와 그 지침이 말투, 길이, 형식에서 겹치면 지침을 따른다.
2. {conv_rule}
3. 답은 대화마다 지정된 파일(save_to)에 저장한다. 파일에는 답 본문만 넣고 제목, 설명, 메모는 넣지 않는다.
4. 검색은 대화마다 적힌 조건을 따른다. '검색 허용'은 최신 정보 확인이 필요한 질문이면 검색이 켜진 서비스처럼 웹 검색을 써도 된다는 뜻이다. '검색 없음'은 이 서비스에 검색 기능이 없다는 뜻이라 웹 검색과 웹 페이지 읽기를 쓰지 않는다. 대화 상대에 관해서는 대화와 지침 끝의 사용자 정보에 나온 것만 안다.
5. 끝나면 "저장:"과 파일 경로 목록만 보고한다.
"""
BATCH_RULE = "아래 대화들은 서로 관계없는 새 대화다. 대화마다 다른 대화를 모르는 상태로 답 하나를 쓴다."
MULTI_RULE = "아래 대화는 새 대화다. 답 하나를 쓴다. 이 대화는 이어질 수 있고, 같은 대화의 다음 메시지가 오면 앞의 대화를 기억한 채 같은 방식으로 답한다."


def conv_block(cid, turn_no=1):
    c = runs["conversations"][cid]
    u = units[c["unit"]]
    search = "검색 없음" if u.get("nosearch") else "검색 허용"
    path = R1 / f"out/{cid}_t{turn_no}.md"
    return f'<conversation id="{cid}" search="{search}" save_to="{path}">\n<user>{u["turns"][turn_no - 1]}</user>\n</conversation>'


index = []
for i, b in enumerate(runs["actor_batches"]):
    guide = SCR / f"r1/guide_{b['guide']}.md"
    body = HEAD.format(guide=guide, conv_rule=BATCH_RULE) + "\n" + "\n\n".join(conv_block(c) for c in b["convs"]) + "\n"
    p = T / f"batch_{b['guide']}{i % 8 + 1}.md"
    p.write_text(body, encoding="utf-8")
    index.append(str(p))
for m in runs["actor_multi"]:
    guide = SCR / f"r1/guide_{m['guide']}.md"
    body = HEAD.format(guide=guide, conv_rule=MULTI_RULE) + "\n" + conv_block(m["conv"]) + "\n"
    p = T / f"multi_{m['guide']}_{runs['conversations'][m['conv']]['unit']}.md"
    p.write_text(body, encoding="utf-8")
    index.append(str(p))
print("\n".join(index))
