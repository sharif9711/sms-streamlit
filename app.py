import streamlit as st
import qrcode
import base64
from io import BytesIO
from supabase import create_client
import urllib.parse

st.set_page_config(page_title="📱 문자 보내기 (Streamlit)", layout="centered")

# -------------------------------
# Supabase 연결
# -------------------------------
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_ANON_KEY"]
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

st.title("📱 문자 보내기 (Streamlit 버전) 📱")
st.subheader("✉️ 문자 보내기")
st.caption("여러 줄 입력 가능")

# 입력창
msg = st.text_area("문자 내용", height=150)
phones = st.text_area("전화번호 (줄바꿈으로 여러 개)", height=120)

# -------------------------------
# QR 생성 함수
# -------------------------------
def make_qr(url):
    qr = qrcode.QRCode(box_size=10, border=2)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    return img

# -------------------------------
# Supabase 저장
# -------------------------------
def save_message_to_db(message):
    supabase.table("messages").insert({
        "id": "",
        "message": message
    }).execute()

# -------------------------------
# 버튼 클릭 처리
# -------------------------------
if st.button("📱 QR 코드 생성"):
    if not msg:
        st.error("⚠️ 문자 내용을 입력하세요.")
    else:
        st.success("QR 코드가 생성되었습니다!")

        save_message_to_db(msg)

        encoded_msg = urllib.parse.quote(msg)
        phone_list = [p.strip() for p in phones.split("\n") if p.strip()]

        if len(phone_list) == 1:
            url = f"sms:{phone_list[0]}?&body={encoded_msg}"
        else:
            joined = ",".join(phone_list)
            url = f"sms:{joined}?&body={encoded_msg}"

        img = make_qr(url)

        buf = BytesIO()
        img.save(buf, format="PNG")
        st.image(buf.getvalue(), caption="QR 코드", width=280)
