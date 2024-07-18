'''该代码用于从调用api生成的JSON文件中抽取每一个提到的藏品'''
# -*- coding: utf-8 -*-
import json
import re


# Function to extract relevant information
def extract_information_from_json(json_obj):
    extracted_info = []

    # Traverse through relate_cultural_relic_name
    for relic in json_obj.get('relate_cultural_relic_name', []):
        document_entity_name = relic.get('document_entity_name')
        cultural_relic_id = relic.get('cultural_relic_id')

        # Check if document_entity_name is not null
        if document_entity_name:
            # Find a sentence containing document_entity_name in asr_error_correction_result
            pattern = re.compile(r'[^。]*' + re.escape(document_entity_name) + r'[^。]*[。]', re.UNICODE)
            match = pattern.search(json_obj.get('asr_error_correction_result', ''))
            if match:
                extract_content = match.group(0)
                extracted_info.append({
                    "cultural_relic_id": cultural_relic_id,
                    "extract_content": extract_content
                })

    # Add extracted information to the json object
    json_obj["extract_information"] = extracted_info
    return json_obj


# Load JSON file
input_file_path = '导览语音对照表-asr纠错.json'
with open(input_file_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Process JSON objects
processed_data = [extract_information_from_json(obj) for obj in data]

# Save results to new JSON file
output_file_path = 'extracted_information.json'
with open(output_file_path, 'w', encoding='utf-8') as f:
    json.dump(processed_data, f, ensure_ascii=False, indent=4)
