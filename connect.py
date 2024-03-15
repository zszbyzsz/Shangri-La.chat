
from lmdeploy.serve.openai.api_client import APIClient


        
def call_with_messages(system_prompts, user_prompt):
    server_ip = "127.0.0.1"
    server_port = "23333"
    api_client = APIClient(f'http://{server_ip}:{server_port}')
    messages = [{"role": "system", "content": system_prompts},
                {"role": "user", "content": user_prompt}]
    for item in api_client.chat_completions_v1(
        model='internlm2-chat-20b', 
        messages=messages,
        temperature=0.9,
        max_tokens=4096):
        
        chat_ans_id = item['id']
        chat_crated = item['created']
        chat_ans = item['choices']
        chat_ans_content = item['choices'][0]['message']['content']
        chat_useage = item['usage']
  
    return chat_ans_content