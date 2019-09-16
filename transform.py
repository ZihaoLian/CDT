
import os
from win32com import client as wc
import docx


def doc2docx(originDir):
    word = wc.Dispatch('Word.Application')
    for root, _, files in os.walk(os.path.join(os.getcwd(),originDir)):
        for file in files:
            doc = word.Documents.Open(os.path.join(root,file))        # 目标路径下的文件
            doc.SaveAs(os.path.join(os.getcwd(),'dist',file+'x'), 12, False, "", True,
                    "", False, False, False, False)  # 转化后路径下的文件
            doc.Close()
    word.Quit()

def docx2csv():
    for root, _, files in os.walk(os.path.join(os.getcwd(),'dist')):
        for file in files:
            doc = word.Documents.Open(os.path.join(root,file))        # 目标路径下的文件
            doc.SaveAs(os.path.join(os.getcwd(),'dist',file+'x'), 12, False, "", True,
                    "", False, False, False, False)  # 转化后路径下的文件
            doc.Close()

doSaveAas('origin')