from pdf2image import convert_from_path
import os

def convert_carousel_to_images(pdf_path: str) -> list[str]:
    """
    Convertit chaque page du PDF en image JPG.
    Retourne la liste des chemins d'images générées.
    """
    
    output_dir = "posts/images"
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"🔄 Converting {pdf_path} to images...")
    
    pages = convert_from_path(
        pdf_path,
        dpi=150,
        poppler_path=r"C:\Users\Dell\Downloads\Release-26.02.0-0\poppler-26.02.0\Library\bin"
    )
    
    image_paths = []
    for i, page in enumerate(pages, 1):
        image_path = f"{output_dir}/slide_{i:02d}.jpg"
        page.save(image_path, "JPEG", quality=95)
        image_paths.append(image_path)
        print(f"✅ Slide {i}/{len(pages)} saved")
    
    print(f"\n✅ {len(pages)} images ready in {output_dir}/")
    return image_paths


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        # Prend le dernier PDF généré par défaut
        import glob
        pdfs = sorted(glob.glob("posts/*.pdf"))
        if not pdfs:
            print("❌ No PDF found in posts/ folder")
            sys.exit(1)
        pdf_path = pdfs[-1]
    else:
        pdf_path = sys.argv[1]
    
    print(f"📄 PDF: {pdf_path}")
    images = convert_carousel_to_images(pdf_path)
    
    print("\n📱 How to post on LinkedIn:")
    print("1. Create a new post")
    print("2. Click the image icon (not document)")
    print("3. Select ALL images at once (Ctrl+A)")
    print("4. LinkedIn will display them as a carousel")