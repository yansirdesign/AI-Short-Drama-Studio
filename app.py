import streamlit as st
import openai

# --- 1. 界面配置 ---
st.set_page_config(page_title="幻影智造 VisionForge AI", layout="wide", initial_sidebar_state="expanded")

# 自定义 CSS 美化
st.markdown("""
    <style>
    .main { background-color: #F8FAFC; }
    .stTabs [data-baseweb="tab-list"] { gap: 24px; }
    .stTabs [data-baseweb="tab"] { height: 50px; white-space: pre-wrap; background-color: #FFFFFF; border-radius: 10px 10px 0 0; gap: 1px; padding: 10px 20px; }
    .stTabs [aria-selected="true"] { background-color: #EEF2FF; border-bottom: 2px solid #4F46E5; }
    div[data-testid="stExpander"] { border: none; background-color: white; box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1); border-radius: 12px; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. 侧边栏配置 ---
with st.sidebar:
    st.title("🎬 幻影智造 v1.0")
    st.caption("AI短剧/动态漫一站式创作中台")
    st.divider()
    
    api_key = st.text_input("DeepSeek API Key", type="password", help="请从 DeepSeek 官网获取")
    base_url = "https://api.deepseek.com" # 默认使用 DeepSeek
    
    st.divider()
    user_input = st.text_area("✨ 灵感描述", placeholder="例如：一个关于赛博木兰在未来城市复仇的故事，风格冷冽，画面要有电影感...", height=150)
    creative_mode = st.radio("创作类型", ["短剧 (Live Action)", "动态漫 (Anime)"])
    
    generate_btn = st.button("🚀 生成全案", type="primary")

# --- 3. 核心生成逻辑 ---
def call_ai(prompt):
    client = openai.OpenAI(api_key=api_key, base_url=base_url)
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    return response.choices[0].message.content

# --- 4. 任务提示词库 ---
PROMPTS = {
    "script": f"你是一个资深短剧编剧。请根据用户灵感：'{user_input}'。生成：1.吸睛选题；2.逻辑严密的4幕剧本（含场次、对白、动作描写）。",
    "visual": "基于剧本，为即梦/Nanobanana Pro生成：1.主角三视图提示词(英文)；2.核心场景提示词(英文)。要求：电影感，8k，高画质。",
    "video": "为可灵/Seedance 2.0生成5个镜头的视频提示词(英文)。要求：必须包含高动态指令（如camera pan, motion, wind），并注明每个镜头的旁白。",
    "audio": "根据剧本推荐：1.BGM风格建议；2.关键音效(SFX)时间点建议。"
}

# --- 5. 主页面内容展示 ---
if generate_btn:
    if not api_key:
        st.error("❌ 请在侧边栏输入 API Key 后再开始。")
    elif not user_input:
        st.warning("⚠️ 请先输入你的灵感。")
    else:
        with st.spinner("正在构思中... AI 导演正在为您努力工作..."):
            try:
                # 步骤1：生成剧本
                script_res = call_ai(PROMPTS["script"])
                
                tab1, tab2, tab3, tab4 = st.tabs(["📝 剧本选题", "🎨 视觉/三视图", "📹 视频分镜", "🎵 音频建议"])
                
                with tab1:
                    st.markdown("### 📝 剧本方案")
                    st.write(script_res)
                
                with tab2:
                    visual_res = call_ai(f"基于以下剧本生成即梦/Nanobanana提示词：\n{script_res}\n\n要求格式：{PROMPTS['visual']}")
                    st.markdown("### 🎨 角色与场景设定")
                    st.info("提示：请直接复制以下 Prompt 到即梦或 Nanobanana Pro 使用")
                    st.write(visual_res)
                    
                with tab3:
                    video_res = call_ai(f"基于以下剧本生成可灵/Seedance视频提示词：\n{script_res}\n\n要求格式：{PROMPTS['video']}")
                    st.markdown("### 📹 视频生成指令")
                    st.warning("提示：这些提示词已增加动态指令，适合可灵 1.5 或 Seedance 2.0")
                    st.write(video_res)
                    
                with tab4:
                    audio_res = call_ai(f"基于以下剧本生成音频方案：\n{script_res}\n\n要求格式：{PROMPTS['audio']}")
                    st.markdown("### 🎵 音频与 BGM 规划")
                    st.write(audio_res)
                    
            except Exception as e:
                st.error(f"发生错误: {str(e)}")
else:
    # 默认展示页面
    st.image("https://img.freepik.com/free-vector/abstract-digital-technology-background-with-network-connection-lines_1017-25552.jpg", use_column_width=True)
    st.markdown("""
    ### 欢迎使用 幻影智造
    本软件将帮助你快速完成从**灵感**到**视频全方案**的跨越。
    1. 在左侧填写灵感
    2. 点击生成全案
    3. 复制对应的 Prompt 到即梦/可灵进行制作
    """)

# --- 6. 环境依赖文件 (重要) ---
# 提示：在 GitHub 仓库中还需要创建一个 requirements.txt 文件，内容如下：
# streamlit
# openai
