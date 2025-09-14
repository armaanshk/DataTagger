
import streamlit as st
import pandas as pd
from pathlib import Path
import time
import csv
from datetime import datetime

BASE = Path(__file__).resolve().parent
DATA_DIR = BASE/"data"
TEXT_CSV = DATA_DIR/"text"/"texts.csv"
IM_DIR = DATA_DIR/"images"
AU_DIR = DATA_DIR/"audio"
ANN_DIR = BASE/"annotations"
ANN_DIR.mkdir(exist_ok=True)

st.set_page_config(page_title="Multi-Modal Annotation Tool", layout="wide")
st.title("Multi-Modal Annotation Tool")

menu = st.sidebar.selectbox("Select mode", ["Text", "Image", "Audio", "Annotation Stats", "Guidelines"])
st.sidebar.markdown("---")
st.sidebar.write("Annotator: ")
annotator = st.sidebar.text_input("Name", value="annotator_1")

def save_csv_row(path, row):
    exists = path.exists()
    with open(path,"a",newline="",encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(row)

if menu=="Guidelines":
    st.header("Annotation Guidelines")
    st.markdown("""
    - **Text**: Label sentences as *Positive*, *Negative*, or *Neutral*.
    - **Images**: Provide a category label for the image (e.g., Dog, Cat, Car). Optionally provide bounding box coordinates (xmin,ymin,xmax,ymax) in pixels.
    - **Audio**: Label audio clip as *Speech*, *Music*, or *Noise*.
    - Use consistent labels. When unsure, choose the closest label and flag for review.
    """)
    st.info("Keep annotations consistent. Provide feedback in the 'Annotation Stats' page if you find unclear samples.")
elif menu=="Text":
    st.header("Text Annotation")
    df = pd.read_csv(TEXT_CSV)
    idx = st.number_input("Text index", min_value=0, max_value=len(df)-1, value=0)
    row = df.iloc[idx]
    st.write("Sentence:")
    st.write(row["sentence"])
    col1, col2 = st.columns(2)
    with col1:
        label = st.radio("Label", ["Positive","Negative","Neutral"])
    with col2:
        if st.button("Save Annotation"):
            rid = row["id"]
            ts = datetime.utcnow().isoformat()
            save_csv_row(ANN_DIR/"text_labels.csv", [rid, row["sentence"], label, annotator, ts])
            st.success("Saved!")
elif menu=="Image":
    st.header("Image Annotation")
    imgs = sorted([p.name for p in IM_DIR.glob("*.jpg")])
    if not imgs:
        st.warning("No images found.")
    else:
        sel = st.selectbox("Select image", imgs)
        st.image(str(IM_DIR/sel), use_column_width=True)
        label = st.selectbox("Label", ["Dog","Cat","Car","Other"])
        st.write("Optional: Enter bounding box coordinates in pixels (xmin,ymin,xmax,ymax)")
        xmin = st.number_input("xmin", min_value=0, value=0)
        ymin = st.number_input("ymin", min_value=0, value=0)
        xmax = st.number_input("xmax", min_value=0, value=0)
        ymax = st.number_input("ymax", min_value=0, value=0)
        if st.button("Save Image Annotation"):
            ts = datetime.utcnow().isoformat()
            save_csv_row(ANN_DIR/"image_labels.csv", [sel.split(".")[0], sel, label, xmin, ymin, xmax, ymax, annotator, ts])
            st.success("Saved!")
elif menu=="Audio":
    st.header("Audio Annotation")
    audios = sorted([p.name for p in AU_DIR.glob("*.wav")])
    if not audios:
        st.warning("No audio found.")
    else:
        sel = st.selectbox("Select audio", audios)
        st.audio(str(AU_DIR/sel))
        label = st.selectbox("Label", ["Speech","Music","Noise","Other"])
        if st.button("Save Audio Annotation"):
            ts = datetime.utcnow().isoformat()
            save_csv_row(ANN_DIR/"audio_labels.csv", [sel.split(".")[0], sel, label, annotator, ts])
            st.success("Saved!")
elif menu=="Annotation Stats":
    st.header("Annotation Statistics")
    t = pd.read_csv(ANN_DIR/"text_labels.csv")
    i = pd.read_csv(ANN_DIR/"image_labels.csv")
    a = pd.read_csv(ANN_DIR/"audio_labels.csv")
    st.subheader("Text Annotations")
    st.write(t)
    st.subheader("Image Annotations")
    st.write(i)
    st.subheader("Audio Annotations")
    st.write(a)
    st.markdown("### Summary counts")
    st.write("Text counts:")
    st.write(t['label'].value_counts())
    st.write("Image counts:")
    st.write(i['label'].value_counts())
    st.write("Audio counts:")
    st.write(a['label'].value_counts())
