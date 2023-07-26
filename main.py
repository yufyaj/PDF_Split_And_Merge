from PyPDF2 import PdfReader, PdfWriter, Transformation
import PyPDF2

INPUT_PDF_PATH  = 'C:/Users/YuyaKato/Desktop/06d1570e-fa50-4da1-9cfe-aaeac9034485.pdf'
OUTPUT_PDF_PATH = 'C:/Users/YuyaKato/Desktop/output.pdf'

def crop_pdf():
    # 用紙を確認
    input_pdf  = PdfReader(INPUT_PDF_PATH)
    output_pdf = PyPDF2.PdfWriter()
    top        = PyPDF2._page.PageObject.create_blank_page(width=0, height=0)
    bottom     = PyPDF2._page.PageObject.create_blank_page(width=0, height=0)
    # ページ数分ループ
    for i in range(len(input_pdf.pages)):
        page = input_pdf.pages[i]
        # Media Boxの座標＝サイズ（pt単位）
        (x0, y0) = page.mediabox.lower_left
        (x1, y1) = page.mediabox.upper_right
        pageWidth = x1
        pageHeight = y1
        page.cropbox.lower_left  = (x0, y1 / 2)
        page.cropbox.upper_right = (x1, y1)

        if ((i + 1) % 2 == 0 or (i + 1) == len(input_pdf.pages)):
            bottom = PyPDF2._page.PageObject.create_blank_page(width=pageWidth, height=pageHeight)
            bottom.merge_page(page)
            op = Transformation().translate(tx=0, ty=-1 * (y1 / 2))
            bottom.add_transformation(op)
            newPage = PyPDF2._page.PageObject.create_blank_page(width=pageWidth, height=pageHeight)
            newPage.merge_page(top)
            newPage.merge_page(bottom)
            output_pdf.add_page(newPage)
            top     = PyPDF2._page.PageObject.create_blank_page(width=0, height=0)
            bottom  = PyPDF2._page.PageObject.create_blank_page(width=0, height=0)
        else:
            top     = page
    
    # ファイル出力
    with open(OUTPUT_PDF_PATH, mode='wb') as f:
        output_pdf.write(f)

if __name__ == "__main__":
    crop_pdf()