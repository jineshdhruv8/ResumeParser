from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfpage import PDFTextExtractionNotAllowed
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfdevice import PDFDevice
from pdfminer.layout import LAParams
from pdfminer.converter import PDFPageAggregator
import pdfminer


# def read_PDF(fileObj):
#     import PyPDF2
#
#     # creating a pdf reader object
#     pdfReader = PyPDF2.PdfFileReader(fileObj)
#
#     # printing number of pages in pdf file
#     print(pdfReader.numPages)
#
#     # creating a page object
#     pageObj = pdfReader.getPage(0)
#
#     # extracting text from page
#     print(pageObj.extractText())



def read_PDF_Miner(fileObj):


    # Create a PDF parser object associated with the file object.
    parser = PDFParser(fileObj)

    # Create a PDF document object that stores the document structure.
    # Password for initialization as 2nd parameter
    document = PDFDocument(parser)

    # Check if the document allows text extraction. If not, abort.
    if not document.is_extractable:
        raise PDFTextExtractionNotAllowed

    # Create a PDF resource manager object that stores shared resources.
    rsrcmgr = PDFResourceManager()

    # Create a PDF device object.
    device = PDFDevice(rsrcmgr)

    # BEGIN LAYOUT ANALYSIS
    # Set parameters for analysis.
    laparams = LAParams()

    # Create a PDF page aggregator object.
    device = PDFPageAggregator(rsrcmgr, laparams=laparams)

    # Create a PDF interpreter object.
    interpreter = PDFPageInterpreter(rsrcmgr, device)

    def parse_obj(lt_objs):

        # loop over the object list
        for obj in lt_objs:

            # if it's a textbox, print text and location
            if isinstance(obj, pdfminer.layout.LTTextBoxHorizontal):
                print("%6d, %6d, %s" % (obj.bbox[0], obj.bbox[1], obj.get_text().replace('\n', '_')))

            # if it's a container, recurse
            elif isinstance(obj, pdfminer.layout.LTFigure):
                parse_obj(obj._objs)

    # loop over all pages in the document
    for page in PDFPage.create_pages(document):
        # read the page into a layout object
        interpreter.process_page(page)
        layout = device.get_result()

        # extract text from this object
        parse_obj(layout._objs)

# def read_PDFMiner3(fileObj):
#     from pdfminer.pdfparser import PDFParser, PDFDocument
#     from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
#     from pdfminer.converter import PDFPageAggregator
#     from pdfminer.layout import LAParams, LTTextBox, LTTextLine
#
# #     fp = open('file.pdf', 'rb')
#     parser = PDFParser(fileObj)
#     doc = PDFDocument()
#     parser.set_document(doc)
#     doc.set_parser(parser)
#     doc.initialize('')
#     rsrcmgr = PDFResourceManager()
#     laparams = LAParams()
#     device = PDFPageAggregator(rsrcmgr, laparams=laparams)
#     interpreter = PDFPageInterpreter(rsrcmgr, device)
#     # Process each page contained in the document.
#     for page in doc.get_pages():
#         interpreter.process_page(page)
#         layout = device.get_result()
#         for lt_obj in layout:
#             if isinstance(lt_obj, LTTextBox) or isinstance(lt_obj, LTTextLine):
#                 print(lt_obj.get_text())
#


def main():
    from pymongo import MongoClient
    import gridfs

    con = MongoClient(host='127.0.0.1', port=3001)
    db = con.meteor
    fs = gridfs.GridFS(db)

    # creating a pdf file object
    pdfFileObj = open('/home/jinesh/Desktop/Job Application Documents/Jinesh/DHRUV_JINESH_SOFTWARE_RESUME.pdf', 'rb')
    id = fs.put(pdfFileObj)
    # read_PDF(fs.get(id))
    read_PDF_Miner(fs.get(id))
    # read_PDFMiner3(fs.get(id))


if __name__ == '__main__':
    main()