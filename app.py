import streamlit as st
import json
import os
import random

# --- 1. 页面配置与美学风格 ---
st.set_page_config(page_title="斯比的五十坨屎", layout="wide")

st.markdown("""
    <style>
    /* 1. 强制整个 App 的文字颜色，防止夜间模式变白 */
    .stApp, .stMarkdown, p, span, div, h1, h2, h3, h4, h5, h6 {
        color: #3e2723 !important;
    }

    .stApp {
        background-image: url("https://www.transparenttextures.com/patterns/old-map.png"); 
        background-color: #f4ece1;
    }

    /* 2. 档案盒子的样式 */
    .paper-box {
        background: rgba(255, 255, 255, 0.6);
        padding: 25px;
        border: 2px solid #5d4037;
        border-radius: 15px;
        box-shadow: 5px 5px 15px rgba(0,0,0,0.1);
        /* 这里的文字也要强制加深 */
        color: #3e2723 !important;
    }

    /* 3. 按钮文字颜色单独设置（因为按钮背景是深的，字要浅色才看得清） */
    .stButton>button {
        width: 100%;
        background-color: #5d4037 !important;
        color: #f4ece1 !important; /* 按钮内部文字保持浅色 */
        font-weight: bold;
        border-radius: 8px;
        border: none;
        padding: 10px;
    }
    
    /* 4. 解决展开框 (expander) 的标题颜色 */
    .streamlit-expanderHeader {
        color: #5d4037 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. 存档系统工具 ---
SAVE_FILE = "save_data.json"

def load_save():
    if os.path.exists(SAVE_FILE):
        try:
            with open(SAVE_FILE, 'r') as f:
                return json.load(f)
        except:
            return None
    return None

def save_game(idx, order):
    with open(SAVE_FILE, 'w') as f:
        json.dump({"idx": idx, "order": order}, f)

# --- 3. 核心初始化逻辑 (防崩溃版) ---
if 'initialized' not in st.session_state or 'order' not in st.session_state:
    # 加载案件数据
    try:
        with open('cases.json', 'r', encoding='utf-8') as f:
            st.session_state.all_cases = json.load(f)
    except FileNotFoundError:
        st.error("❌ 找不到 cases.json 文件！")
        st.stop()

    # 读取存档或新建随机顺序
    saved_data = load_save()
    if saved_data and "order" in saved_data and len(saved_data["order"]) == len(st.session_state.all_cases):
        st.session_state.order = saved_data["order"]
        st.session_state.idx = saved_data.get("idx", 0)
    else:
        indices = list(range(len(st.session_state.all_cases)))
        random.shuffle(indices)
        st.session_state.order = indices
        st.session_state.idx = 0
        save_game(st.session_state.idx, st.session_state.order)

    st.session_state.initialized = True
    st.session_state.answer_correct = False

# --- 4. 游戏界面展示 ---
st.title(" 斯比的五十坨屎：机密调查档案")

# 开场背景介绍
with st.expander("📖 案情前传：", expanded=(st.session_state.idx == 0)):
    st.markdown("""
    <div style="font-style: italic; color: #5d4037; line-height: 1.6;">
        你刚刚结束了五天的借住生活回到家中。<br>
        本以为有<b>自动饮水机</b>和<b>定时喂食器</b>的加持，你的小猫<b>斯比</b>会过得安稳，<br>
        谁知推开门的那一刻，迎接你的是遍布全屋的“惊喜”……<br><br>
        作为唯一的调查员，你必须根据样本（💩）的形态、颜色和位置，
        推断出这失踪的 120 小时里，斯比到底背着你干了什么。
    </div>
    """, unsafe_allow_html=True)

# 检查游戏是否通关
if st.session_state.idx >= len(st.session_state.all_cases):
    st.balloons()
    st.success("🏆 终极真相：你已经查清了所有 50 份样本！斯比欣慰的看着你，准备等你夸她“真棒”。")
    if st.button("重置档案，再次调查"):
        if os.path.exists(SAVE_FILE): os.remove(SAVE_FILE)
        st.session_state.clear()
        st.rerun()
    st.stop()

# 获取当前案件数据
current_case_pos = st.session_state.order[st.session_state.idx]
case = st.session_state.all_cases[current_case_pos]

# 进度条
st.write(f"**当前档案进度：{st.session_state.idx + 1} / {len(st.session_state.all_cases)}**")

# 展示区布局
col_cat, col_text = st.columns([1, 2])

with col_cat:
    # 加载斯比立绘
    if os.path.exists("cat_head.png"):
        st.image("cat_head.png")
    else:
        st.write("🐱 (等待斯比立绘 cat_head.png)")

with col_text:
    # 动态展示背景场景图
    scene_file = f"{case['location']}.png"
    if os.path.exists(scene_file):
        st.image(scene_file, use_container_width=True)
    else:
        st.info(f"📍 现场位置：{case['location']}")

    st.markdown(f"""
    <div class="paper-box">
        <h2 style='color: #5d4037;'>{case['name']}</h2>
        <p style='font-size: 18px;'><b>调查记录：</b>{case['camera']}</p>
        <p style='font-size: 24px;'><b>物证：💩</b> {', '.join(case['evidence'])}</p>
    </div>
    """, unsafe_allow_html=True)

    st.write("---")

    # 选项区
    if not st.session_state.answer_correct:
        st.write("#### 🔍 请点击你的推断：")
        # 这种布局让按钮更整齐
        for i, opt in enumerate(case['options']):
            if st.button(opt, key=f"btn_{st.session_state.idx}_{i}"):
                if i == case['correct']:
                    st.session_state.answer_correct = True
                    st.rerun()
                else:
                    st.error("❌ 斯比正在失望的看着你。")
    else:
        # 答对后的显示
        st.success(f"✅ 斯比骄傲的看着你！\n\n{case['wiki']}")
        if st.button("归档，前往下一处现场 ➡"):
            st.session_state.idx += 1
            st.session_state.answer_correct = False
            save_game(st.session_state.idx, st.session_state.order)
            st.rerun()

# 侧边栏辅助功能
with st.sidebar:
    st.write("### 调查工具箱")
    if st.button("🗑️ 销毁并重置进度"):
        if os.path.exists(SAVE_FILE): os.remove(SAVE_FILE)
        st.session_state.clear()
        st.rerun()
