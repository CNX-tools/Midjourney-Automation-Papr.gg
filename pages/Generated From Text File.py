import os
import shutil
import sys
sys.path.append(os.getcwd())  # NOQA
import streamlit as st

import subprocess
from dotenv import load_dotenv

load_dotenv(override=True)


class TextFileGenerator():
    def __init__(self):
        self.init_app()

    def __init_uploaded_file(self):
        # Remove all the temp files
        if os.path.exists('.temp/temp_prompt.txt'):
            os.remove('.temp/temp_prompt.txt')

        print('All temp files removed')

    def __init_main_content(self):
        self.text_uploader = st.file_uploader('Upload the text file', type=['txt'], on_change=self.__init_uploaded_file)

        if self.text_uploader:
            # Save the file to .txt
            with open('.temp/temp_prompt.txt', 'wb') as f:
                f.write(self.text_uploader.getvalue())
            string_io = self.text_uploader.getvalue().decode('utf-8')
            self.current_text_area = st.text_area('Text content', value=string_io, height=300)

    def __init_sidebar(self):
        st.sidebar.button('Start | Restart prompting bot', on_click=self.__prompting_bot, use_container_width=True)

        st.sidebar.button('Start | Restart downloading bot', on_click=self.__download_bot, use_container_width=True)

    def __prompting_bot(self):
        subprocess.Popen([r'script\prompt_bot.bat'], creationflags=subprocess.CREATE_NEW_CONSOLE)
        st.success('Prompt bot started !')

    def __download_bot(self):
        subprocess.Popen([r'script\download_bot.bat'], creationflags=subprocess.CREATE_NEW_CONSOLE)
        st.success('Download bot started !')

    def init_app(self):
        shutil.rmtree('.temp', ignore_errors=True)
        os.makedirs('.temp', exist_ok=True)
        self.__init_sidebar()
        self.__init_main_content()


if __name__ == '__main__':
    TextFileGenerator()
