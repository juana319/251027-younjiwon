import streamlit as st

st.title("🎈 My new app")
st.write(
    "Let's start building! For help and inspiration, head over to [docs.streamlit.io](https://docs.streamlit.io/)."
)
import streamlit as st
from itertools import product
from math import comb

st.set_page_config(page_title="모눈종이 최단경로 계산기", layout="wide")

# ...existing code...
st.title("🎈 모눈종이 최단경로 계산기")
st.write("한 칸 크기 1, 대각선 불가. A에서 출발하여 입력한 순서대로 모든 점을 지나 B로 가는 '전체 최단경로'의 경우의 수와 경로들을 확인합니다.")

# 유틸리티: 문자열 -> 좌표 파싱
def parse_point(s, default=None):
    try:
        parts = [p.strip() for p in s.split(",")]
        if len(parts) != 2:
            return default
        return (int(parts[0]), int(parts[1]))
    except:
        return default

# 세션 상태 초기화
if "A" not in st.session_state:
    st.session_state.A = "0,0"
if "B" not in st.session_state:
    st.session_state.B = "3,2"
if "intermediates" not in st.session_state:
    st.session_state.intermediates = "1,0;2,1"
if "examples_set" not in st.session_state:
    st.session_state.examples_set = False

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### 좌표 입력")
    st.text("좌표는 정수 x,y 형식. 여러 중간점은 세미콜론(;)으로 구분합니다. 입력 순서대로 지나갑니다.")
    st.session_state.A = st.text_input("출발점 A", value=st.session_state.A)
    st.session_state.intermediates = st.text_area("중간점 (없으면 비워두기) — 예: 1,0;2,1", value=st.session_state.intermediates, height=80)
    st.session_state.B = st.text_input("도착점 B", value=st.session_state.B)

with col2:
    st.markdown("### 작업")
    if st.button("예시보기"):
        # 예시값 설정
        st.session_state.A = "0,0"
        st.session_state.intermediates = "1,0;2,1"
        st.session_state.B = "3,2"
        st.session_state.examples_set = True
        st.experimental_rerun()

    if st.button("초기화"):
        st.session_state.A = "0,0"
        st.session_state.intermediates = ""
        st.session_state.B = "0,0"
        st.experimental_rerun()

    compute = st.button("경우의 수 구하기")

st.markdown("---")

# 파싱
A = parse_point(st.session_state.A)
B = parse_point(st.session_state.B)
intermediate_str = st.session_state.intermediates.strip()
intermediates = []
if intermediate_str != "":
    for part in intermediate_str.split(";"):
        p = parse_point(part.strip())
        if p is None:
            st.error(f"중간점 입력 형식 오류: '{part}'")
            intermediates = None
            break
        intermediates.append(p)

if A is None or B is None or intermediates is None:
    st.stop()

points = [A] + intermediates + [B]
labels = ["A"] + [f"C{i+1}" for i in range(len(intermediates))] + ["B"]

# 경로 생성 유틸리티
def segment_moves(s, e):
    dx = e[0] - s[0]
    dy = e[1] - s[1]
    moves = []
    if dx > 0:
        moves += ["R"] * dx
    elif dx < 0:
        moves += ["L"] * (-dx)
    if dy > 0:
        moves += ["U"] * dy
    elif dy < 0:
        moves += ["D"] * (-dy)
    return moves  # multiset of moves; shortest path has len = |dx|+|dy|

def count_shortest_between(s, e):
    dx = abs(e[0] - s[0])
    dy = abs(e[1] - s[1])
    # 조합으로 계산: (dx+dy) choose dx
    return comb(dx + dy, dx)

# 중복 순열 생성 (멀티셋의 모든 순열) — 재귀
def multiset_permutations(moves_counts):
    # moves_counts: dict move->count
    total = sum(moves_counts.values())
    moves = list(moves_counts.keys())
    def helper(curr_counts):
        if sum(curr_counts.values()) == 0:
            yield []
            return
        for m in moves:
            if curr_counts[m] > 0:
                curr_counts[m] -= 1
                for rest in helper(curr_counts):
                    yield [m] + rest
                curr_counts[m] += 1
    yield from helper(moves_counts.copy())

# 각 세그먼트에서 가능한 모든 최소 경로(문자열 리스트) 생성, 제한 적용
MAX_PATHS_DISPLAY = 300  # 화면에 표시할 최대 전체 경로 수
MAX_PER_SEGMENT_ENUM = 200  # 각 세그먼트에서 열거 허용수 (안전)

