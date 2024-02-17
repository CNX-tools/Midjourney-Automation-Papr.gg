import streamlit as st


class TextFileGenerator():
    def __init__(self):
        self.init_app()

    def __init_main_content(self):
        self.text_uploader = st.file_uploader('Upload the text file', type=['txt'])

        if self.text_uploader:
            string_io = self.text_uploader.getvalue().decode('utf-8')
            st.text_area('Text content', value=string_io, height=300)

    def __init_sidebar(self):
        st.sidebar.write('🤖 Bot status')

        # TODO: Check the bot status and change the text accordingly by adding icon
        st.sidebar.write('- Prompting Bot')
        st.sidebar.write('- Downloading Bot')

        st.sidebar.write('---')

        st.sidebar.button('Start | Restart prompting bot', on_click=self.__prompting_bot, use_container_width=True)

        st.sidebar.button('Start | Restart downloading bot', on_click=self.__download_bot, use_container_width=True)

    def __prompting_bot(self):
        pass

    def __download_bot(self):
        pass

    def init_app(self):
        self.__init_sidebar()
        self.__init_main_content()


if __name__ == '__main__':
    TextFileGenerator()
