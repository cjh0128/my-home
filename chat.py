import streamlit as st
from translate import Translator
st.title("我的小小ai")
text = st.text_area("输入要翻译的中文：", "你好，Streamlit！")
target_lang = st.selectbox("目标语言", ["英语", "日语", "韩语"])

lang_map = {"英语": "en", "日语": "ja", "韩语": "ko"}
if st.button("翻译"):
    translator = Translator(to_lang=lang_map[target_lang])
    result = translator.translate(text)
    st.success(f"翻译结果：{result}")