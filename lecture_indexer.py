import json
import re
import sys
from collections import Counter
from pathlib import Path
from youtube_transcript_api import YouTubeTranscriptApi

OUT_DIR = Path(__file__).resolve().parent

STOPWORDS = {
    "the", "and", "to", "of", "in", "is", "it", "that", "for", "you", "we",
    "on", "with", "this", "are", "as", "be", "at", "or", "from", "by", "an",
    "have", "so", "can", "if", "but", "not", "what", "all", "about", "there",
    "going", "now", "like", "just", "right", "here", "uh", "um", "okay", "yeah",
    "very", "really", "actually", "basically", "thing", "things", "way", "see"
}

def extract_video_id(url):
    match = re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11}).*", url)
    return match.group(1) if match else url

def format_timestamp(seconds):
    mins, secs = divmod(int(seconds), 60)
    hrs, mins = divmod(mins, 60)
    return f"{hrs:02d}:{mins:02d}:{secs:02d}" if hrs else f"{mins:02d}:{secs:02d}"

def extract_top_concepts(text, top_n=5):
    words = re.findall(r"\b[a-zA-Z]{4,}\b", text.lower())
    filtered = [w for w in words if w not in STOPWORDS]
    return [word for word, _ in Counter(filtered).most_common(top_n)]

def process_lecture(video_url, window_sec=180):
    video_id = extract_video_id(video_url)
    ytt_api = YouTubeTranscriptApi()
    transcript = ytt_api.fetch(video_id, languages=["en", "en-US", "en-GB"]).to_raw_data()

    chunks, current_text, chunk_start = [], [], 0.0

    for entry in transcript:
        if entry["start"] - chunk_start >= window_sec and current_text:
            joined_text = " ".join(current_text)
            chunks.append({
                "start_sec": int(chunk_start),
                "timestamp": format_timestamp(chunk_start),
                "url": f"https://youtu.be/{video_id}?t={int(chunk_start)}",
                "key_concepts": extract_top_concepts(joined_text),
                "raw_text": joined_text
            })
            current_text = []
            chunk_start = entry["start"]
        current_text.append(entry["text"].replace("\n", " "))

    if current_text:
        joined_text = " ".join(current_text)
        chunks.append({
            "start_sec": int(chunk_start),
            "timestamp": format_timestamp(chunk_start),
            "url": f"https://youtu.be/{video_id}?t={int(chunk_start)}",
            "key_concepts": extract_top_concepts(joined_text),
            "raw_text": joined_text
        })

    json_path = OUT_DIR / "lecture_dataset.json"
    md_path = OUT_DIR / "lecture_index.md"

    with open(json_path, "w", encoding="utf-8") as jf:
        json.dump(chunks, jf, indent=2)

    with open(md_path, "w", encoding="utf-8") as mf:
        mf.write(f"# Lecture Concept Index (Video ID: {video_id})\n\n")
        for c in chunks:
            concepts = ", ".join(c["key_concepts"])
            mf.write(f"* **[{c['timestamp']}]({c['url']})** — Top Concepts: {concepts}\n")

    print(f"Success! Saved {md_path} and {json_path}")

if __name__ == "__main__":
    target_url = sys.argv[1] if len(sys.argv) > 1 else "https://www.youtube.com/watch?v=aircAruvnKk"
    process_lecture(target_url)