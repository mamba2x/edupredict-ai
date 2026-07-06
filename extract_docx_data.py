import zipfile
import xml.etree.ElementTree as ET
import os

def get_docx_text(path):
    WORD_NAMESPACE = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
    PARA = WORD_NAMESPACE + 'p'
    TEXT = WORD_NAMESPACE + 't'
    
    try:
        with zipfile.ZipFile(path) as docx:
            tree = ET.parse(docx.open('word/document.xml'))
            root = tree.getroot()
            paragraphs = []
            for para in root.iter(PARA):
                texts = [node.text for node in para.iter(TEXT) if node.text]
                if texts:
                    paragraphs.append(''.join(texts))
            return '\n'.join(paragraphs)
    except Exception as e:
        return f"Error reading {path}: {str(e)}"

# Read Approved CIS-Final Year Project Report Guide.docx and write to a txt
guide_text = get_docx_text("Approved CIS-Final Year Project Report Guide.docx")
with open("guide_text.txt", "w", encoding="utf-8") as f:
    f.write(guide_text)

# Read EduPredict_Workflow_and_DFD.docx and write to a txt
workflow_text = get_docx_text("EduPredict_Workflow_and_DFD.docx")
with open("workflow_text.txt", "w", encoding="utf-8") as f:
    f.write(workflow_text)

print("Extraction complete!")
