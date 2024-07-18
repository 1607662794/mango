# -*- coding: utf-8 -*-
# 该文档用于调用api进行asr纠错。
from http import HTTPStatus
import dashscope
import os
import json
from tqdm import tqdm
import re


# Function to call Dashscope API
def process_text_with_dashscope(prompt_text):
    # qwen-max，网页版千问背后的模型：容易修饰过头
    # qwen-turbo，超大规模语言模型：效果还行，不大稳定
    # qwen-plus，超大规模语言模型增强版：效果还行
    resp = dashscope.Generation.call(
        model='qwen-plus',
        api_key=os.getenv('DASHSCOPE_API_KEY'),
        prompt=prompt_text
    )
    if resp.status_code == HTTPStatus.OK:
        return resp.output.text
    else:
        print(f"Error {resp.code}: {resp.message}")
        return None


def extract_json_from_response(response_text):
    # 使用正则表达式提取json部分
    match = re.search(r'```json\n(.*?)\n```', response_text, re.DOTALL)
    if match:
        json_content = match.group(1)
        return json.loads(json_content)
    else:
        print("JSON content not found in the response")
        return None

# Function to process each json object
def process_json_object(json_obj):
    prompt_text = f"""
    # 任务：
        ## ASR纠错。
    
    # 对应能力与角色：
        ## 作为一位专业的大规模语言模型引导专家，我希望您在这项具体任务中展现出卓越的洞察力、精准的信息提取能力和强大的错误纠正能力。对输入的Json文件内容进行ASR纠错，并返回新的Json对象。
    
    # 标准操作流程：
        1.找到给定Json对象中的"file_content"关键字。
        2.对"file_content"关键字对应的内容进行ASR纠错。
        3.为Json对象新增"asr_error correction_result"关键字。
        4.将纠正后的文本作为"asr_error correction_result"关键字对应的内容。
        5.将修正的Json内容以Json格式输出，确保格式清晰、准确。
        
    # 注意事项
        1.原来的JSON对象不要改变，只是新增了一组键值对。
        2.该任务解决的Json文件内容整体属于文物与博物馆学。
        3.输入的Json对象中，除了"file_content"关键字对应内容外，其余部分均已经过人工校核，因此在进行纠正时，可以参考其余部分，如"document_entity_name": "持杖蒿里俑"，而"file_content"中却被转写成了"池丈蒿藜涌”，因此，修正时，应将其修正为"持杖蒿里俑"。
        
    # 示例：
        ## 输入：
            将信息以JSON格式输出，确保格式清晰、准确。JSON格式如下：
            {{
            "file_path": "湖南人-doc\\1099\\1099_原文.docx",
            "relate_cultural_relic_name": [
                {{
                    "document_entity_name": "架鹰胡人俑",
                    "formal_entity_name": "青瓷驾鹰俑",
                    "cultural_relic_id": "1802548233990312008"
                }},
                {{
                    "document_entity_name": "牵驼胡人俑",
                    "formal_entity_name": "陶牵骆驼俑",
                    "cultural_relic_id": "1788047018564784134"
                }},
                {{
                    "document_entity_name": "持杖蒿里俑",
                    "formal_entity_name": "隋大业六年墓胡人持杖陶俑",
                    "cultural_relic_id": "1788047170511835224"
                }}
            ],
            "file_content": "驾鹰胡人俑、牵驼胡人俑、池丈蒿藜涌。胡永是一种较为特殊的陪葬俑，目前已知的绝大部分胡永出自隋唐墓葬，尤其是盛唐墓。相比唐三彩胡永的盛名，岳州窑烧造的胡永影响力小，受关注程度不高，但他也烧造了大量的胡勇，姿态各异，品类繁多。您现在看到的这件嫁衣胡人俑高鼻深目，满脸络腮胡须，头戴幞头，身着圆领窄袖套袍，腰上系带，脚穿长筒靴，左手贴在身上，右胳膊上则立着一只鹰。再看这件千驼胡人俑，塑造的也是惟妙惟肖，他右手挽起，身体前倾，似在拽着骆驼前行，骆驼载着货物，温顺可爱。这件持杖蒿里有浓眉高鼻、络腮胡须，身着交领广袖短袍，腰束带长裤，束腿脚，穿草鞋，双手持杖而立，神情严肃。南方地区的胡勇以湖南出土居多，反映了隋唐时期湖南作为海上丝绸之路陆路中转站的重要性。",
            "classification": "湖南人"
        }}
        ## 输出：
            {{
            "file_path": "湖南人-doc\\1099\\1099_原文.docx",
            "relate_cultural_relic_name": [
                {{
                    "document_entity_name": "架鹰胡人俑",
                    "formal_entity_name": "青瓷驾鹰俑",
                    "cultural_relic_id": "1802548233990312008"
                }},
                {{
                    "document_entity_name": "牵驼胡人俑",
                    "formal_entity_name": "陶牵骆驼俑",
                    "cultural_relic_id": "1788047018564784134"
                }},
                {{
                    "document_entity_name": "持杖蒿里俑",
                    "formal_entity_name": "隋大业六年墓胡人持杖陶俑",
                    "cultural_relic_id": "1788047170511835224"
                }}
            ],
            "file_content": "驾鹰胡人俑、牵驼胡人俑、池丈蒿藜涌。胡永是一种较为特殊的陪葬俑，目前已知的绝大部分胡永出自隋唐墓葬，尤其是盛唐墓。相比唐三彩胡永的盛名，岳州窑烧造的胡永影响力小，受关注程度不高，但他也烧造了大量的胡勇，姿态各异，品类繁多。您现在看到的这件嫁衣胡人俑高鼻深目，满脸络腮胡须，头戴幞头，身着圆领窄袖套袍，腰上系带，脚穿长筒靴，左手贴在身上，右胳膊上则立着一只鹰。再看这件千驼胡人俑，塑造的也是惟妙惟肖，他右手挽起，身体前倾，似在拽着骆驼前行，骆驼载着货物，温顺可爱。这件持杖蒿里有浓眉高鼻、络腮胡须，身着交领广袖短袍，腰束带长裤，束腿脚，穿草鞋，双手持杖而立，神情严肃。南方地区的胡勇以湖南出土居多，反映了隋唐时期湖南作为海上丝绸之路陆路中转站的重要性。",
            "asr_error correction_result": "驾鹰胡人俑、牵驼胡人俑、持杖蒿里俑。胡俑是一种较为特殊的陪葬俑，目前已知的绝大部分胡俑出自隋唐墓葬，尤其是盛唐墓。相比唐三彩胡俑的盛名，岳州窑烧造的胡俑影响力小，受关注程度不高，但他也烧造了大量的胡俑，姿态各异，品类繁多。您现在看到的这件架鹰胡人俑高鼻深目，满脸络腮胡须，头戴幞头，身着圆领窄袖套袍，腰上系带，脚穿长筒靴，左手贴在身上，右胳膊上则立着一只鹰。再看这件牵驼胡人俑，塑造的也是惟妙惟肖，他右手挽起，身体前倾，似在拽着骆驼前行，骆驼载着货物，温顺可爱。这件持杖蒿里俑浓眉高鼻、络腮胡须，身着交领广袖短袍，腰束带长裤，束腿脚，穿草鞋，双手持杖而立，神情严肃。南方地区的胡俑以湖南出土居多，反映了隋唐时期湖南作为海上丝绸之路陆路中转站的重要性。",
            "classification": "湖南人"
        }}
                
    # 需要处理的输入：
        将信息以JSON格式输出，确保格式清晰、准确。JSON格式如下：
        {json.dumps(json_obj, ensure_ascii=False)}
    """

    result = process_text_with_dashscope(prompt_text)
    if result:
        return extract_json_from_response(result)
    else:
        return None


def process_json_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    processed_data = []
    for item in tqdm(data[:12], desc="Processing items", total=len(data)):
        processed_item = process_json_object(item)
        if processed_item:
            processed_data.append(processed_item)

    with open('music_to_text/导览语音对照表-asr纠错.json', 'w', encoding='utf-8') as file:
        json.dump(processed_data, file, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    process_json_file('music_to_text/导览语音对照表.json')
