import re
from TTS.api import TTS


def split_text(text, max_len=200):
    # 根据中文或英文标点分句
    sentences = re.split(r'([。！？!?])', text)
    chunks = []
    current = ""
    for i in range(0, len(sentences)-1, 2):
        sentence = sentences[i] + sentences[i+1]
        if len(current) + len(sentence) <= max_len:
            current += sentence
        else:
            chunks.append(current)
            current = sentence
    if current:
        chunks.append(current)
    return chunks


model_name = r"tts_models/multilingual/multi-dataset/xtts_v2"

book_path = r"data/book/test.txt"

if __name__ == "__main__":
    tts = TTS(model_name=model_name, progress_bar=False)
    with open(book_path, "r", encoding="gbk") as f:
        text = f.read()

        # 切分文本（根据标点断句）

    chunks = split_text(text)
    for i, chunk in enumerate(chunks):
        output_path = f"output_{i}.wav"
        tts.tts_to_file(text=chunk, file_path=output_path, speaker=tts.speakers[0], language="zh-cn")
        print(f"Saved {output_path}")

        if i >= 5:
            break
