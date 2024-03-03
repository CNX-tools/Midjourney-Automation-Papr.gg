import os
import shutil
import sys
sys.path.append(os.getcwd())  # NOQA
import streamlit as st

import subprocess
import zipfile
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

    def __download_selected_folder(self):
        # Current selected folder
        selected_folder = st.session_state.folder_by_days
        print(f"==>> selected_folder: {selected_folder}")

        # Zip the folder
        shutil.make_archive(f'download/{selected_folder}', 'zip', f'download/{selected_folder}')

        # Download the zip file
        st.download_button(
            label='Download the selected folder',
            data=open(f'download/{selected_folder}.zip', 'rb'),
            file_name=f'{selected_folder}.zip',
            use_container_width=True,
        )

    def _download_images_folder(self):
        st.markdown('### Download the images')

        folder_by_days = os.listdir('download')
        folder_by_days = [x for x in folder_by_days if os.path.isdir(f'download/{x}')]
        st.selectbox('Select the folder by days', options=folder_by_days, key='folder_by_days')
        st.button('Zip the folder', on_click=self.__download_selected_folder)

    def __init_main_content(self):
        st.markdown('### Generated From Text File')
        self.text_uploader = st.file_uploader('Upload the text file', type=['txt'], on_change=self.__init_uploaded_file)

        if self.text_uploader:
            # Save the file to .txt
            with open('.temp/temp_prompt.txt', 'wb') as f:
                f.write(self.text_uploader.getvalue())
            string_io = self.text_uploader.getvalue().decode('utf-8')
            self.current_text_area = st.text_area('Text content', value=string_io, height=300)

        # Download the images folder
        self._download_images_folder()

    def __init_sidebar(self):
        st.sidebar.button('Start | Restart prompting bot', on_click=self.__prompting_bot, use_container_width=True)

        st.sidebar.button('Start | Restart downloading bot', on_click=self.__download_bot, use_container_width=True)

    def __prompting_bot(self):
        if not os.path.exists('.temp/temp_prompt.txt'):
            st.error('Please upload the text file first !')
            return
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
