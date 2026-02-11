import json
import time
import os
import sys
import random

# 终端颜色配置
YELLOW = '\033[93m'
GREEN = '\033[92m'
RED = '\033[91m'
BOLD = '\033[1m'
CYAN = '\033[96m'
MAGENTA = '\033[95m'
RESET = '\033[0m'

def typing_print(text, delay=0.02):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def load_game_data():
    if not os.path.exists('cases.json'):
        print(f"{RED}错误：找不到 cases.json！{RESET}")
        return None
    with open('cases.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        random.shuffle(data) 
        return data

def get_rank(score, total):
    ratio = score / total
    if ratio == 1.0:
        return f"{MAGENTA}【传说级·猫屎鉴别大师】{RESET}", "斯比甘拜下风，你已经看穿了它所有的“内幕”。"
    elif ratio >= 0.8:
        return f"{CYAN}【金牌·首席铲屎官】{RESET}", "你对斯比的肠胃了如指掌，家里非常安全。"
    elif ratio >= 0.6:
        return f"{YELLOW}【资深·铲屎工】{RESET}", "你基本能分清哪坨是惊喜，哪坨是惊吓。"
    else:
        return f"{RED}【新手·喂猫机器】{RESET}", "加油啊！你这样斯比会很难办的。"

def start_game():
    all_data = load_game_data()
    if not all_data: return

    os.system('clear' if os.name == 'posix' else 'cls')
    print(f"{YELLOW}{BOLD}========================================{RESET}")
    print(f"{YELLOW}{BOLD}    💩 斯比的五十坨屎：首席鉴定师 💩    {RESET}")
    print(f"{YELLOW}{BOLD}========================================{RESET}\n")

    score = 0
    total = len(all_data)

    for i, case in enumerate(all_data):
        # 这里的进度也改成了 💩
        print(f"\n{BOLD}💩 采样进度: {i+1}/{total}{RESET}")
        time.sleep(0.5)
        
        # 氛围描述
        print(f"{CYAN}{case['camera']}{RESET}")
        time.sleep(0.8)
        
        # 核心改动：证据图标变为 💩
        print(f"📍 发现位置: {case['location']}")
        print(f"🔍 核心💩: {', '.join(case['evidence'])}")
        print("\n请开始你的逻辑推理：")
        
        for j, opt in enumerate(case['options']):
            clean_opt = opt.split('. ')[-1].replace('(√)', '').strip()
            print(f"  ({j + 1}) {clean_opt}")
            
        while True:
            choice = input(f"\n提交你的判断 (1-{len(case['options'])}): ").strip()
            if choice.isdigit() and 0 < int(choice) <= len(case['options']):
                if int(choice) - 1 == case['correct']:
                    print(f"\n{GREEN}✅ 真相大白！这是：【{case['name']}】{RESET}")
                    print(f"📖 {case['wiki']}")
                    score += 1
                    break
                else:
                    print(f"\n{RED}❌ 逻辑错误！斯比的这坨💩没那么简单，再想想。{RESET}")
                    break 
            else:
                print("请输入数字编号。")
        
        input(f"\n{YELLOW}[按回车键处理下一坨 💩]{RESET}")
        os.system('clear' if os.name == 'posix' else 'cls')

    # 最终报告
    print(f"{MAGENTA}{BOLD}========================================{RESET}")
    print(f"{MAGENTA}{BOLD}           💩 终极鉴定结案报告 💩         {RESET}")
    print(f"{MAGENTA}{BOLD}========================================{RESET}\n")
    
    rank_name, rank_desc = get_rank(score, total)
    typing_print(f"鉴定成功率: {BOLD}{score}{RESET} / {total}")
    typing_print(f"获得称号: {rank_name}")
    typing_print(f"专家评价: {rank_desc}")
    print(f"\n{MAGENTA}========================================{RESET}")
    typing_print("斯比在远方欣慰地打了个饱嗝。")

if __name__ == "__main__":
    start_game()