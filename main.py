import calendar
import datetime
import pandas as pd
import streamlit as st

# 페이지 기본 설정
st.set_page_config(
    page_title="수행평가 일정 관리 시스템", page_icon="📅", layout="wide"
)

# 초기 데이터 설정 (세션 상태 활용)
if "tasks" not in st.session_state:
    st.session_state.tasks = [
        {
            "id": 1,
            "title": "국어 독후감 작성",
            "start_date": datetime.date(2026, 9, 1),
            "due_date": datetime.date(2026, 9, 25),
            "rubric": "1. 논리성(40점)\n2. 문장력(30점)\n3. 분량 준수(30점)",
            "submitted_students": 18,
            "total_students": 30,
        },
        {
            "id": 2,
            "title": "수학 탐구 보고서",
            "start_date": datetime.date(2026, 9, 10),
            "due_date": datetime.date(2026, 9, 23),
            "rubric": "1. 주제 적합성(50점)\n2. 과정의 정밀성(50점)",
            "submitted_students": 25,
            "total_students": 30,
        },
    ]

# 사이드바: 사용자 역할 선택
st.sidebar.title("👤 사용자 역할 선택")
role = st.sidebar.radio("역할을 선택하세요", ["학생 화면", "교사 화면"])

st.sidebar.markdown("---")
st.sidebar.info("💡 교사 화면에서 수행평가를 등록하면 학생 화면에 실시간 반영됩니다.")

# 오늘 날짜
today = datetime.date.today()

# ==============================================================================
# 1. 학생 화면
# ==============================================================================
if role == "학생 화면":
    st.title("🎓 학생용 수행평가 일정 및 알림")

    # [알림 기능] 마감 3일 전 알림 체크
    upcoming_tasks = []
    for task in st.session_state.tasks:
        days_left = (task["due_date"] - today).days
        if 0 <= days_left <= 3:
            upcoming_tasks.append((task["title"], days_left))

    if upcoming_tasks:
        for title, days in upcoming_tasks:
            if days == 0:
                st.error(
                    f"🚨 **[긴급]** '{title}' 수행평가 마감일입니다! 오늘까지 제출하세요."
                )
            else:
                st.warning(
                    f"⏰ **[알림]** '{title}' 수행평가 제출 {days}일 남았습니다. (마감 3일 전 알림)"
                )
    else:
        st.success("🎉 현재 마감 3일 임박한 수행평가가 없습니다.")

    st.markdown("---")

    # 달력 및 전체 일정 요약 카드
    st.subheader("📅 진행 중인 수행평가 목록")

    if not st.session_state.tasks:
        st.info("등록된 수행평가가 없습니다.")
    else:
        for task in st.session_state.tasks:
            days_left = (task["due_date"] - today).days
            progress_pct = int(
                (task["submitted_students"] / task["total_students"]) * 100
            )

            # D-day 문구 설정
            if days_left > 0:
                d_day_str = f"D-{days_left} (제출일로부터 {days_left}일 남았습니다)"
            elif days_left == 0:
                d_day_str = "D-Day (오늘 마감!)"
            else:
                d_day_str = f"마감됨 (D+{abs(days_left)})"

            with st.expander(
                f"📌 **{task['title']}** | 🔥 {d_day_str}", expanded=True
            ):
                col1, col2 = st.columns([2, 1])

                with col1:
                    st.write(
                        f"**제출 기간:** {task['start_date']} ~ {task['due_date']}"
                    )
                    st.write("**평가 기준표:**")
                    st.text(task["rubric"])

                with col2:
                    st.markdown(f"**전체 제출 진행도 ({progress_pct}%)**")
                    st.progress(progress_pct / 100)
                    st.caption(
                        f"제출인원: {task['submitted_students']}명 / 총 {task['total_students']}명"
                    )

    # 🗓️ 월별 인터랙티브 달력 뷰 구현
    st.markdown("---")
    st.subheader("🗓️ 월별 수행평가 달력")

    # 연도 및 월 선택 (기본값: 오늘 연도/월 또는 등록된 일정 기준)
    col_y, col_m = st.columns(2)
    with col_y:
        selected_year = st.selectbox(
            "연도 선택", [2025, 2026, 2027], index=1
        )
    with col_m:
        selected_month = st.selectbox(
            "월 선택", list(range(1, 13)), index=8
        )  # 9월 기본 선택 (인덱스 8)

    # 파이썬 calendar 모듈을 이용한 달력 생성
import calendar

cal = calendar.monthcalendar(selected_year, selected_month)
days_name = ["월", "화", "수", "목", "금", "토", "일"]

# 날짜별 수행평가 매핑 사전(Dict) 만들기
task_map = {}
for task in st.session_state.tasks:
    # 시작일부터 마감일까지의 모든 날짜를 매핑
    curr = task["start_date"]
    end = task["due_date"]
    while curr <= end:
        if curr.year == selected_year and curr.month == selected_month:
            if curr.day not in task_map:
                task_map[curr.day] = []
            # 마감일인지 시작일인지 표시
            if curr == end:
                task_map[curr.day].append(f"🔴 [마감] {task['title']}")
            elif curr == curr == task["start_date"]:
                task_map[curr.day].append(f"🟢 [시작] {task['title']}")
            else:
                task_map[curr.day].append(f"🔵 {task['title']}")
        curr += datetime.timedelta(days=1)

