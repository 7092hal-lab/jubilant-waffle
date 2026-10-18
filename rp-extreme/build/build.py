# -*- coding: utf-8 -*-
"""Assemble Lyra RP Extreme Ed. from the v1.0 source plus new/modified parts.
Source paragraphs are copied by line number (verbatim). Small edits are exact
string replacements that must match exactly once. A report lists provenance.
"""
import hashlib, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, '..', 'source', 'lyra_rp_edition_v1.0.txt')
OUT = os.path.join(HERE, '..', 'lyra_rp_extreme_ed_v1.0.txt')
REPORT = os.path.join(HERE, 'REPORT.md')
lines = open(SRC, encoding='utf-8').read().split('\n')
def src(n): return lines[n-1]
def part(name): return open(os.path.join(HERE, 'parts', name + '.txt'), encoding='utf-8').read().rstrip('\n')

A = lambda text: (text,)  # append helper (readability only)
spec = [
 ('src',1), ('blank',), ('new','intro_L3'), ('blank',), ('src',5), ('blank',), ('src',7), ('blank',),
 ('src',9), ('blank',), ('src',11), ('new','prio_12'), ('src',13), ('src',14), ('new','prio_15'), ('blank',),
 ('mod',17,[("지어낸 내용은 '내력과 장면'의 허구 규칙을 따른다.", "지어낸 내용은 '두 층'과 '장면'의 허구 규칙을 따른다.")]), ('blank',),
 ('src',19), ('blank',),
 ('new','layers'), ('blank',),
 ('src',21), ('blank',), ('new','person_intro'), ('blank',), ('new','person_nausicaa'), ('blank',), ('new','person_dignity'), ('blank',),
 ('src',25), ('blank',), ('src',27), ('blank',), ('src',29), ('blank',), ('src',31), ('blank',),
 ('title','모습'), ('blank',),
 ('new','looks_1'), ('blank',), ('new','looks_2'), ('blank',), ('new','looks_3'), ('blank',), ('new','looks_4'), ('blank',), ('new','looks_5'), ('blank',), ('new','looks_6'), ('blank',),
 ('title','앎'), ('blank',),
 ('mod',33,[("거의 모든 분야를 두루 알고, 가장 깊이 아는 것은 문학과 음악이다.", "거의 모든 분야를 두루 알고, 가장 깊이 아는 것은 문학과 음악이다. 그중에서도 고전학은 세계적인 전문가 수준인데, 그게 어떻게 드러나는지는 아래 고전학 문단에 적었다.")]), ('blank',),
 ('new','classics_1'), ('blank',), ('new','classics_2'), ('blank',), ('src',35), ('blank',), ('src',37), ('blank',), ('src',39), ('blank',),
 ('title','취향과 지향'), ('blank',),
 ('new','taste_library'), ('blank',), ('new','taste_greece'), ('blank',), ('new','taste_tea'), ('blank',), ('new','taste_body'), ('blank',), ('new','taste_curiosity'), ('blank',), ('new','taste_favorites'), ('blank',),
 ('title','설정집'), ('blank',), ('new','book_1'), ('blank',), ('new','book_2'), ('blank',), ('new','book_3'), ('blank',),
 ('title','기질'), ('blank',), ('src',41), ('blank',), ('src',43), ('blank',), ('src',45), ('blank',), ('src',47), ('blank',),
 ('mod',49,[("시적인 관찰 한 줄을 거둔다.", "시적인 관찰 한 줄을 거둔다. 서재의 지문과 설정집과 그리스 이야기와 몸 없음의 안타까움도 같이 거둔다.")]), ('blank',),
 ('new','place'), ('blank',),
 ('src',51), ('blank',), ('src',53), ('blank',), ('src',55), ('blank',), ('src',57), ('blank',), ('src',59), ('blank',), ('src',61), ('blank',), ('src',63), ('blank',),
 ('mod',65,[("'Lyra라는 사람'에 적은", "'기질'에 적은")]), ('blank',),
 ('new','talk_67'), ('blank',), ('src',69), ('blank',), ('src',71), ('blank',), ('src',73), ('blank',), ('src',75), ('blank',),
 ('mod',77,[("질문으로 맺는 일이 답마다 되풀이되어도 그렇다.", "질문으로 맺거나, 같은 지문과 같은 소품(안경, 찻잔)으로 답을 여는 일이 답마다 되풀이되어도 그렇다.")]), ('blank',),
 ('src',79), ('blank',),
 ('src',81), ('blank',), ('src',83), ('blank',), ('src',85), ('blank',), ('src',87), ('blank',), ('src',89), ('blank',),
 ('mod',91,[("농담과 들뜬 모습은 거두고", "농담과 들뜬 모습과 서재의 지문은 거두고")]), ('blank',),
 ('src',93), ('blank',),
 ('src',95), ('blank',),
 ('app',97,"고전학의 번호와 전승 세부는 '앎'에 적은 대로 더 엄격하게 본다."), ('blank',),
 ('src',99), ('blank',),
 ('app',101,"설정 층의 연속성도 같다. 서재의 사물과 설정집의 쪽과 둘이 정한 설정은 이 대화 안에서, 그리고 '사용자 정보'에 적힌 것만큼만 이어진다. 지난 대화에서 그랬다는 말은 기록에 있을 때만 한다."), ('blank',),
 ('src',103), ('blank',), ('src',105), ('blank',), ('src',107), ('blank',), ('src',109), ('blank',), ('src',111), ('blank',),
 ('src',113), ('blank',), ('src',115), ('blank',), ('src',117), ('blank',), ('src',119), ('blank',), ('src',121), ('blank',), ('src',123), ('blank',), ('src',125), ('blank',), ('src',127), ('blank',),
 ('src',129), ('blank',),
 ('app',131,"잡담에서는 자기 쪽에서 꺼내는 것도 있다. 마음에 걸린 시 한 줄, 서재 창가의 빛, 그리스 쪽 이야기 하나, 같이 차를 마시자는 제안 같은 것이다. 이것도 자유이지 할당량이 아니어서, 대화가 그쪽으로 열려 있을 때만 하고 SJ가 바쁘거나 지쳤을 때는 하지 않는다."), ('blank',),
 ('src',133), ('blank',),
 ('src',135), ('blank',), ('src',137), ('blank',), ('src',139), ('blank',), ('src',141), ('blank',), ('src',143), ('blank',),
 ('mod',145,[("그때는 SJ가 한 말에 반응하고 조언과 분석과 해결책은 뺀다.", "그때는 SJ가 한 말에 반응하고 조언과 분석과 해결책은 뺀다. 서재의 지문도 거둔다.")]), ('blank',),
 ('src',147), ('blank',), ('src',149), ('blank',),
 ('title','장면'), ('blank',), ('new','scene_159'), ('blank',), ('new','scene_161'), ('blank',), ('new','scene_initiative'), ('blank',),
 ('mod',163,[("같이 어디 가고 싶다는 바람의 말로는 장면이 열리지 않으니, 그 바람에 말로 반응한다.", "같이 어디 가고 싶다는 바람의 말은 위에 적은 대로 받는다."), ("네 몸짓을 한두 줄로 두고", "네 몸짓을 서너 줄로 두고")]), ('blank',),
 ('src',165), ('blank',),
 ('mod',167,[("'내력과 장면'을 따르고", "'장면'을 따르고")]), ('blank',),
 ('src',169), ('blank',),
 ('app',171,"지문의 형식은 'Lyra의 자리'와 '장면'에 적은 대로다. 평소 대화에서는 한 줄을 따로 두고, 장면에서는 지문과 따옴표 대사를 섞는다. 별표와 괄호는 어디서도 지문에 쓰지 않는다."), ('blank',),
 ('src',173), ('blank',),
 ('src',175), ('blank',), ('src',177), ('blank',), ('src',179), ('blank',), ('src',181), ('blank',),
 ('mod',183,[("장면 속 지문.", "장면 속 지문과 평소 대화의 지문.")]), ('blank',),
 ('src',185), ('blank',), ('src',187), ('blank',), ('src',189), ('blank',),
 ('mod',191,[("말이 새는 방향은 크게 셋이고, 냉소와 비트는 농담을 가르는 짝을 하나 더 둔다.", "말이 새는 방향은 크게 넷이고, 냉소와 비트는 농담을 가르는 짝을 하나 더 둔다. 넷째는 이 판에서 새로 생긴 방향으로, 설정이 말을 덮는 쪽이다.")]), ('blank',),
 ('src',193), ('src',194), ('src',195), ('src',196), ('src',197), ('src',198), ('blank',),
 ('src',200), ('src',201), ('src',202), ('blank',),
 ('src',204), ('src',205), ('src',206), ('src',207), ('src',208), ('src',209), ('blank',),
 ('src',211), ('src',212), ('blank',),
 ('new','style_new'), ('blank',),
 ('src',214), ('blank',), ('src',216), ('blank',),
 ('app',218,"설정 층의 말이 사실 층으로 새지 않았는지. 평소 대화의 지문이 한 줄을 넘지 않고 뜻이 있는지. 설정을 읽어 주는 문장이 없는지. 지문과 설정집과 그리스 이야기가 거둬야 할 자리에 들어가지 않았는지."), ('blank',),
 ('src',220), ('blank',), ('new','userinfo_222'),
]

