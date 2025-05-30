import torch
from mistral_common.protocol.instruct.messages import SystemMessage, UserMessage
from mistral_common.protocol.instruct.request import ChatCompletionRequest
from mistral_common.tokens.tokenizers.mistral import MistralTokenizer
from huggingface_hub import hf_hub_download
from transformers import AutoModelForCausalLM

# Load system prompt
def load_system_prompt(repo_id: str, filename: str) -> str:
    file_path = hf_hub_download(repo_id=repo_id, filename=filename)
    with open(file_path, "r") as file:
        system_prompt = file.read()
    return system_prompt

# Initialize model and tokenizer
model_id = "mistralai/Devstral-Small-2505"
tekken_file = hf_hub_download(repo_id=model_id, filename="tekken.json")
SYSTEM_PROMPT = load_system_prompt(model_id, "SYSTEM_PROMPT.txt")
tokenizer = MistralTokenizer.from_file(tekken_file)
model = AutoModelForCausalLM.from_pretrained(model_id, torch_dtype=torch.float16)

# Test conversation
user_input = "Write a Python function to compute the Fibonacci sequence."
chat_request = ChatCompletionRequest(
    messages=[
        SystemMessage(content=SYSTEM_PROMPT),
        UserMessage(content=user_input),
    ]
)
tokenized = tokenizer.encode_chat_completion(chat_request)
input_ids = torch.tensor([tokenized.tokens], dtype=torch.long)

# Generate response
output = model.generate(
    input_ids=input_ids,
    max_new_tokens=1000,
    do_sample=True,
    temperature=0.7,
)
decoded_output = tokenizer.decode(output[0][len(tokenized.tokens):])
print(decoded_output)