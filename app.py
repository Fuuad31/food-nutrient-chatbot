# app.py

import streamlit as st
import os
import base64
from langchain.memory import ConversationBufferMemory

# Impor fungsi dan variabel yang dibutuhkan dari file lain
from database import init_db, save_message_to_db
from agent_logic import create_agent

# --- 1. Inisialisasi Awal ---
st.set_page_config(page_title="Chatbot Gizi Cerdas", page_icon="🥗")
st.title("Chatbot Gizi Cerdas 🥗")
st.write("Unggah gambar makanan, dan AI akan menganalisisnya untuk Anda. Anda juga bisa melanjutkan percakapan!")

# Inisialisasi database
init_db()

# --- 2. Manajemen State & Memory ---
if "memory" not in st.session_state:
    st.session_state.memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
if "session_id" not in st.session_state:
    st.session_state.session_id = os.urandom(16).hex()
if "messages" not in st.session_state:
    st.session_state.messages = []

# Buat instance agent executor
agent_executor = create_agent()

# --- 3. Logika Tampilan UI ---

# Tampilkan riwayat chat dari session state
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Terima input dari pengguna
prompt_input = st.chat_input("Tanyakan sesuatu atau unggah gambar makanan...")
uploaded_file = st.file_uploader("Unggah gambar makanan", type=["jpg", "jpeg", "png"], label_visibility="collapsed")

# Proses input jika ada
if prompt_input or uploaded_file:
    final_input = prompt_input if prompt_input else "Tolong analisis makanan di gambar ini"
    image_b64_string = None
    
    # Handle gambar yang diunggah
    if uploaded_file:
        st.image(uploaded_file, width=200)
        image_bytes = uploaded_file.getvalue()
        image_b64_string = base64.b64encode(image_bytes).decode("utf-8")
        
    if final_input:
        # Tampilkan pesan pengguna di UI
        user_display_message = final_input.split(" [gambar_disediakan:")[0]
        st.session_state.messages.append({"role": "user", "content": user_display_message})
        with st.chat_message("user"):
            st.markdown(user_display_message)
            
        # Panggil agent dan tampilkan respons AI
        with st.chat_message("assistant"):
            with st.spinner("AI sedang bekerja..."):
                agent_input = {
                    "input": final_input,
                    "chat_history": st.session_state.memory.load_memory_variables({})['chat_history']
                }
                if image_b64_string:
                    agent_input["input"] = f"Analisis makanan di gambar ini: {image_b64_string}. Pertanyaan pengguna: {prompt_input if prompt_input else ''}"

                response = agent_executor.invoke(agent_input)
                ai_response = response["output"]

                st.markdown(ai_response)
                
                # Simpan interaksi ke memori dan database
                st.session_state.memory.save_context({"input": final_input}, {"output": ai_response})
                st.session_state.messages.append({"role": "assistant", "content": ai_response})
                save_message_to_db(st.session_state.session_id, "user", user_display_message)
                save_message_to_db(st.session_state.session_id, "assistant", ai_response)