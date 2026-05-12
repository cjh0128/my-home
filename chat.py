import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# 解决中文乱码
plt.rcParams["font.family"] = ["SimHei", "WenQuanYi Micro Hei"]
plt.rcParams["axes.unicode_minus"] = False

st.set_page_config(page_title="全能助手｜聊天+翻译+Excel+文本处理", layout="wide")
st.title("🤖 全能工具箱：聊天AI + 翻译 + Excel报表 + 批量文本")

# 侧边栏菜单
menu = st.sidebar.radio("功能选择", [
    "💬 AI聊天助手",
    "🌐 在线翻译",
    "📊 Excel自动统计&图表",
    "📝 批量文本处理"
])

# ===================== 1. AI聊天助手 =====================
if menu == "💬 AI聊天助手":
    st.header("💬 免费聊天助手（会自动朗读）")

    # 初始化聊天记录
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # 展示历史消息
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # 输入对话
    if prompt := st.chat_input("随便问我问题..."):
        # 用户消息
        st.session_state.messages.append({"role":"user","content":prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # 简易智能回复
        reply = f"我收到你的问题：{prompt}\n你可以问我学习、工作、翻译、写文案、解题都可以。"

        with st.chat_message("assistant"):
            st.markdown(reply)
        st.session_state.messages.append({"role":"assistant","content":reply})

        # 自动语音朗读
        import streamlit.components.v1 as components
        components.html(f"""
        <script>
            let u = new SpeechSynthesisUtterance(`{reply}`);
            u.lang = "zh-CN";
            u.rate = 1;
            speechSynthesis.speak(u);
        </script>
        """, height=0)

# ===================== 2. 在线翻译 =====================
elif menu == "🌐 在线翻译":
    st.header("🌐 中英文互译 / 多语言翻译")
    text = st.text_area("输入要翻译的文字", height=180)
    choice = st.selectbox("翻译方向", [
        "中 → 英",
        "英 → 中",
        "中 → 日",
        "中 → 韩"
    ])

    if st.button("开始翻译") and text.strip():
        # 简易网页翻译调用
        import streamlit.components.v1 as components
        components.html(f"""
        <div id="res"></div>
        <script>
        async function trans(){{
            let t = `{text}`;
            let url = "";
            if("{choice}" === "中 → 英") url="https://translate.googleapis.com/translate_a/single?client=gtx&sl=zh-CN&tl=en&dt=t&q="+encodeURIComponent(t);
            if("{choice}" === "英 → 中") url="https://translate.googleapis.com/translate_a/single?client=gtx&sl=en&tl=zh-CN&dt=t&q="+encodeURIComponent(t);
            if("{choice}" === "中 → 日") url="https://translate.googleapis.com/translate_a/single?client=gtx&sl=zh-CN&tl=ja&dt=t&q="+encodeURIComponent(t);
            if("{choice}" === "中 → 韩") url="https://translate.googleapis.com/translate_a/single?client=gtx&sl=zh-CN&tl=ko&dt=t&q="+encodeURIComponent(t);
            let r = await fetch(url);
            let d = await r.json();
            document.getElementById("res").innerText = d[0][0][0];
        }}
        trans();
        </script>
        """, height=120)
        st.info("翻译结果会显示在上方")

# ===================== 3. Excel自动统计+可视化 =====================
elif menu == "📊 Excel自动统计&图表":
    st.header("📁 上传Excel，自动生成统计报表+图表")
    up_file = st.file_uploader("上传Excel文件", type=["xlsx","xls"])
    if up_file:
        df = pd.read_excel(up_file)
        st.subheader("原始数据")
        st.dataframe(df, use_container_width=True)

        st.subheader("基础统计报表")
        st.dataframe(df.describe(), use_container_width=True)

        st.subheader("缺失值统计")
        st.dataframe(df.isnull().sum(), use_container_width=True)

        # 自动绘图
        num_cols = df.select_dtypes(include=["int64","float64"]).columns.tolist()
        if len(num_cols)>=2:
            st.subheader("折线图")
            fig,ax = plt.subplots(figsize=(10,4))
            df[num_cols].plot(ax=ax)
            st.pyplot(fig)

            st.subheader("柱状图")
            fig2,ax2 = plt.subplots(figsize=(10,4))
            df[num_cols[:2]].plot(kind="bar",ax=ax2)
            st.pyplot(fig2)

# ===================== 4. 批量文本处理 =====================
elif menu == "📝 批量文本处理":
    st.header("📝 批量文本格式一键处理")
    text_in = st.text_area("粘贴多行文本", height=220)
    opt = st.radio("选择功能", [
        "去除空行",
        "每行去首尾空格",
        "全部转大写",
        "全部转小写",
        "自动加序号"
    ])

    if st.button("开始处理") and text_in:
        lines = text_in.splitlines()
        out = []
        if opt=="去除空行":
            out = [l for l in lines if l.strip()!=""]
        elif opt=="每行去首尾空格":
            out = [l.strip() for l in lines]
        elif opt=="全部转大写":
            out = [l.upper() for l in lines]
        elif opt=="全部转小写":
            out = [l.lower() for l in lines]
        elif opt=="自动加序号":
            out = [f"{i+1}. {l}" for i,l in enumerate(lines)]

        res_text = "\n".join(out)
        st.text_area("处理结果", res_text, height=220)
        st.download_button("下载为TXT文件", res_text, file_name="文本处理结果.txt")