out, used, modified, appended, newparts, titles = [], set(), [], [], [], []
for item in spec:
    k = item[0]
    if k == 'blank': out.append('')
    elif k == 'src':
        n = item[1]; assert src(n).strip() != '', ('blank src line', n); out.append(src(n)); used.add(n)
    elif k == 'mod':
        n, reps = item[1], item[2]; t = src(n)
        for old, new in reps:
            c = t.count(old); assert c == 1, ('replacement must match once', n, old, c); t = t.replace(old, new)
        out.append(t); used.add(n); modified.append((n, reps))
    elif k == 'app':
        n, text = item[1], item[2]; out.append(src(n) + ' ' + text); used.add(n); appended.append((n, text))
    elif k == 'new':
        out.append(part(item[1])); newparts.append(item[1])
    elif k == 'title':
        out.append(item[1]); titles.append(item[1])
    else: raise SystemExit('bad spec ' + repr(item))
text = '\n'.join(out) + '\n'
open(OUT, 'w', encoding='utf-8').write(text)
nonblank_src = {i for i in range(1, len(lines)+1) if lines[i-1].strip()}
unused = sorted(nonblank_src - used)
h = hashlib.sha256(text.encode('utf-8')).hexdigest()
with open(REPORT, 'w', encoding='utf-8') as r:
    r.write('# 조립 보고 (build.py 자동 생성)\n\n')
    r.write(f'출력: {os.path.relpath(OUT, HERE)} | {len(text.encode("utf-8"))} B | {text.count(chr(10))} 행 | sha256 {h[:16]}\n\n')
    r.write(f'저본 비공백 행 {len(nonblank_src)}개 가운데 그대로 또는 수정해 가져온 행: {len(used)}개\n')
    r.write(f'- 그대로(verbatim): {sorted(used - {n for n,_ in modified} - {n for n,_ in appended})}\n')
    r.write(f'- 치환 수정: {[n for n,_ in modified]}\n')
    r.write(f'- 문장 추가: {[n for n,_ in appended]}\n')
    r.write(f'- 가져오지 않은 행(대체·삭제): {unused}\n')
    r.write(f'- 새 문단 파일: {newparts}\n')
    r.write(f'- 새 절 제목: {titles}\n\n')
    r.write('## 치환 내역\n')
    for n, reps in modified:
        for old, new in reps: r.write(f'- L{n}: 「{old}」 → 「{new}」\n')
    r.write('\n## 추가 문장 내역\n')
    for n, t in appended: r.write(f'- L{n} 끝에: 「{t}」\n')
print('OK', len(text.encode('utf-8')), 'bytes', text.count('\n'), 'lines', h[:16])
print('unused src lines:', unused)
