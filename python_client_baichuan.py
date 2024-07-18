from openai import OpenAI

client = OpenAI(
    api_key="your_api_key",
    base_url="https://api.baichuan-ai.com/v1/",
)

completion = client.chat.completions.create(
    model="Baichuan4",
    messages=[{
        "content": "今天天气怎么样？使用json格式输出",
        "role": "user"
    }
    ],
    tools=[{
        "type": "function",
        "function": {
            "name": "get_current_weather",
            "description": "获取当前位置天气",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "城市或者省，如北京"
                    },
                    "format": {
                        "type": "string",
                        "description": "要使用的温度单位。从用户位置推断。"
                    }
                },
                "required": [
                    "location",
                    "format"
                ]
            }
        }
    }]
)
print(completion.choices[0].message)




