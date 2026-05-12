import streamlit as st

st.title("我的第一个聊天机器人")

# 初始化聊天记录
if "messages" not in st.session_state:
    st.session_state.messages = []

# 显示聊天记录
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 接收用户输入
if prompt := st.chat_input("你想说点什么？"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 机器人回复（这里是简单的 echo）
    response = f"你说的是：{prompt}"
    with st.chat_message("assistant"):
        st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})