# YouTube Lecture Concept Indexer

A lightweight, dependency-light Python utility designed to parse raw YouTube lecture audio transcripts, filter conversational noise, and export structured datasets and timestamped Markdown study guides. Built to automate data preprocessing for educational technology and natural language processing (NLP) research workflows.

---

## 🚀 Key Features

* **Automated Transcript Retrieval:** Programmatically fetches timestamped caption tracks from any public YouTube lecture URL.
* **Contextual Time-Window Chunking:** Groups raw sentence fragments into configurable 3-minute blocks to preserve complete instructional thoughts.
* **Noise Filtering & Frequency Scoring:** Strips out conversational fillers, punctuation, and common English stopwords using custom regex and Python's `Counter`.
* **Dual Pipeline Output:** Simultaneously generates:
  * `lecture_index.md`: A clean, human-readable study guide featuring clickable timestamped links.
  * `lecture_dataset.json`: A structured machine-ready JSON dataset optimized for downstream NLP and EdTech pipelines.

---

## 🛠️ Tech Stack & Requirements

* **Language:** Python 3.x
* **Core Dependency:** `youtube-transcript-api`

---

## ⚙️ Installation & Usage

1. Clone or download this repository:
   ```bash
   git clone [https://github.com/adinarayan0706-stack/youtube-lecture-indexer.git](https://github.com/adinarayan0706-stack/youtube-lecture-indexer.git)
   cd youtube-lecture-indexer
