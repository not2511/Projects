import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel
from transformers import BitsAndBytesConfig

# Paths
base_model_id = "tiiuae/falcon-rw-1b"
adapter_path = "models/falcon-rw1b-medbot/checkpoint-178" 

# Load tokenizer
tokenizer = AutoTokenizer.from_pretrained(base_model_id, trust_remote_code=True)
tokenizer.pad_token = tokenizer.eos_token

# Load 4-bit base model
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_compute_dtype=torch.float16,
    bnb_4bit_use_double_quant=True,
    bnb_4bit_quant_type="nf4"
)

print("Loading base model...")
model = AutoModelForCausalLM.from_pretrained(
    base_model_id,
    quantization_config=bnb_config,
    device_map="auto",
    trust_remote_code=True
)

# Disable cache to avoid Falcon bug
model.config.use_cache = False

# Load LoRA adapter
print("Merging adapter...")
model = PeftModel.from_pretrained(model, adapter_path)

# Inference loop
def generate_response(user_input, max_new_tokens=256):
    prompt = f"<human>: {user_input}\n<bot>:"
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
    model.eval()
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            pad_token_id=tokenizer.eos_token_id,
            do_sample=True,
            top_k=50,
            top_p=0.95,
            temperature=0.7,
            eos_token_id=tokenizer.eos_token_id,
            early_stopping=True
        )

    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return response.split("<bot>:")[-1].strip()


if __name__ == "__main__":
    print("Medical Chatbot Ready. Ask a question.")
    while True:
        user_query = input("\nYou: ")
        if user_query.lower() in ["exit", "quit", "stop"]:
            break
        reply = generate_response(user_query)
        print(f"Bot: {reply}")
