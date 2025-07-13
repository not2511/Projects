import gradio as gr
import fitz
from inference.infer_rw1b_adapter import generate_response

chat_history = []

def extract_text_from_pdf(file):
    with fitz.open(file.name) as doc:
        text = ""
        for page in doc:
            text += page.get_text()
    return text.strip()

def reply_fn(message, pdf_file):
    global chat_history
    if pdf_file is not None:
        message = extract_text_from_pdf(pdf_file)

    if not message.strip():
        return "", None, "<div style='color:red;'>No input or invalid file.</div>"

    chat_history.append(("user", message))
    response = generate_response(message)
    chat_history.append(("bot", response))

    html = ""
    for role, msg in chat_history:
        cls = "user" if role == "user" else "bot"
        icon = "" if role == "user" else "🤖 "
        html += f'<div class="{cls}">{icon}{msg}</div>'
    return "", None, html

def clear_fn():
    global chat_history
    chat_history = []
    return "", None, ""

with gr.Blocks(css="""
    .chatbot-container {
        max-height: 550px;
        overflow-y: auto;
        border: 1px solid #ccc;
        padding: 12px;
        border-radius: 10px;
        background-color: #f9f9f9;
        display: flex;
        flex-direction: column;
    }
    .bot {
        background-color: #eef;
        padding: 8px 12px;
        border-radius: 10px;
        margin-bottom: 8px;
        font-family: sans-serif;
    }
    .user {
        background-color: #cfe3ff;
        padding: 8px 12px;
        border-radius: 10px;
        margin-bottom: 8px;
        text-align: right;
        font-family: sans-serif;
    }
    .analyze-btn, .clear-btn {
        margin-top: 12px;
    }
""") as demo:
    gr.Markdown("## 🩺 Medical Chatbot (Symptoms & Report Analyzer)")

    with gr.Row():
        with gr.Column(scale=3):
            chat_output = gr.HTML(label="Chat", value="", elem_classes="chatbot-container")
        with gr.Column(scale=1):
            user_input = gr.Textbox(lines=3, placeholder="Type symptoms or paste report text...")
            pdf_upload = gr.File(label="Or Upload Medical Report (.pdf)", file_types=[".pdf"])
            submit_btn = gr.Button("Analyze", variant="primary", elem_classes="analyze-btn")
            clear_btn = gr.Button("Clear Chat", variant="secondary", elem_classes="clear-btn")

    submit_btn.click(reply_fn, inputs=[user_input, pdf_upload], outputs=[user_input, pdf_upload, chat_output])
    clear_btn.click(clear_fn, outputs=[user_input, pdf_upload, chat_output])

demo.launch()