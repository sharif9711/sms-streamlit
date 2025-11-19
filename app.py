import streamlit as st
import qrcode
from io import BytesIO
import random
import string
import urllib.parse

st.set_page_config(page_title="📱 문자 보내기", page_icon="📱", layout="centered")
st.title("📱 문자 보내기 (Streamlit 버전) 📱")


# ------------------------------------------------
# 메시지를 key로 저장하는 함수
# ------------------------------------------------
def generate_key(length=6):
    chars = string.ascii_uppercase + string.digits
    return "".join(random.choice(chars) for _ in range(length))


if "msg_store" not in st.session_state:
    st.session_state.msg_store = {}   # {key: 메시지}


# ------------------------------------------------
# PC 화면: 입력 → QR 생성
# ------------------------------------------------
if "key" not in st.query_params:

    st.subheader("핸드폰 번호 입력")
    phones_text = st.text_area(
        "번호를 줄바꿈으로 입력하세요",
        height=140,
        placeholder="01012345678\n01098765432"
    )

    st.subheader("문자 내용")
    msg_text = st.text_area(
        "여러 줄 입력 가능",
        height=200,
        placeholder="문자 내용을 입력하세요"
    )

    if st.button("QR 코드 생성"):
        phones = [v.strip() for v in phones_text.split("\n") if v.strip()]

        if not phones:
            st.error("핸드폰 번호를 입력하세요.")
            st.stop()

        if not msg_text.strip():
            st.error("문자 내용을 입력하세요.")
            st.stop()

        # 메시지 저장 후 key 부여
        key = generate_key()
        st.session_state.msg_store[key] = msg_text

        p_param = urllib.parse.quote(",".join(phones))

        # QR 주소 (아주 짧음, 절대 깨지지 않음)
        final_url = f"https://aisw00011.streamlit.app/?p={p_param}&key={key}"

        st.subheader("📲 QR 코드")
        qr = qrcode.make(final_url)
        buf = BytesIO()
        qr.save(buf)
        st.image(buf.getvalue(), width=260)

        st.write("📌 아래 주소를 복사해서 사용할 수도 있습니다.")
        st.code(final_url)


# ------------------------------------------------
# 모바일 화면: key로 메시지 복구 → 버튼 생성
# ------------------------------------------------
else:
    st.subheader("📨 문자 보내기")

    p = st.query_params.get("p", [""])[0]
    key = st.query_params.get("key", [""])[0]

    phones = p.split(",")

    # key로 메시지 복구
    msg = st.session_state.msg_store.get(key, "")

    if not msg:
        st.error("메시지를 불러올 수 없습니다. QR 코드를 다시 생성하세요.")
        st.stop()

    # ------------------------------
    # 전체 문자 보내기 버튼
    # ------------------------------
    st.write(f"### 📢 전체에게 문자 보내기 ({len(phones)}명)")

    isiPhone = "iphone" in st.request.headers["User-Agent"].lower()

    if isiPhone:
        sms_url = f"sms:/open?addresses={','.join(phones)}&body={urllib.parse.quote(msg)}"
    else:
        sms_url = f"sms:{','.join(phones)}?body={urllib.parse.quote(msg)}"

    st.markdown(
        f"""
        <a href="{sms_url}" style="
            display:block;
            background:#88BFFF;
            padding:24px;
            border-radius:20px;
            text-align:center;
            font-size:28px;
            color:white;
            text-decoration:none;
            font-weight:700;
            margin-bottom:20px;
        ">📢 전체에게 보내기</a>
        """,
        unsafe_allow_html=True
    )

    st.write("---")

    # ------------------------------
    # 개별 문자 보내기 버튼
    # ------------------------------
    st.write("### 📱 개별 보내기")

    for i, pnum in enumerate(phones):
        sms_url = f"sms:{pnum}?body={urllib.parse.quote(msg)}"

        st.markdown(
            f"""
            <a href="{sms_url}" style="
                display:block;
                background:#C9B6E4;
                padding:22px;
                border-radius:18px;
                text-align:center;
                font-size:26px;
                color:white;
                text-decoration:none;
                font-weight:700;
                margin-bottom:18px;
            ">📨 [{i+1}] {pnum}</a>
            """,
            unsafe_allow_html=True
        )
