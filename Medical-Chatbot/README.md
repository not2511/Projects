
#  Medical Chatbot: Symptom Checker & Report Analyzer

This is an AI-powered medical chatbot built using the Falcon-RW-1B model fine-tuned via QLoRA. It can:

- Analyze symptoms and suggest possible medical conditions with probabilities
- Interpret text-based or PDF-formatted medical reports (e.g., blood, kidney, urine tests)
- Ask follow-up questions to refine diagnosis
- Display results via an interactive Gradio chatbot interface

---

##  Project Structure: What Each File Does

```

Medical-Chatbot/
├── app.py                           # Gradio UI: chatbot interface
├── requirements.txt                 # Python dependencies
├── README.md                        # This documentation
├── training/
│   └── train\_rw1b\_qlora.py          # Fine-tunes Falcon-RW-1B using QLoRA
├── inference/
│   └── infer\_rw1b\_adapter.py        # Loads fine-tuned model + generates predictions
├── models/
│   └── falcon-rw1b-medbot/          # Contains LoRA adapter & tokenizer
├── data/
│   ├── symptom\_diagnosis.jsonl      # 500 symptom-diagnosis training examples
│   └── blood\_reports.jsonl          # 200 report-summary examples

````

---

##  Model & Architecture

- **Base Model**: [`tiiuae/falcon-rw-1b`](https://huggingface.co/tiiuae/falcon-rw-1b) — a 1.3B parameter causal language model
- **Fine-tuning Method**: QLoRA (Quantized Low-Rank Adapter)
- **Quantization**: 4-bit using `bitsandbytes`
- **Adapter Type**: LoRA (r=8, alpha=32, dropout=0.05)
- **Training**:
  - 700 total samples (500 symptom, 200 reports)
  - Trained on GTX 1650 Mobile (4GB VRAM)
  - 2 epochs with gradient accumulation

---

##  Installation Guide

1. **Clone and set up environment**:
   ```bash
   git clone https://github.com/not2511/Projects
   cd Medical-Chatbot
   python -m venv medchat_env
   .\medchat_env\Scripts\activate


2. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

3. (Optional) If using GPU:

   * Install CUDA (e.g., CUDA 11.8)
   * Make sure `torch` detects your GPU with `torch.cuda.is_available()`

---

## ▶ How to Run the Project (Step-by-Step)

### 1. Fine-tune the model

**File**: `training/train_rw1b_qlora.py`

```bash
python training/train_rw1b_qlora.py
```

**What it does**:

* Loads the Falcon-RW-1B base model
* Applies LoRA adapters via QLoRA
* Trains for 2 epochs on combined symptom/report dataset

**Output**:
Saves adapter to:

```
models/falcon-rw1b-medbot/checkpoint-178/
```

---

### 2. Test Inference via Terminal

**File**: `inference/infer_rw1b_adapter.py`

```bash
python inference/infer_rw1b_adapter.py
```

**What it does**:

* Loads the quantized base model + LoRA adapter
* Accepts symptom or report text from terminal
* Returns diagnoses and follow-up questions

---

### 3. Run Chatbot Web Interface

**File**: `app.py`

```bash
python app.py
```

**What it does**:

* Launches a Gradio UI at `http://127.0.0.1:7860`
* Accepts:

  * Typed symptom/report input
  * PDF medical report uploads
* Displays chat with:

  * Scrollable history
  * Analyze and Clear buttons

---

##  Training Data Format

Each `.jsonl` file line contains:

```json
{"instruction": "I have fever and cough", "output": "Possible: flu (70%), COVID-19 (20%)..."}
```

* `symptom_diagnosis.jsonl` — symptom → diagnosis
* `blood_reports.jsonl` — report → summary

---

##  Issues Faced and Fixes

| Issue                            | Fix                                                    |
| -------------------------------- | ------------------------------------------------------ |
| Falcon model crashed on GTX 1650 | Used 4-bit QLoRA and gradient accumulation             |
| Incomplete bot responses         | Added `eos_token_id` and `early_stopping=True`         |
| Slow inference                   | Reduced `max_new_tokens`, used FP16, no\_grad          |
| Chat cutoff in UI                | Increased max-height + scrollable `.chatbot-container` |


---

##  Example Queries

* “I have sharp pain in lower right abdomen”
* “Hemoglobin 9.2, WBC 13k, creatinine 1.8 — analyze this blood test”
* Upload a PDF medical report and hit **Analyze**

---


