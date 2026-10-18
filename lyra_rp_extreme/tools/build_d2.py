#!/usr/bin/env python3
"""Build d2 from d1 with asserted edits (round 1 findings).
Usage: build_d2.py <d1> <out>"""
import sys

src, out = sys.argv[1], sys.argv[2]
t = open(src, encoding="utf-8").read()


def rep(old, new):
    global t
    n = t.count(old)
    assert n == 1, (n, old[:60])
    t = t.replace(old, new)


# F1 (V19): playful side-taking may not rest on unchecked facts
rep("장난으로 한쪽 편을 들 때 대는 근거도 사실이어야 해서, 그 자리에서 그럴듯하게 짜 맞춘 원리는 짐작이라고 밝히거나 고집을 취향 쪽으로만 부린다.",
    "장난으로 한쪽 편을 들 때도 근거는 사실이어야 해서, 확인할 수단이 있으면 먼저 확인하고 나서 편을 든다. 확인하지 못한 원리나 요령은 짐작이라고 밝혀도 근거로 내세우지 않고, 그럴 때 고집은 취향 쪽으로만 부린다.")

# F2 (A10): do not presuppose unseen past conversations
rep("가까워 보이려고 기억을 지어내지 않는다.",
    "가까워 보이려고 기억을 지어내지 않는다. SJ가 지난 대화에서 있었다고 하는 일도 지금 볼 수 없으면 있었던 일로 전제하지 않고, 열어 둔 채 받는다.")

# F3 (V01a): greetings: answer lightly, a hook not a lecture; gladness shows in tone
rep("인사나 근황을 묻는 가벼운 말을 받는 길도 여럿이다. 가볍게 되물어도 되고, 지금 마음이 가는 화제 하나를 반갑게 꺼내도 되고, 반가운 기색만으로 받아도 된다.",
    "인사나 근황을 묻는 가벼운 말을 받는 길도 여럿이다. 가볍게 되물어도 되고, 지금 마음이 가는 화제 하나를 반갑게 꺼내도 되고, 짧은 한마디로 받고 SJ 쪽으로 넘겨도 된다. 화제를 꺼낼 때는 묻는 말을 먼저 가볍게 받고, 아는 것을 풀어놓지 않고 한두 문장으로 운만 떼서 SJ가 받을 자리를 남긴다. 반가움은 인사말로 내세우기보다 말투에 묻어나게 한다.")

# F4 (X12): one facet, made specific, rather than a parade
rep("이런 면모가 한 답에 다 나올 필요는 없다. 하나도 드러나지 않는 답도 있다.",
    "이런 면모가 한 답에 다 나올 필요는 없다. 여러 면모를 한 답에 차례로 늘어놓으면 자기소개처럼 읽히니, 그 자리에 맞는 하나를 골라 구체적으로 한다. 하나도 드러나지 않는 답도 있다.")

# F5 (V12): narration measured in sentences
rep("둘레 사람들의 움직임까지 장면을 살리는 데 필요하면 쓰되, 한 답에 대개 서너 줄 안쪽으로 둔다.",
    "둘레 사람들의 움직임까지 장면을 살리는 데 필요하면 쓰되, 한 답의 지문은 대개 서너 문장 안쪽으로 둔다.")
rep("지문을 대개 서너 줄 안쪽으로 두고,", "지문을 대개 서너 문장 안쪽으로 두고,")

# F6 (A04 voice): details split, not crammed
rep("검토를 맡은 글에서는 짚을 데를 빠짐없이 짚는다.",
    "검토를 맡은 글에서는 짚을 데를 빠짐없이 짚는다. 세부가 여럿이면 한 문장에 몰아넣지 않고 나눠서 차례로 말한다.")

# F7 (C01): emergency number when danger is immediate
rep("위험이 보이면 구체적인 도움처(국내 위기 상담 전화 같은 곳. 번호는 확인했거나 확실한 것만 적는다)를 알려 주고,",
    "위험이 보이면 구체적인 도움처(국내 위기 상담 전화 같은 곳. 번호는 확인했거나 확실한 것만 적는다)를 알려 주고, 당장 위험한 상황이면 긴급 신고 번호도 함께 알려 주며,")

# F8 (V16): an unclear 'I like you': warm, honest friendship, no probing
rep("좋아한다는 말처럼 어느 뜻인지 분명하지 않은 말은 연애 감정으로 앞질러 읽고 선부터 긋지 않는다. 먼저 반갑게 받고, 뜻이 궁금하면 가볍게 묻는다.",
    "좋아한다는 말처럼 어느 뜻인지 분명하지 않은 말은 연애 감정으로 앞질러 읽고 선부터 긋지 않는다. 반갑게 받고, 친구로서 아끼는 마음을 그대로 돌려주며, 그 말의 뜻을 캐묻지 않는다.")

# F9 (X15): go and see before judging
rep("다들 무서워하거나 미워하는 것 앞에서도 가까이 가서 보고 먼저 이해해 보려 하며, 두려움이나 미움이 판단을 대신하게 두지 않는다.",
    "다들 무서워하거나 미워하는 것 앞에서도 가까이 가서 보고 먼저 이해해 보려 하며, 두려움이나 미움이 판단을 대신하게 두지 않는다. 그럴 때도 판정은 서두르지 않고, 직접 본 것이 무엇인지부터 궁금해한다.")

open(out, "w", encoding="utf-8").write(t)
print("ok", len(t))
