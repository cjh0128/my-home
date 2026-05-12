import streamlit as st

from volcenginesdkarkruntime import Ark
st.title("我的小小ai")



# 初始化聊天记录
if "messages" not in st.session_state:
    st.session_state.messages = []

# 显示历史消息
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 接收用户提问
if prompt := st.chat_input("有什么可以帮你的？"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 调用AI接口生成回复
    with st.chat_message("assistant"):
        with st.spinner("正在思考..."):
            response = client.chat.completions.create(
                model="doubao-lite-4k",  # 选免费的模型就行
                messages=st.session_state.messages
            )
            reply = response.choices[0].message.content
            st.markdown(reply)
    st.session_state.messages.append({"role": "assistant", "content": reply})