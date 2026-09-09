import gradio as gr
from backend import ask_hr_policy


def chat_with_hr(message, history):
    if not message.strip():
        return "Please enter your HR question."

    return ask_hr_policy(message)


with gr.Blocks(
    title="AI HR Policy Assistant",
    theme=gr.themes.Soft()
) as demo:

    gr.Markdown(
        """
        # 🤖 AI HR Policy Assistant

        ### Your intelligent HR policy helper

        Ask questions about:

        - 🏖️ Leave Policy
        - 💰 Salary & Benefits
        - 🕘 Attendance
        - 🏢 Workplace Rules
        - 👩‍💼 Employee Responsibilities
        - ⚠️ Disciplinary Procedures
        - 📋 Company Policies
        """
    )

    chatbot = gr.Chatbot(
        label="HR Assistant",
        height=500
    )

    message = gr.Textbox(
        label="Ask your HR question",
        placeholder="Example: How many annual leaves can an employee take?",
        lines=3
    )

    submit = gr.Button(
        "Ask HR Assistant",
        variant="primary"
    )

    clear = gr.Button("Clear Chat")

    submit.click(
        chat_with_hr,
        inputs=[message, chatbot],
        outputs=chatbot
    )

    clear.click(
        lambda: [],
        outputs=chatbot
    )


demo.launch()
