import gradio as gr
from TTS.api import TTS

MODELS = {
    "xtts_v2 (multilingual multi-dataset)": "tts_models/multilingual/multi-dataset/xtts_v2",
    "vits (en vctk)": "tts_models/en/vctk/vits",
    "fastspeech2 (en ljspeech)": "tts_models/en/ljspeech/fastspeech2",
}

tts_cache = {}


def load_model(model_name):
    if model_name not in tts_cache:
        tts_cache[model_name] = TTS(MODELS[model_name])
    return tts_cache[model_name]


def get_languages(model_name):
    tts = load_model(model_name)
    if hasattr(tts, "languages") and tts.languages:
        return tts.languages
    return []


def get_speakers(model_name):
    tts = load_model(model_name)
    if hasattr(tts, "speakers") and tts.speakers:
        return tts.speakers
    return []


def generate_tts(model_name, text, speaker, language):
    tts = load_model(model_name)
    output_path = "output.wav"
    if tts.is_multi_speaker:
        tts.tts_to_file(text=text, speaker=speaker, language=language, file_path=output_path)
    elif tts.is_multi_lingual:
        tts.tts_to_file(text=text, language=language, file_path=output_path)
    else:
        tts.tts_to_file(text=text, file_path=output_path)
    return output_path


with gr.Blocks() as demo:
    gr.Markdown("# 多模型多语言多说话人 TTS Demo")

    with gr.Row():
        model_dropdown = gr.Dropdown(list(MODELS.keys()), label="选择模型")
        confirm_btn = gr.Button("确认模型")

    language_dropdown = gr.Dropdown(label="选择语言")
    speaker_dropdown = gr.Dropdown(label="选择说话人")

    text_input = gr.Textbox(label="输入文本", lines=3, placeholder="请输入需要合成的文本")

    generate_button = gr.Button("生成语音")
    audio_output = gr.Audio(label="生成音频", type="filepath")

    def update_language_and_speaker(model_name):
        langs = get_languages(model_name)
        spks = get_speakers(model_name)
        return gr.update(choices=langs, value=langs[0] if langs else None), gr.update(choices=spks, value=spks[0] if spks else None)

    confirm_btn.click(
        update_language_and_speaker,
        inputs=model_dropdown,
        outputs=[language_dropdown, speaker_dropdown],
    )

    generate_button.click(
        generate_tts,
        inputs=[model_dropdown, text_input, speaker_dropdown, language_dropdown],
        outputs=audio_output,
    )

demo.launch()