segments = list(zip(points[:-1], points[1:]))

# 계산 버튼 동작
if compute:
    # 총 경우의 수 계산 (조합의 곱)
    total_count = 1
    segment_counts = []
    for s, e in segments:
        cnt = count_shortest_between(s, e)
        segment_counts.append(cnt)
        total_count *= cnt

    st.success(f"전체 최단거리 경우의 수: {total_count:,}")

    # 경로가 너무 많을 경우 경고
    if total_count > 1000000:
        st.warning("경우의 수가 매우 큽니다. 전체 경로를 열거하지 않고 개수만 표시합니다.")
        st.stop()

    # 각 세그먼트에 대해 실제 경로 열거 (제한 적용)
    all_segment_paths = []
    segment_enumeration_ok = True
    for idx, (s, e) in enumerate(segments):
        moves = segment_moves(s, e)
        # 카운트별로 멀티셋 구성
        counts = {}
        for m in moves:
            counts[m] = counts.get(m, 0) + 1
        cnt = segment_counts[idx]
        if cnt > MAX_PER_SEGMENT_ENUM:
            st.info(f"세그먼트 {idx+1} ({labels[idx]} -> {labels[idx+1]}) 의 경우의 수 {cnt} 가 너무 커서 열거를 제한합니다.")
            segment_enumeration_ok = False
            break
        # 열거
        seg_paths = []
        for perm in multiset_permutations(counts):
            seg_paths.append("".join(perm))
        all_segment_paths.append(seg_paths)

    if not segment_enumeration_ok:
        st.stop()

    # 전체 경로(세그먼트들의 카르테시안 곱)
    full_paths_iter = product(*all_segment_paths)
    full_paths = []
    for idx, seg_tuple in enumerate(full_paths_iter):
        # seg_tuple는 각 세그먼트의 move 문자열
        full_path = "".join(seg_tuple)
        full_paths.append(full_path)
        if len(full_paths) >= MAX_PATHS_DISPLAY:
            break

    st.info(f"열거된 전체 경로 수 (표시 한도 {MAX_PATHS_DISPLAY}): {len(full_paths)} / {total_count}")

    # 경로를 격자에 그려 출력
    grids = []
    # bounding box 계산 (전체 경로를 포함할 수 있게 각 포인트 범위로)
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    minx, maxx = min(xs), max(xs)
    miny, maxy = min(ys), max(ys)

    # 경로가 공간을 벗어날 수 없으므로 위 bbox로 충분
    pad = 1
    minx -= pad
    maxx += pad
    miny -= pad
    maxy += pad

    width = maxx - minx + 1
    height = maxy - miny + 1

    def render_path_to_grid(path_moves):
        # 초기 빈 격자
        grid = [[" ." for _ in range(width)] for _ in range(height)]
        # 위치 마크 함수
        def mark(x, y, ch):
            gx = x - minx
            gy = maxy - y  # 화면은 위가 큰 y -> index
            if 0 <= gy < height and 0 <= gx < width:
                grid[gy][gx] = f"{ch:>2}"
        # 마커: A, C1.., B
        for lab, p in zip(labels, points):
            mark(p[0], p[1], lab)

        # 따라가기
        x, y = points[0]
        for mv in path_moves:
            if mv == "R":
                x += 1
            elif mv == "L":
                x -= 1
            elif mv == "U":
                y += 1
            elif mv == "D":
                y -= 1
            # 마커가 이미 문자일 수 있으므로 우선적으로 A/C/B 유지
            gx = x - minx
            gy = maxy - y
            if 0 <= gy < height and 0 <= gx < width:
                current = grid[gy][gx].strip()
                if current in ("A", "B") or (current.startswith("C")):
                    # 보존
                    pass
                else:
                    grid[gy][gx] = " *"
        # 문자열화
        rows = ["".join(cell for cell in row) for row in grid]
        return "\n".join(rows)

    st.markdown("### 예시 경로 (텍스트 격자 표시)")
    for i, fp in enumerate(full_paths):
        st.markdown(f"**경로 #{i+1}** (moves: {fp})")
        grid_text = render_path_to_grid(fp)
        st.code(grid_text, language=None)

    if total_count > len(full_paths):
        st.markdown("...생략됨 (경우의 수가 많아 일부만 표시했습니다).")

else:
    st.info("좌표를 입력하고 '경우의 수 구하기' 버튼을 눌러 결과를 확인하세요.")