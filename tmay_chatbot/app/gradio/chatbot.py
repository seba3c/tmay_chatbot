import gradio as gr

from tmay_chatbot.app.base import GradioApp
from tmay_chatbot.chatbot.base import TmayChatbot
from tmay_chatbot.chatbot.factory import get_chatbot


class TmayChatbotGradioApp(GradioApp):
    def __init__(self, chatbot: TmayChatbot):
        self.chatbot = chatbot

    def format_context(self, context):
        result = "<h2 style='color: #ff7800;'>Relevant Context</h2>\n\n"
        for doc in context:
            result += f"<span style='color: #ff7800;'>Source: {doc.metadata['source']}</span>\n\n"
            result += doc.content + "\n\n"
        return result

    def chat(self, history):
        last_message = history[-1]["content"]
        prior = history[:-1]
        answer, context = self.chatbot.answer_question(last_message, prior)
        history.append({"role": "assistant", "content": answer})
        return history, self.format_context(context)

    def run_hook(self, *args, **kwargs):
        def put_message_in_chatbot(message, history):
            return "", history + [{"role": "user", "content": message}]

        response, context = self.chatbot.present_yourself()
        initial_history = [{"role": "assistant", "content": response}]

        theme = gr.themes.Soft(font=["Inter", "system-ui", "sans-serif"])

        with gr.Blocks(title="Job Interview Bot", theme=theme) as ui:
            gr.Markdown("# 🏢 Hi there, I am excited about this interview!\n")

            with gr.Row():
                with gr.Column(scale=1):
                    chatbot = gr.Chatbot(
                        label="💬 Conversation",
                        height=600,
                        type="messages",
                        show_copy_button=True,
                        value=initial_history,
                    )
                    message = gr.Textbox(
                        label="Your Question",
                        placeholder="Ask me anything about my work experience, academic background, etc...",
                        show_label=False,
                    )

                with gr.Column(scale=1):
                    context_markdown = gr.Markdown(
                        label="📚 Retrieved Context",
                        value=self.format_context(context),
                        container=True,
                        height=600,
                    )

            message.submit(
                put_message_in_chatbot,
                inputs=[message, chatbot],
                outputs=[message, chatbot],
            ).then(self.chat, inputs=chatbot, outputs=[chatbot, context_markdown])

        ui.launch(**kwargs)


if __name__ == "__main__":
    tmay_chatbot = get_chatbot()
    TmayChatbotGradioApp(tmay_chatbot).run(inbrowser=True, share=False)
