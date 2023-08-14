from docxtpl import DocxTemplate, InlineImage
from docx.shared import Mm
import os
import time


def main(docname, docnewname, insert_time, **kwargs):
    doc = DocxTemplate(docname)
    kw = {k: InlineImage(doc, v, width=Mm(140)) for k, v in kwargs.items()}
    content = {
        'insert_time': insert_time,
    }
    content |= kw
    # 'img': InlineImage(doc, './FiuqFfsVsAAe7SB.jpg', width=Mm(140)),

    doc.render(content)
    doc.save(docnewname)


if __name__ == '__main__':
    pic_path = r'D:\wwa\xunpic'
    docname = os.path.join(r'D:\wwa', '云网采控中心巡检报告-template.docx')
    insert_time = '2023年3月9日 6点40'
    docnewname = docname.replace('template', insert_time)
    contenx = dict()
    for name in os.listdir(pic_path):
        key = name.split('.')[0]
        contenx[key] = os.path.join(pic_path, name)
    main(docname, docnewname, insert_time, **contenx)
