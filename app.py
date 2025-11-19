import streamlit as st
import qrcode
from io import BytesIO
import base64
import urllib.parse

st.set_page_config(page_title="📱 문자 보내기", page_icon="📱", layout="centered")

st.title("📱 문자 보내기 📱")


# ------------------------------------------------
# PC 화면: 번호 + 문자 입력 → QR 생성
# ------------------------------------------------
if "p" not in st.query_params and "m" not in st.query_params:

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

        if len(phones) == 0:
            st.error("핸드폰 번호를 입력하세요.")
            st.stop()

        if not msg_text.strip():
            st.error("문자 내용을 입력하세요.")
            st.stop()

        # 🔥 URL-safe Base64 인코딩
        encoded_msg = base64.urlsafe_b64encode(msg_text.encode("utf-8")).decode().rstrip("=")

        p_param = urllib.parse.quote(",".join(phones))
        m_param = encoded_msg  # 안전한 문자열

        final_url = (
            "https://aisw00011.streamlit.app"
            f"/?p={p_param}&m={m_param}"
        )

        st.subheader("📲 QR 코드")
        qr = qrcode.make(final_url)
        buf = BytesIO()
        qr.save(buf)
        st.image(buf.getvalue(), width=260)

        st.write("📌 아래 주소를 복사해서 사용할 수도 있습니다.")
        st.code(final_url)


# ------------------------------------------------
# 모바일 화면: 문자 보내기 버튼 생성
# ------------------------------------------------
else:
    st.subheader("📨 문자 보내기")

    p = st.query_params.get("p", [""])[0]
    m = st.query_params.get("m", [""])[0]

    phones = p.split(",")

    # 🔥 URL-safe Base64 디코딩 (깨짐 없음)
    pad_len = 4 - (len(m) % 4)
    if pad_len != 4:
        m += "=" * pad_len

    decoded_msg = base64.urlsafe_b64decode(m.encode()).decode()

    # ------------------------------
    # 전체 문자 보내기 버튼
    # ------------------------------
    st.write(f"### 📢 전체에게 문자 보내기 ({len(phones)}명)")

    isiPhone = "iphone" in st.request.headers["User-Agent"].lower()

    if isiPhone:
        sms_url = f"sms:/open?addresses={','.join(phones)}&body={urllib.parse.quote(decoded_msg)}"
    else:
        sms_url = f"sms:{','.join(phones)}?body={urllib.parse.quote(decoded_msg)}"

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
        sms_url = f"sms:{pnum}?body={urllib.parse.quote(decoded_msg)}"

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


