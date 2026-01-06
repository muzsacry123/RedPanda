import requests
from datetime import datetime

# 配置部分
DEEPSEEK_API_KEY = ""
SERPAPI_KEY = ""                    # SerpAPI密钥

# 卦象计算
def calculate_trigram(num):
    trigrams = {
        7: ("乾", "天", "刚健"),
        6: ("兑", "泽", "悦纳"),
        5: ("离", "火", "明丽"),
        4: ("震", "雷", "震动"),
        3: ("巽", "风", "入顺"),
        2: ("坎", "水", "险陷"),
        1: ("艮", "山", "静止"),
        0: ("坤", "地", "柔顺")
    }
    remainder = num % 8
    if remainder == 0:
        remainder = 0
    return trigrams[remainder]

def get_current_hour_number():
    now = datetime.now()
    hour = now.hour
    if hour == 23 or hour == 0:
        return 1  # 子时
    elif 1 <= hour < 3:
        return 2  # 丑时
    elif 3 <= hour < 5:
        return 3  # 寅时
    elif 5 <= hour < 7:
        return 4  # 卯时
    elif 7 <= hour < 9:
        return 5  # 辰时
    elif 9 <= hour < 11:
        return 6  # 巳时
    elif 11 <= hour < 13:
        return 7  # 午时
    elif 13 <= hour < 15:
        return 8  # 未时
    elif 15 <= hour < 17:
        return 9  # 申时
    elif 17 <= hour < 19:
        return 10  # 酉时
    elif 19 <= hour < 21:
        return 11  # 戌时
    else:
        return 12  # 亥时

def calculate_hexagram(x, y, z):
    # 上卦
    a = x % 8
    upper = calculate_trigram(a)

    # 下卦
    b = (y + z) % 8
    lower = calculate_trigram(b)

    # 动爻
    hour_num = get_current_hour_number()
    c = (a + b + hour_num) % 6
    moving_yao = c if c != 0 else 6

    return {
        "upper_name": upper[0],
        "upper_symbol": upper[1],
        "upper_nature": upper[2],
        "lower_name": lower[0],
        "lower_symbol": lower[1],
        "lower_nature": lower[2],
        "moving_yao": moving_yao,
        "a": a,
        "b": b,
        "c": c,
        "hour_num": hour_num
    }

# 搜索
def serpapi_search(query):
    # 使用SerpAPI搜索
    params = {
        "engine": "google",
        "q": f"{query} 易经 解读",
        "api_key": SERPAPI_KEY,
        "hl": "zh-cn",
        "gl": "cn",
        "num": 3
    }

    response = requests.get("https://serpapi.com/search", params=params)
    results = response.json()

    search_text = ""
    for item in results.get("organic_results", [])[:2]:
        title = item.get("title", "")
        snippet = item.get("snippet", "")
        search_text += f"{title}: {snippet}\n"

    return search_text if search_text else "未找到相关资料"

# AI调用
def call_deepseek(prompt):
    #调用DeepSeek API
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": "你是易经解读专家，根据卦象和问题给出分析。"},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.3
    }

    response = requests.post(
        "https://api.deepseek.com/chat/completions",
        headers=headers,
        json=data
    )

    result = response.json()
    return result["choices"][0]["message"]["content"]


# 主程序
def main():
    print("这是Szand的易经卦象推算Agent小作业~欢迎使用捏！")
    print("输入问题 + 三个数字，俺让小D老师帮你推算卦象并解读！")

    # 检查API密钥
    if DEEPSEEK_API_KEY == "sk-你的DeepSeek_API密钥":
        print("请先配置DeepSeek API密钥")
        return

    if SERPAPI_KEY == "你的SerpAPI密钥":
        print("请先配置SerpAPI密钥")
        return

    while True:
        question = input("\n请输入问题 (输入'退出'结束): ")
        if question == "退出":
            break
        print("\n请输入三个数字 (用空格分隔): ")
        try:
            x, y, z = map(int, input().split())
        except:
            print("输入格式错误，请重新开始")
            continue
        print("推算卦象ing...")

        hexagram = calculate_hexagram(x, y, z)

        print(f"推算结果:")
        print(f"上卦: {hexagram['upper_name']} ({hexagram['upper_symbol']})")
        print(f"下卦: {hexagram['lower_name']} ({hexagram['lower_symbol']})")
        print(f"动爻: 第{hexagram['moving_yao']}爻")
        print(f"推算公式: ")
        print(f"  上卦: {x} ÷ 8 余数 {hexagram['a']} → {hexagram['upper_name']}")
        print(f"  下卦: ({y}+{z}) ÷ 8 余数 {hexagram['b']} → {hexagram['lower_name']}")
        print(f"  动爻: ({hexagram['a']}+{hexagram['b']}+时辰{hexagram['hour_num']}) ÷ 6 余数 {hexagram['c']}")

        print("\n搜索相关资料ing...")
        search_query = f"{hexagram['upper_name']}{hexagram['lower_name']}卦"
        search_result = serpapi_search(search_query)

        print("\nAI分析ing...")

        # 构建提示词
        prompt = f"""
        请分析以下易经卦象：
        
        用户问题：{question}
        
        卦象推算：
        - 上卦：{hexagram['upper_name']} ({hexagram['upper_symbol']})，特性：{hexagram['upper_nature']}
        - 下卦：{hexagram['lower_name']} ({hexagram['lower_symbol']})，特性：{hexagram['lower_nature']}
        - 动爻：第{hexagram['moving_yao']}爻
        - 完整卦象：{hexagram['upper_name']}{hexagram['lower_name']}卦
        
        搜索资料：
        {search_result}
        
        请按以下格式回答：
        1. 思考过程（简要说明分析思路）
        2. 卦象解析（解释卦象含义）
        3. 问题解答（针对用户问题的建议）
        """

        # AI解读
        answer = call_deepseek(prompt)

        print("解读结果:")
        print(answer)

        # 是否继续
        if input("\n继续咨询? (y/n): ").lower() != 'y':
            break

if __name__ == "__main__":
    main()