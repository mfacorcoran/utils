def pdf2ocr(pdffile):
    """
    Optical Character Recognition on PDF files using Python
    see https://pythontips.com/2016/02/25/ocr-on-pdf-files-using-python/
    :param pdffile: pdffile to be OCR'd
    :return:

    """
    from wand.image import Image
    from PIL import Image as PI
    import pyocr
    import pyocr.builders
    import io
    tool = pyocr.get_available_tools()[0]
    lang = tool.get_available_languages()[0] # [0] for english
    req_image = []
    final_text = []
    print "Reading {0}".format(pdffile)
    image_pdf = Image(filename=pdffile, resolution=300)
    image_jpeg = image_pdf.convert('jpeg')
    for img in image_jpeg.sequence:
        img_page = Image(image=img)
        req_image.append(img_page.make_blob('jpeg'))
    print "Generating text"
    for img in req_image:
        txt = tool.image_to_string(
            PI.open(io.BytesIO(img)),
            lang=lang,
            builder=pyocr.builders.TextBuilder()
        )
        final_text.append(txt)
    return final_text
