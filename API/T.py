from flask import Flask, jsonify, request
from flask_cors import CORS
import os
from openai import OpenAI

app = Flask(__name__)
CORS(app)  # 解决跨域问题

# 初始化 OpenAI 客户端（使用百炼API）
client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

# 模拟聊天历史
chat_history = []

@app.route('/')
def index():
    """API 根路径，返回状态信息"""
    return jsonify({
        "status": "0",
        "message": "API is running",
        "version": "1.0.0"
    })

@app.route('/chat', methods=['POST'])
def chat():
    """接收用户消息并返回AI回复"""
    data = request.json
    user_message = data.get('content')
    
    if not user_message:
        return jsonify({
            "status": "1",
            "message": "Missing content parameter"
        }), 400
    
    # 添加用户消息到历史
    chat_history.append({"role": "user", "content": user_message})
    
    try:
        # 调用大模型生成回复
        completion = client.chat.completions.create(
            model="qwen-plus",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                *chat_history
            ],
            # 根据模型要求调整参数
            # extra_body={"enable_thinking": False},
        )
        
        # 提取回复内容
        ai_reply = completion.choices[0].message.content
        
        # 添加AI回复到历史
        chat_history.append({"role": "assistant", "content": ai_reply})
        
        return jsonify({
            "status": "0",
            "message": "Success",
            "data": {
                "content": ai_reply,
                "timestamp": str(completion.created)
            }
        })
    
    except Exception as e:
        return jsonify({
            "status": "2",
            "message": f"Error: {str(e)}"
        }), 500

if __name__ == '__main__':
    app.run(debug=True)