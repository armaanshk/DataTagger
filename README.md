# Multi-Modal Data Annotation

## Overview
A simple, multi-modal annotation tool that supports **text**, **image**, and **audio** labeling. Built with **Streamlit** for a minimal UI and easy interaction.

## Features
- Text annotation (Positive / Negative / Neutral)
- Image annotation (label + optional bounding box coordinates)
- Audio annotation (Speech / Music / Noise)
- Saves annotations to CSV in `annotations/`
- Sample data included (text CSV, generated images, generated audio)

## How to run
1. Install Python (3.8+ recommended).
2. Create a virtual environment (optional):
```bash
python -m venv venv
source venv/bin/activate    # Linux/macOS
venv\Scripts\activate     # Windows
```
3. Install dependencies:
```bash
pip install streamlit pandas pillow
```
4. Run the app:
```bash
streamlit run app_streamlit.py
```
5. Open the URL shown by Streamlit in your browser.

## Project structure
```
data-annotation-project/
├─ data/
│  ├─ text/texts.csv
│  ├─ images/*.jpg
│  └─ audio/*.wav
├─ annotations/
│  ├─ text_labels.csv
│  ├─ image_labels.csv
│  └─ audio_labels.csv
├─ app_streamlit.py
└─ README.md
```

## How it works
- Use the **Text** tab to annotate sentences and save them.
- Use the **Image** tab to label images; optionally enter bounding box coordinates.
- Use the **Audio** tab to play and label audio clips.
- All annotations are appended to CSV files in `annotations/` with timestamp and annotator name.

## Extensions (ideas)
- Add inter-annotator agreement checks (duplicate samples).
- Add bounding-box drawing UI (e.g., labelImg integration).
- Add export to COCO/YOLO formats.
- Add user authentication and role-based access.
- Add quality-control dashboards and consensus workflows.

## License
MIT
