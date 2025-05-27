import streamlit as st
import os
import requests
from datetime import datetime

# 과제 저장 폴더 설정
save_folder = "C:/1반"
os.makedirs(save_folder, exist_ok=True)

st.title("📄 정보 과제 제출(같은 학번 중복 제출은 불가함")

# 사용자 외부 IP 가져오기
def get_client_ip():
    try:
        response = requests.get("https://api64.ipify.org?format=json", timeout=5)
        return response.json()["ip"]
    except:
        return "알 수 없음"

# 학번 입력 받기
student_number = st.text_input("🔢 학번을 입력하세요:")

# 파일 업로드 받기
uploaded_file = st.file_uploader("📎 제출할 파일을 첨부하세요")

# 제출 버튼
if st.button("제출하기"):
    if not student_number:
        st.warning("⚠️ 학번을 입력해주세요.")
    elif not uploaded_file:
        st.warning("⚠️ 파일을 첨부해주세요.")
    else:
        # 확장자 추출 및 경로 설정
        ext = os.path.splitext(uploaded_file.name)[1]
        filename = f"{student_number}{ext}"
        save_path = os.path.join(save_folder, filename)

        # 중복 제출 확인
        if os.path.exists(save_path):
            st.error("🚫 이미 제출된 학번입니다. 중복 제출은 허용되지 않습니다.")
        else:
            # 파일 저장
            with open(save_path, "wb") as f:
                f.write(uploaded_file.read())

            # IP 및 시간 기록
            user_ip = get_client_ip()
            time_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            ip_log_path = os.path.join(save_folder, f"{student_number}_iplog.txt")

            with open(ip_log_path, "w", encoding="utf-8") as log_file:
                log_file.write(f"제출 시간: {time_str}\n")
                log_file.write(f"제출한 IP: {user_ip}\n")

            st.success("✅ 과제가 성공적으로 제출되었습니다.")
            st.info(f"📁 파일 저장 위치: {save_path}")
            st.info(f"🛡️ 제출 IP 기록 파일: {ip_log_path}")
