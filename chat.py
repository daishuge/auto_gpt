import openai 
import time 
import os

pandora=False  # 控制是否使用 Fake API
history = []  # 存储对话历史的列表
openai.api_key = os.getenv("openai_api_key")

# 读取角色信息
with open("role.txt", "r", encoding="utf-8") as f:
    role = f.read()

def get_total_tokens(messages):     #获取令牌数
    return sum(len(message['content'].split()) * 1.5 for message in messages)

def truncate_history(history, max_tokens=1500):     #缩减历史记录
    while get_total_tokens(history) > max_tokens:
        history.pop(0)

def gpt_api(query, max, if_print, tem, history, rol=role):
    """
    使用 OpenAI 的 ChatCompletion 创建聊天响应。
    
    参数:
        - query: 用户的查询内容
        - max: 响应的最大令牌数
        - if_print: 控制是否在控制台打印每个响应片段
        - tem: 生成响应的温度（创造性）
        - history: 对话历史记录(列表)
        - rol: 角色信息(字符串)
    """
    history.append({'role': 'user', 'content': query})
    truncate_history(history)

    messages = [
        {"role": "system", "content": rol}
    ]
    messages.extend(history)

    response = openai.ChatCompletion.create(
        model='gpt-4',
        messages=messages,
        temperature=tem,
        max_tokens=max,
        stream=True
    )

    result = ""

    for chunk in response:
        if 'choices' in chunk and 'delta' in chunk['choices'][0]:
            chunk_msg = chunk['choices'][0]['delta'].get('content', '')
            result += chunk_msg

            if if_print:
                print(chunk_msg, end='', flush=True)
                time.sleep(0.05)

    print("\n\n")
    history.append({'role': 'assistant', 'content': result})
    return result

while True:
    user_input = input("You: ")

    if user_input == "exit":
        break
        
    reply = gpt_api(user_input, 1000, True, 1, history)