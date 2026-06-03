import pdfplumber
import os

pdf_path = r'C:\Users\Siddique Akbar\Downloads\map b (2).pdf'
output_dir = 'pdf_images'
os.makedirs(output_dir, exist_ok=True)

try:
    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages):
            img = page.to_image(resolution=150)
            img.save(os.path.join(output_dir, f"page_{i+1}.png"))
            print(f"Saved page {i+1} to {output_dir}")
except Exception as e:
    print(f"Error: {e}")
