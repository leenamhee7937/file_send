import streamlit as st
import os

# 저장할 폴더 경로 (윈도우 기준)
save_folder = "C:/1ban"

# 폴더가 없으면 생성
os.makedirs(save_folder, exist_ok=True)

st.title("📄 과제 제출")

# 학번 입력 받기
student_number = st.text_input("🔢 학번을 입력하세요:")

# 파일 업로드
uploaded_file = st.file_uploader("📎 파일을 첨부하세요")

# 제출 버튼
if st.button("제출하기"):
    if not student_number:
        st.warning("⚠️ 학번을 입력해주세요.")
    elif not uploaded_file:
        st.warning("⚠️ 파일을 첨부해주세요.")
    else:
        # 저장 경로 설정
        file_extension = os.path.splitext(uploaded_file.name)[1]
        save_path = os.path.join(save_folder, f"{student_number}{file_extension}")

        # 파일 저장
        with open(save_path, "wb") as f:
            f.write(uploaded_file.read())

        st.success(f"✅ 파일이 저장되었습니다: {save_path}")
