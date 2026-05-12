import streamlit as st
import streamlit.components.v1 as components

# 页面设置
st.set_page_config(page_title="我的AI助手", page_icon="🤖")
st.title("我的专属AI助手 🤖")

# 初始化聊天记录
if "messages" not in st.session_state:
    st.session_state.messages = []

# 显示历史消息
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 接收用户输入
if prompt := st.chat_input("有什么可以帮你的？"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 这里先做一个简单的回复，后面可以换成真正的AI接口
    with st.chat_message("assistant"):
        with st.spinner("正在思考..."):
            reply = f"收到啦！你刚才说的是：「{prompt}」。\n\n（我现在是一个基础版助手，接入大模型后就能真正帮你干活啦！）"
            st.markdown(reply)
    st.session_state.messages.append({"role": "assistant", "content": reply})

    # 文字转语音（用浏览器自带功能，不用额外装库）
    components.html(f"""
    <script>
        function speak() {{
            const utterance = new SpeechSynthesisUtterance("{reply}");
            utterance.lang = "zh-CN";
            utterance.rate = 1;
            window.speechSynthesis.speak(utterance);
        }}
        speak();
    </script>
    """, height=0)