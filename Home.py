import json
import streamlit as st

st.set_page_config(
    page_title='MidJourney automation',
    layout='wide'
)


class Main():
    def __init__(self):
        # Read the configs
        self.__read_configs()

        # Initialize the main content
        self.__init_main_content()

    def __read_configs(self):
        with open('configs/general.json', 'r', encoding='utf-8') as f:
            self.general_configs = json.load(f)

        with open('configs/prompts.json', 'r', encoding='utf-8') as f:
            self.prompts_configs = json.load(f)

        with open('configs/images.json', 'r', encoding='utf-8') as f:
            self.images_configs = json.load(f)

    def __init_main_content(self):
        st.title('Configurations')

        st.header('1. General settings')
        st.text_input('Bot start prompting command', key='start_command', value=self.general_configs['start_command'])
        st.text_input('Time delay between messages (in seconds)',
                      key='time_delay', value=self.general_configs['time_delay'])

        st.header('2. Prompts settings')
        st.text_input('(Optional) Prompt prefix', key='prompt_prefix', value=self.prompts_configs['prefix'])
        st.text_input('(Optional) Prompt suffix', key='prompt_suffix', value=self.prompts_configs['suffix'])

        st.header('3. Images settings')
        st.checkbox('Enable split the images', key='split_images', value=self.images_configs['split_images'])

        st.button('Save configurations', on_click=self.__save_configurations)

    def __save_configurations(self):
        # General
        self.general_configs['start_command'] = st.session_state.start_command
        self.general_configs['time_delay'] = st.session_state.time_delay

        # Prompts
        self.prompts_configs['prefix'] = st.session_state.prompt_prefix
        self.prompts_configs['suffix'] = st.session_state.prompt_suffix

        # Images
        self.images_configs['split_images'] = st.session_state.split_images

        # Save the configurations
        with open('configs/general.json', 'w', encoding='utf-8') as f:
            json.dump(self.general_configs, f, indent=4, ensure_ascii=False)

        with open('configs/prompts.json', 'w', encoding='utf-8') as f:
            json.dump(self.prompts_configs, f, indent=4, ensure_ascii=False)

        with open('configs/images.json', 'w', encoding='utf-8') as f:
            json.dump(self.images_configs, f, indent=4, ensure_ascii=False)

        st.toast(body='✅ Configurations saved successfully')


if __name__ == '__main__':
    main = Main()
