import streamlit as st
import json
import os
import random

# --- 1. 初始化设置 ---
st.set_page_config(page_title="斯比的五十坨屎", layout="wide")

SAVE_FILE = "save_data.json" # 存档文件名

# --- 2. 存档系统逻辑 ---
def load_save():
    """读取存档：进度和打乱后的题目顺序"""
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, 'r') as f:
            return json.load(f)
    return None

def save_game(idx, order):
    """保存进度"""
    with open(SAVE_FILE, 'w') as f:
        json.dump({"idx": idx, "order": order}, f)

# --- 3. 初始化数据与随机逻辑 (健壮修复版) ---
if 'initialized' not in st.session_state:
    with open('cases.json', 'r', encoding='utf-8') as f:
        all_cases = json.load(f)
    
    saved_data = load_save()
    
    # 这里增加了对 "order" 键的检查，防止 KeyError
    if saved_data and isinstance(saved_data, dict) and "order" in saved_data:
        st.session_state.order = saved_data["order"]
        st.session_state.idx = saved_data.get("idx", 0)
    else:
        # 如果没有存档，或者存档格式不对，就重新洗牌
        case_indices = list(range(len(all_cases)))
        random.shuffle(case_indices) 
        st.session_state.order = case_indices
        st.session_state.idx = 0
        # 立即创建一个正确的存档文件
        save_game(st.session_state.idx, st.session_state.order)
    
    st.session_state.all_cases = all_cases
    st.session_state.initialized = True
    st.session_state.answer_correct = False

    # --- 这一步最关键：根据当前的进度索引，从打乱的顺序里取出对应的题目数据 ---
# 如果因为刷新导致 session_state 丢了，强制重新触发一次初始化逻辑
if 'order' not in st.session_state or 'all_cases' not in st.session_state:
    st.session_state.initialized = False # 强制标记为未初始化
    # 这里直接重定向或者手动调用一次加载逻辑
    with open('cases.json', 'r', encoding='utf-8') as f:
        st.session_state.all_cases = json.load(f)
    
    saved_data = load_save()
    if saved_data and "order" in saved_data:
        st.session_state.order = saved_data["order"]
        st.session_state.idx = saved_data.get("idx", 0)
    else:
        case_indices = list(range(len(st.session_state.all_cases)))
        random.shuffle(case_indices)
        st.session_state.order = case_indices
        st.session_state.idx = 0
    st.session_state.initialized = True
    st.session_state.answer_correct = False

# 现在再执行这两行就安全了
current_case_pos = st.session_state.order[st.session_state.idx]
case = st.session_state.all_cases[current_case_pos]

# --- 确保这两行之后，才是你显示“案发现场：{case['location']}”的代码 ---

# --- 4. 界面布局  ---
st.markdown("""
    <style>
    .stApp { background-color: #f4ece1; background-image: url("https://www.transparenttextures.com/patterns/old-map.png"); }
    .paper-box { background: rgba(255, 255, 255, 0.6); padding: 20px; border: 2px solid #5d4037; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.title("📜 斯比的五十坨💩")
# --- 游戏背景介绍区 ---
with st.expander("📖 案情前传：", expanded=True):
    st.markdown(f"""
    <div style="font-style: italic; color: #5d4037; line-height: 1.6;">
        你去朋友家借住了五天，
        本以为有<b>自动饮水机</b>和<b>定时喂食器</b>的加持，你的小猫<b>斯比</b>会过得安稳，
        谁知推开门的那一刻，迎接你的是遍布全屋的“惊喜”……
        <br><br>
        家里全是斯比的“杰作（💩）” 请根据你找到的样本（💩）推断出斯比到底做了什么。
    </div>
    """, unsafe_allow_html=True)
st.write(f"**当前档案进度：{st.session_state.idx + 1} / {len(st.session_state.all_cases)}** (已存档)")

# 重置游戏按钮（删档）
if st.sidebar.button("🗑️ 销毁所有档案（重置游戏）"):
    if os.path.exists(SAVE_FILE):
        os.remove(SAVE_FILE)
    st.session_state.clear()
    st.rerun()

# --- 5. 核心展示区 ---
col_cat, col_text = st.columns([1, 2])

with col_cat:
    if os.path.exists("cat_head.png"):
        st.image("cat_head.png")

with col_text:
    st.markdown(f"""
    <div class="paper-box">
        <h3>案发现场：{case['location']}</h3>
        <p><b>记录：</b>{case['camera']}</p>
        <p style='font-size: 24px;'><b>物证：💩</b> {', '.join(case['evidence'])}</p>
    </div>
    """, unsafe_allow_html=True)

    st.write("---")

    if not st.session_state.answer_correct:
        for i, opt in enumerate(case['options']):
            if st.button(opt, key=f"btn_{st.session_state.idx}_{i}"):
                if i == case['correct']:
                    st.session_state.answer_correct = True
                    st.rerun()
                else:
                    st.error("逻辑谬误！斯比不认可这个推断。")
    else:
        st.success(f"✅ 真相大白！\n\n{case['wiki']}")
        if st.button("保存进度并前往下一案 ➡"):
            st.session_state.idx += 1
            st.session_state.answer_correct = False
            # 执行【存档】
            save_game(st.session_state.idx, st.session_state.order)
            st.rerun()
