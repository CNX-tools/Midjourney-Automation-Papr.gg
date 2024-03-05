import streamlit as st

st.set_page_config(
    page_title='MidJourney automation',
    layout='wide'
)

st.write('# How to use this automation?')
st.write('---')
st.write('''
This automation requires 2 bots to work together:
- **Prompt bot**: This bot will enter the prompts uploaded from the .txt file. When this bot is started,
it will listen from the chat whether the "bot starting command" is entered. If it is, the bot will start entering the prompts as human being:
typing /imagine, press tab, then enter the prompt, then press enter. This process will be repeated until all prompts are entered.

Each time you change the prompts, you need to restart this bot to enter the new prompts.

- **Download bot**: This bot will listen images sent from the chat channel. When it detects an image, it will download the image to the local machine.
Furthermore, if the "split images" is enabled, it will split the original image into 4 parts.

This bot just need to be started once. It will keep listening to the chat channel and download the images automatically.
You just need to restart it whenever it is crashed or something wrong happened.
         
### 1. **Setting up the configurations at Home tab**
- In general settings, the default "bot starting command" is "start".
- In prompts settings, you can enter the prefix and suffix for the prompt.

Press the "Save configurations" button to save the configurations.

### 2. **Generated From Text File**
- First, connect to the VPS by using AnyDesk or Remote Desktop (Feel free to use the faster one).

- Second, upload the .txt file containing the prompts to the "Generated From Text File" tab.

- Third, start the "Prompt bot" by clicking the "Start | Restart prompting bot" button.

- Fourth, start the "Download bot" by clicking the "Start | Restart downloading bot" button. IF you have 
already started the bot, you don't need to restart it. It will keep listening to the chat channel.

- Fifth, press the "start automation" button to start the automation. The bot will start entering the prompts as human being.

### 3. **The images are downloaded to the local machine, in the download folder**
         ''')
st.image('./assets/images/download_folder.png')
