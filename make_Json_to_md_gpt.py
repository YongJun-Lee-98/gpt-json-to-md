import json
import os
import tkinter as Tk
from tkinter import filedialog

def convert_conversation_to_markdown(conversation):
    """
    주어진 대화를 마크다운 형식으로 변환합니다.
    """
    markdown_content = f"## {conversation['title']}\n\n"

    # 각 메시지를 순회하며 마크다운 형식으로 변환
    for message_id, message_info in conversation['mapping'].items():
        if message_info.get('message'):
            # 메시지 작성자 확인
            author_role = message_info['message']['author']['role']
            author = "ChatGPT" if author_role == 'assistant' else "User"
            # 메시지 내용
            content = message_info['message']['content'].get('parts', [''])[0]
            # 마크다운에 메시지 추가
            markdown_content += f"**{author}**:\n```\n{content}\n```\n\n"
    return markdown_content

def read_json_file(file_path):
    """
    JSON 파일을 읽어서 데이터를 반환합니다.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def save_markdown_files(markdown_files, directory):
    """
    변환된 마크다운 파일들을 지정된 디렉토리에 저장합니다.
    """
    for title, markdown_content in markdown_files:  # enumerate 제거
        file_name = f"{title.replace('/', '_').replace(' ', '_')}.md"
        file_path = os.path.join(directory, file_name)
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(markdown_content)


# 저장할 디렉토리 경로 선택
save_directory = filedialog.askdirectory(title="저장할 위치를 설정해주세요")  # 디렉토리 선택 대화상자

# 선택한 디렉토리 경로 출력
print('Selected directory:', save_directory)

# JSON 파일 선택
json_file_path = filedialog.askopenfilename(
    title = "JSON 파일을 선택해주세요",
    filetypes=[('JSON Files', '*.json')])

# 선택한 파일 경로 출력
print('Selected JSON file:', json_file_path)

# JSON 데이터 읽기
json_content = read_json_file(json_file_path)

# JSON 데이터의 각 대화를 마크다운으로 변환하고, 제목도 함께 저장
markdown_files = [(conv['title'], convert_conversation_to_markdown(conv)) for conv in json_content]

# 변환된 마크다운 파일들을 저장
save_markdown_files(markdown_files, save_directory)