import os, sys
from bs4 import BeautifulSoup as bs
import requests
import wget as wg
import zipfile
import shutil
from PIL import Image
import re
class WriteTag(object):

    def __init__(self, tag, classname, content, format='.html'):
        self.tag = tag
        self.classname = classname
        self.content = content
        self.format = format
        self.result = open(f'res{self.format}', encoding='utf-8', mode='a')
    def writerLines(self):

        self.result.write(f'<{self.tag} class={self.classname}>{self.content}</{self.tag}>\n')
        self.result.close()
    def htmlStart(self):
 
        self.result.write(f'<!DOCTYPE html><html lang="ru">\n')
        self.result.close()
    def tagOpen(self):

        self.result.write(f'<{self.tag} class={self.classname}>{self.content}\n')
        self.result.close()
    def tagClose(self):

        self.result.write(f'{self.classname}{self.content}</{self.tag}>\n')
        self.result.close()


class ParsingCian(object):
    def __init__(self, idd):
        self.idd = idd
        self.tempdir = 'temp'
        self.tempfile = f'{self.tempdir}/{self.idd}/{self.idd}.docx'
        self.docimage = f'{self.tempdir}/{self.idd}/word/media'
        self.deleteFiles = {
            "folder" : {'_rels':1, 'docProps':2,'word':3},
            "tmp":{f'{self.idd}.docx':1,'[Content_Types].xml':2},
            "img":{'cian-logo-cyrillic-horizontal-small.png':1,'no.png':2,'yes.png':3,'logo.jpeg':4}
        }
        self.image_dir = f'temp/{self.idd}/img'
    def fileoperation(self) :

        os.mkdir(f'{self.tempdir}/{self.idd}'),
        wg.download(f'http://cian.ru/export/docx/sale/flat/{self.idd}', f'{self.tempdir}/{self.idd}/{self.idd}.docx'),
        zipfile.ZipFile(self.tempfile).extractall(f'{self.tempdir}/{self.idd}/'),
        wg.download(f'http://cian.ru/rent/flat/{self.idd}/', f'{self.tempdir}/{self.idd}/{self.idd}.html'),
        os.mkdir(f'{self.tempdir}/{self.idd}/img'),os.mkdir(f'temp/{self.idd}/images'),
        for deleteImages in self.deleteFiles.get('img'):
            os.remove(f'{self.docimage}/{deleteImages}')
        for x in os.listdir(self.docimage):
            os.replace(f'{self.docimage}/{x}', f'{self.tempdir}/{self.idd}/img/{x}')
        for deleteFolder in self.deleteFiles.get('folder'):
            shutil.rmtree(f'{self.tempdir}/{self.idd}/{deleteFolder}')
        for deleteFiles in self.deleteFiles.get('tmp'):
            os.remove(f'{self.tempdir}/{self.idd}/{deleteFiles}')
    def watterMark(self):
        files = os.listdir(self.image_dir)
        jpg = filter(lambda x: x.endswith('.jpeg'), files)
        for i in jpg:
            base_image = Image.open(f'{self.image_dir}/{i}')
            output_image = f'temp/{self.idd}/images/{i}'
            wattermark_path = f'temp/wattermark.o'
            watermark = Image.open(wattermark_path)
            watermark.thumbnail = (100,100)
            width, height = base_image.size
            transparent = Image.new('RGB', (width, height), (0, 0, 0, 0))
            transparent.paste(base_image, (0, 0))
            x = int(transparent.size[0]/2) - int(watermark.size[0]/2)
            y = int(transparent.size[1]/2) - int(watermark.size[1]/2)
            transparent.paste(watermark, (x,y), mask=watermark)
            transparent.save(output_image)
    def htmlparsing(self):
        html = f'temp/{self.idd}/{self.idd}.html'
        with open(html, 'r', encoding='utf-8') as file:
            content = file.read()
            soup = bs(content, 'html.parser')
            WriteTag('','','').htmlStart()
            WriteTag('body', 'header', '').tagOpen()
            for el in soup.select('.a10a3f92e9--phone--3XYRR'):
                tel = el.text
                WriteTag('div', 'tel', tel).writerLines()
            for el in soup.select('.a10a3f92e9--title--2Widg'):
                name = el.text
                WriteTag('div', 'name', name).writerLines()
            for el in soup.select('.a10a3f92e9--geo--18qoo'):
                adress = el.text
                adr = 'На'.join(adress.split('На')[: -1])
                WriteTag('div', 'adress', adr).writerLines()
            WriteTag('div', 'options', '').tagOpen()
            WriteTag('table', 'options', '').tagOpen()
            WriteTag('tbody', 'options', '').tagOpen()
            for el in soup.select('.a10a3f92e9--info-title--2bXM9'):
                title = el.text
                WriteTag('tb', 'title', title).writerLines()
            WriteTag('tbody', '', '').tagClose()
            WriteTag('thead', 'options', '').tagOpen()
            for el in soup.select('.a10a3f92e9--info-value--18c8R'):
                value = el.text
                WriteTag('th', 'value', value).writerLines()
            WriteTag('thead', '', '').tagClose()
            WriteTag('table','','').tagClose()
            WriteTag('div','','').tagClose()
            for el in soup.select('.a10a3f92e9--description-text--3Sal4'):
                description = el.text
                WriteTag('div', 'description', description).writerLines()
            WriteTag('div', 'opt','').tagOpen()
            for el in soup.select('.a10a3f92e9--container--By_bg'):
                for x in el.select('li'):
                    definfo = x.text
                    WriteTag('div','definfo',definfo).writerLines()
            for el in soup.select('.a10a3f92e9--container--L-EIV'):
                for x in el.select('li'):
                    optinfo = x.text
                    WriteTag('div','optinfo', optinfo).writerLines()
            WriteTag('div', '', '').tagClose()
            WriteTag('home', 'home','').tagOpen()
            for el in soup.select('.a10a3f92e9--title--1GSlx'):
                for x in el.select('span'):
                    span = x.text
                    WriteTag('span', 'span', span)
            WriteTag('div', 'options', '').tagOpen()
            WriteTag('table', 'options', '').tagOpen()
            WriteTag('tbody', 'options', '').tagOpen()
            for el in soup.select('.a10a3f92e9--name--3bt8k'):
                title = el.text
                WriteTag('tb', 'title', title).writerLines()
            WriteTag('tbody', '', '').tagClose()
            WriteTag('thead', 'options', '').tagOpen()
            for el in soup.select('.a10a3f92e9--value--3Ftu5'):
                value = el.text
                WriteTag('th', 'value', value).writerLines()
            WriteTag('thead', '', '').tagClose()
            WriteTag('table', '', '').tagClose()
            WriteTag('div', '', '').tagClose()
            WriteTag('div', 'options', '').tagOpen()
            WriteTag('table', 'options', '').tagOpen()
            WriteTag('tbody', 'options', '').tagOpen()
            for el in soup.select('.a10a3f92e9--name--22FM0'):
                title = el.text
                WriteTag('tb', 'title', title).writerLines()
            WriteTag('tbody', '', '').tagClose()
            WriteTag('thead', 'options', '').tagOpen()
            for el in soup.select('.a10a3f92e9--value--38caj'):
                value = el.text
                WriteTag('th', 'value', value).writerLines()
            WriteTag('thead', '', '').tagClose()
            WriteTag('table', '', '').tagClose()
            WriteTag('div', '', '').tagClose()
        WriteTag('home','','').tagClose()
        WriteTag('body','','').tagClose()

class Run(object):
    def __init__(self,idd):
        self.idd = idd
        ParsingCian(self.idd).fileoperation()
        ParsingCian(self.idd).htmlparsing()
        ParsingCian(self.idd).watterMark()
