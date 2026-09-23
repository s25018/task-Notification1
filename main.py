import datetime
import pandas as pd
import streamlit as st
from streamlit_calendar import calendar

# 1. 페이지 기본 설정
st.set_page_config(
    page_title="💖 공주님의 수행평가 시크릿 다이어리 ✨",
    page_icon="👑",
    layout="wide",
)

# 2. 핑크 공주 & 반짝반짝 커스텀 CSS 적용
st.markdown(
    """
    <style>
    /* 전체 배경을 파스텔 핑크와 로맨틱 파스텔 톤으로 설정 */
    .stApp {
        background: linear-gradient(135deg, #fff0f5 0%, #ffe4e1 50%, #ffd1dc 100%);
        font-family: 'Comic Sans MS', 'Chalkboard SE', 'Nanum Gothic', sans-serif;
    }

    /* 사이드바 핑크 드레스업 */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #ffe4e1 0%, #ffc0cb 100%) !important;
        border-right: 2px dashed #ff69b4;
    }

    /* 제목 텍스트 반짝이 & 핑크 폰트 */
    h1, h2, h3 {
        color: #d81b60 !important;
        text-shadow: 2px 2px 4px #ffb6c1;
    }

    /* 버튼 스타일 - 하트 핫핑크 젤리 버튼 */
    .stButton > button {
        background: linear-gradient(45deg, #ff69b4, #ff1493) !important;
        color: white !important;
        font-weight: bold !important;
        border-radius: 20px !important;
        border: 2px solid #fff !important;
        box-shadow: 0 4px 15px rgba(255, 105, 180, 0.4) !important;
        transition: all 0.3s ease !important;
    }
    .stButton > button:hover {
        transform: scale(1.05) rotate(-1deg) !important;
        box-shadow: 0 6px 20px rgba(255, 20, 147, 0.6) !important;
    }

    /* Expander / 카드 박스 공주풍 경계선 */
    div[data-aria-expanded="true"], div[data-testid="stExpander"] {
        background-color: rgba(255, 255, 255, 0.8) !important;
        border: 2px solid #ffb6c1 !important;
        border-radius: 18px !important;
        box-shadow: 0 8px 16px rgba(255, 182, 193, 0.3) !important;
    }

    /* 알림 박스 핑크 커스텀 */
    .stAlert {
        border-radius: 15px !important;
        border: 2px solid #ff69b4 !important;
    }

    /* 진행도 바 색상을 핫핑크로 변경 */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #ffb6c1 0%, #ff1493 100%) !important;
    }

    /* 탭 디자인 스타일링 */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #fff0f5;
        border-radius: 15px 15px 0 0;
        color: #d81b60;
        font-weight: bold;
        padding: 10px 20px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #ff69b4 !important;
        color: white !important;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# 초기 데이터 설정 (세션 상태 활용)
if "tasks" not in st.session_state:
    st.session_state.tasks = [
        {
            "id": 1,
            "title": "👑 국어 독후감 작성",
            "start_date": datetime.date(2026, 9, 1),
            "due_date": datetime.date(2026, 9, 25),
            "rubric": "1. 논리성(40점) ✨\n2. 문장력(30점) 💖\n3. 분량 준수(30점) 🎀",
            "submitted_students": 18,
            "total_students": 30,
            "color": "#ff69b4",  # 핫핑크
        },
        {
            "id": 2,
            "title": "🎀 수학 탐구 보고서",
            "start_date": datetime.date(2026, 9, 10),
            "due_date": datetime.date(2026, 9, 23),
            "rubric": "1. 주제 적합성(50점) ✨\n2. 과정의 정밀성(50점) 💎",
            "submitted_students": 25,
            "total_students": 30,
            "color": "#ba55d3",  # 퍼플 핑크
        },
    ]

# 사이드바: 사용자 역할 선택
st.sidebar.title("👑 공주님/왕자님 메뉴")
role = st.sidebar.radio(
    "✨ 화면 모드를 선택해 주세요", ["🎀 학생 화면", "👩‍🏫 교사 화면"]
)

st.sidebar.markdown("---")
st.sidebar.info("💖 교사 화면에서 수행평가를 올리면 학생 화면에 실시간으로 보석처럼 나타나요! ✨")

# 오늘 날짜
today = datetime.date.today()


# 달력 이벤트 데이터 변환
def get_calendar_events():
    events = []
    for task in st.session_state.tasks:
        end_date_inclusive = task["due_date"] + datetime.timedelta(days=1)
        events.append(
            {
                "title": f"✨ {task['title']}",
                "start": task["start_date"].strftime("%Y-%m-%d"),
                "end": end_date_inclusive.strftime("%Y-%m-%d"),
                "backgroundColor": task.get("color", "#ff69b4"),
                "borderColor": "#ffffff",
            }
        )
    return events


# 달력 기본 옵션
calendar_options = {
    "editable": False,
    "selectable": True,
    "headerToolbar": {
        "left": "prev,next today",
        "center": "title",
        "right": "dayGridMonth",
    },
    "initialView": "dayGridMonth",
    "locale": "ko",
}

# ==============================================================================
# 1. 학생 화면
# ==============================================================================
if role == "🎀 학생 화면":
    st.title("💖 ✨ 공주님의 수행평가 시크릿 다이어리 ✨ 💖")

    # [알림 기능] 마감 3일 전 알림
    upcoming_tasks = []
    for task in st.session_state.tasks:
        days_left = (task["due_date"] - today).days
        if 0 <= days_left <= 3:
            upcoming_tasks.append((task["title"], days_left))

    if upcoming_tasks:
        for title, days in upcoming_tasks:
            if days == 0:
                st.error(
                    f"🚨 **[공주님 비상!]** '{title}' 마감 당일이에요! 서둘러 제출해 주세요! 👑"
                )
            else:
                st.warning(
                    f"⏰ **[반짝 알림]** '{title}' 제출이 {days}일 남았어요! ✨ (마감 3일 전 핑크 알림)"
                )
    else:
        st.success("🎉✨ 지금은 마감 임박한 수행평가가 없어요! 여유로운 시간 보내세요 💖")

    st.markdown("---")

    # 달력 영역
    st.subheader("🗓️ ✨ 핑크 달력으로 보는 수행평가 일정")
    events = get_calendar_events()
    calendar(events=events, options=calendar_options, key="student_calendar")

    st.markdown("---")

    # 수행평가 상세 리스트
    st.subheader("📋 🎀 진행 중인 수행평가 & 제출 달성도 💖")

    if not st.session_state.tasks:
        st.info("✨ 등록된 수행평가가 없어요.")
    else:
        for task in st.session_state.tasks:
            days_left = (task["due_date"] - today).days
            progress_pct = int(
                (task["submitted_students"] / task["total_students"]) * 100
            )

            if days_left > 0:
                d_day_str = f"D-{days_left} (제출일까지 {days_left}일 남았어요! ✨)"
            elif days_left == 0:
                d_day_str = "D-Day (오늘이 마지막 날이에요! 🚨)"
            else:
                d_day_str = f"마감됨 (D+{abs(days_left)}) 🎀"

            with st.expander(
                f"✨ **{task['title']}** | 💖 {d_day_str}", expanded=True
            ):
                col1, col2 = st.columns([2, 1])

                with col1:
                    st.write(
                        f"**📅 제출 기간:** {task['start_date']} ~ {task['due_date']}"
                    )
                    st.write("**📝 평가 기준표:**")
                    st.text(task["rubric"])

                with col2:
                    st.markdown(f"**💖 전체 제출 달성률 ({progress_pct}%)**")
                    st.progress(progress_pct / 100)
                    st.caption(
                        f"🌸 제출한 친구들: {task['submitted_students']}명 / 총 {task['total_students']}명"
                    )

# ==============================================================================
# 2. 교사 화면
# ==============================================================================
elif role == "👩‍🏫 교사 화면":
    st.title("👩‍🏫 ✨ 교사 공주님의 수행평가 시크릿 센터 ✨ 💖")

    tab1, tab2, tab3, tab4 = st.tabs(
        [
            "🗓️ 핑크 달력 보기",
            "➕ 🎀 새 수행평가 등록",
            "✏️ ✨ 수정 & 삭제",
            "📊 💖 제출 현황 관리",
        ]
    )

    # TAB 1: 전체 달력
    with tab1:
        st.subheader("🗓️ 핑크 달력 스케줄 보기 ✨")
        events = get_calendar_events()
        calendar(events=events, options=calendar_options, key="teacher_calendar")

    # TAB 2: 수행평가 등록
    with tab2:
        st.subheader("➕ ✨ 새로운 수행평가 올려주기 🎀")
        with st.form("add_task_form", clear_on_submit=True):
            title = st.text_input("👑 수행평가 제목", placeholder="예: 🎀 영어 발표 수행평가")

            col_date1, col_date2, col_color = st.columns([2, 2, 1])
            with col_date1:
                start_date = st.date_input("🌸 시작일", today)
            with col_date2:
                due_date = st.date_input(
                    "👑 마감일", today + datetime.timedelta(days=7)
                )
            with col_color:
                color = st.color_picker("✨ 달력 리본 색상", "#ff69b4")

            rubric = st.text_area(
                "📝 세부 평가 기준표",
                placeholder="예:\n1. 발표 완성도 (50점) ✨\n2. 태도 및 전달력 (50점) 💖",
            )
            total_students = st.number_input(
                "🌸 전체 학생 수", min_value=1, value=30
            )

            submitted = st.form_submit_button("💖 예쁘게 등록하기 ✨")

            if submitted:
                if not title:
                    st.error("🎀 수행평가 제목을 꼭 입력해 주세요!")
                elif start_date > due_date:
                    st.error("👑 마감일은 시작일보다 나중이어야 해요!")
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
                            "color": color,
                        }
                    )
                    st.success(
                        f"✨ '{title}' 수행평가가 핑크 달력에 샤방하게 등록되었어요! 💖"
                    )
                    st.rerun()

    # TAB 3: 수정/삭제
    with tab3:
        st.subheader("✏️ ✨ 등록된 수행평가 단장하기 & 삭제하기 🎀")

        if not st.session_state.tasks:
            st.info("🌸 변경할 수행평가가 없어요.")
        else:
            task_titles = [t["title"] for t in st.session_state.tasks]
            selected_title = st.selectbox("💖 선택해 주세요", task_titles)

            task_idx = next(
                i
                for i, t in enumerate(st.session_state.tasks)
                if t["title"] == selected_title
            )
            target_task = st.session_state.tasks[task_idx]

            st.markdown("---")

            col_edit, col_delete = st.columns([3, 1])

            with col_edit:
                st.write(f"### ✏️ '{target_task['title']}' 수정하기 ✨")
                with st.form(key=f"edit_form_{target_task['id']}"):
                    edit_title = st.text_input("👑 제목", value=target_task["title"])

                    c1, c2, c3 = st.columns([2, 2, 1])
                    with c1:
                        edit_start = st.date_input("🌸 시작일", value=target_task["start_date"])
                    with c2:
                        edit_due = st.date_input("👑 마감일", value=target_task["due_date"])
                    with c3:
                        edit_color = st.color_picker(
                            "✨ 색상", value=target_task.get("color", "#ff69b4")
                        )

                    edit_rubric = st.text_area("📝 평가 기준표", value=target_task["rubric"])
                    edit_total = st.number_input(
                        "🌸 전체 학생 수", min_value=1, value=target_task["total_students"]
                    )

                    update_btn = st.form_submit_button("💖 수정 완료하기 ✨")

                    if update_btn:
                        st.session_state.tasks[task_idx]["title"] = edit_title
                        st.session_state.tasks[task_idx]["start_date"] = edit_start
                        st.session_state.tasks[task_idx]["due_date"] = edit_due
                        st.session_state.tasks[task_idx]["rubric"] = edit_rubric
                        st.session_state.tasks[task_idx]["total_students"] = edit_total
                        st.session_state.tasks[task_idx]["color"] = edit_color
                        st.success("✨ 정보가 예쁘게 변경되었어요! 💖")
                        st.rerun()

            with col_delete:
                st.write("### 🗑️ 삭제하기 💔")
                if st.button("💔 수행평가 삭제하기", key=f"del_btn_{target_task['id']}"):
                    del st.session_state.tasks[task_idx]
                    st.success(f"✨ '{target_task['title']}' 항목이 삭제되었어요.")
                    st.rerun()

    # TAB 4: 진행도 관리
    with tab4:
        st.subheader("📊 💖 학생들의 제출 현황 현황판 ✨")

        if not st.session_state.tasks:
            st.info("🌸 등록된 수행평가가 없어요.")
        else:
            for idx, task in enumerate(st.session_state.tasks):
                progress_pct = int(
                    (task["submitted_students"] / task["total_students"]) * 100
                )

                st.markdown(f"### ✨ {task['title']}")
                col1, col2, col3 = st.columns([2, 2, 1])

                with col1:
                    st.write(
                        f"**📅 기간:** {task['start_date']} ~ {task['due_date']}"
                    )
                    st.write(
                        f"**🌸 제출한 학생:** {task['submitted_students']} / {task['total_students']} 명"
                    )

                with col2:
                    st.write(f"**💖 달성률: {progress_pct}%**")
                    st.progress(progress_pct / 100)

                with col3:
                    new_submitted = st.number_input(
                        "🌸 제출 학생 수 변경",
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