# Streamlit 컬럼으로 요일 헤더 표시
header_cols = st.columns(7)
for i, d_name in enumerate(days_name):
    header_cols[i].markdown(
        f"<p style='text-align: center; font-weight: bold;'>{d_name}</p>",
        unsafe_allow_html=True,
    )

# 주별(Week) 날짜 그리드 표시
for week in cal:
    week_cols = st.columns(7)
    for i, day in enumerate(week):
        with week_cols[i]:
            if day == 0:
                st.markdown(
                    "<div style='height: 90px; background-color: #f9f9f9; border-radius: 5px; padding: 5px; color: #ccc;'></div>",
                    unsafe_allow_html=True,
                )
            else:
                # 오늘 날짜 강조 디자인
                is_today = (
                    selected_year == today.year
                    and selected_month == today.month
                    and day == today.day
                )
                bg_color = "#e8f4fd" if is_today else "#ffffff"
                border_style = (
                    "border: 2px solid #1f77b4;"
                    if is_today
                    else "border: 1px solid #e0e0e0;"
                )

                content_html = f"<div style='height: 100px; {border_style} background-color: {bg_color}; border-radius: 5px; padding: 5px; overflow-y: auto; font-size: 11px;'>"
                content_html += (
                    f"<b>{day}</b>"
                    + (" (오늘)" if is_today else "")
                    + "<br>"
                )

                if day in task_map:
                    for t_str in task_map[day]:
                        content_html += f"<span style='display: block; margin-top: 2px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;'>{t_str}</span>"

                content_html += "</div>"
                st.markdown(content_html, unsafe_allow_html=True)


# ==============================================================================
# 2. 교사 화면
# ==============================================================================
elif role == "교사 화면":
    st.title("👩‍🏫 교사용 수행평가 관리 시스템")

    tab1, tab2 = st.tabs(
        ["➕ 새 수행평가 등록", "📊 제출 및 진행도 관리"]
    )

    # TAB 1: 수행평가 등록
    with tab1:
        st.subheader("달력 및 수행평가 정보 입력")
        with st.form("add_task_form", clear_on_submit=True):
            title = st.text_input("수행평가 제목", placeholder="예: 영어 발표 평가")

            col_date1, col_date2 = st.columns(2)
            with col_date1:
                start_date = st.date_input("제출 시작일", today)
            with col_date2:
                due_date = st.date_input(
                    "마감일", today + datetime.timedelta(days=7)
                )

            rubric = st.text_area(
                "평가기준표 작성",
                placeholder="예:\n1. 내용의 충실성 (50점)\n2. 전달력 (50점)",
            )
            total_students = st.number_input(
                "전체 학생 수", min_value=1, value=30
            )

            submitted = st.form_submit_button("수행평가 등록하기")

            if submitted:
                if not title:
                    st.error("수행평가 제목을 입력해 주세요.")
                elif start_date > due_date:
                    st.error("마감일은 시작일보다 이후여야 합니다.")
                else:
                    new_id = (
                        max([t["id"] for t in st.session_state.tasks], default=0)
                        + 1
                    )
                    st.session_state.tasks.append(
                        {
                            "id": new_id,
                            "title": title,
                            "start_date": start_date,
                            "due_date": due_date,
                            "rubric": rubric,
                            "submitted_students": 0,
                            "total_students": total_students,
                        }
                    )
                    st.success(
                        f"'{title}' 수행평가가 성공적으로 등록되었습니다!"
                    )
                    st.rerun()

    # TAB 2: 제출 및 진행도 확인
    with tab2:
        st.subheader("학생 제출 현황 및 백분율 진행도")

        if not st.session_state.tasks:
            st.info("현재 등록된 수행평가가 없습니다.")
        else:
            for idx, task in enumerate(st.session_state.tasks):
                progress_pct = int(
                    (task["submitted_students"] / task["total_students"]) * 100
                )

                st.markdown(f"### 📋 {task['title']}")
                col1, col2, col3 = st.columns([2, 2, 1])

                with col1:
                    st.write(
                        f"**제출 기간:** {task['start_date']} ~ {task['due_date']}"
                    )
                    st.write(
                        f"**현재 제출 인원:** {task['submitted_students']} / {task['total_students']} 명"
                    )

                with col2:
                    st.write(f"**제출 진행도: {progress_pct}%**")
                    st.progress(progress_pct / 100)

                with col3:
                    # 제출 인원 업데이트
                    new_submitted = st.number_input(
                        "제출 인원 수정",
                        min_value=0,
                        max_value=task["total_students"],
                        value=task["submitted_students"],
                        key=f"task_{task['id']}",
                    )
                    if new_submitted != task["submitted_students"]:
                        st.session_state.tasks[idx][
                            "submitted_students"
                        ] = new_submitted
                        st.rerun()

                st.markdown("---")
