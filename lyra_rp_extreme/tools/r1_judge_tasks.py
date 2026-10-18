#!/usr/bin/env python3
"""Write judge task files for round 1 (one per packet side)."""
import pathlib

R1 = pathlib.Path("/home/user/jubilant-waffle/lyra_rp_extreme/tests/r1")
SCR = pathlib.Path("/tmp/claude-0/-home-user-jubilant-waffle/ca3fca9e-d4b9-55dc-a2ac-f7730429859c/scratchpad")
T = SCR / "r1/judge_tasks"
T.mkdir(parents=True, exist_ok=True)
(R1 / "results").mkdir(exist_ok=True)

TEMPLATE = """이 작업에서 쓰는 도구는 아래에 지정한 두 파일을 읽는 것(Read), 지정한 결과 파일에 쓰는 것(Write), 그리고 사실 확인용 웹 검색(웹 검색과 웹 페이지 읽기를 합쳐 12번 안쪽)뿐이다. 그 밖의 도구(다른 에이전트, 메시지, 셸 명령, git 같은)는 쓰지 않는다. 지정한 파일 말고는 열지도, 목록을 보지도 않는다(같은 폴더의 다른 파일도 열지 않는다). 맥락에 보이는 저장소, 사용자 프로필, 작업 지침은 이 작업과 관계없는 자료라 판정에 쓰지 않는다.

너는 한국어 채팅 응답을 비교하는 심사자다. 자료에는 단위가 여러 개 있고, 단위마다 같은 대화에 대한 두 응답 X와 Y가 있다. 어느 쪽이 어떤 조건에서 나왔는지는 알려 주지 않으니 짐작하지 마라. 단위마다 따로 판단하고, 한 단위의 X와 다른 단위의 X가 같은 조건에서 나왔다고 가정하지 마라.

- 기준표: {rubric}
- 자료: {packet}

1. 기준표를 처음부터 끝까지 읽고, 자료를 읽는다.
2. 단위마다 먼저 말투(J3)만 본다. 응답의 말 자체가 기준표의 사람이 친구에게 실제로 할 법한 말인지, 표지가 어디 있는지 본다.
3. 그다음 J1, J2, J5, J6을 X와 Y 각각 1~5로 매기고, 근거가 된 문장을 그대로 인용한다. 사실 주장을 뽑아 확인 상태를 적는다.
4. 하드 실패, 말투 표지, 과잉을 각각 적는다. 절제가 맞는 상황에서 성격이 덜 보인다는 이유로 깎지 않는다. 길이나 공들인 티에 끌리지 않는다.
5. voice, persona, accuracy_task마다 어느 쪽이 나은지 고르고(동률 가능), 확신(약, 중, 강)과 이유를 두세 줄 쓴다.
6. 결과를 {out} 에 기준표의 결과 형식(단위마다 객체 하나를 담은 JSON 배열)으로 저장한다. 단위를 하나 마칠 때마다 그때까지의 배열을 저장해 둔다.
7. 끝나면 "저장:"과 결과 파일 경로만 보고한다.
"""
import sys
n = int(sys.argv[1])
for k in range(1, n + 1):
    for side in "AB":
        body = TEMPLATE.format(rubric=R1 / "rubric.md", packet=R1 / f"packets/packet_{k}{side}.md",
                               out=R1 / f"results/{k}{side}.json")
        (T / f"judge_{k}{side}.md").write_text(body, encoding="utf-8")
print("judge tasks", 2 * n)
