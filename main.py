from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Frame, \
    BaseDocTemplate, PageTemplate, NextFrameFlowable, Image, NextPageTemplate, Table, TableStyle
from reportlab.platypus.flowables import BalancedColumns
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch, mm
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import LETTER
from reportlab.lib import colors
from reportlab.graphics.shapes import Line, LineShape, Drawing, Rect, String
from reportlab.lib.enums import TA_LEFT, TA_RIGHT, TA_CENTER, TA_JUSTIFY
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import pathlib

PAGE_HEIGHT = 842
PAGE_WIDTH = 595
FONT_DIR = './Fonts'

# Register fonts
for font in pathlib.Path(FONT_DIR).glob('*.ttf'):
    pdfmetrics.registerFont(TTFont(font.stem, font))

# Define colors
CLR_BG_S_DIMORPHISM_FIRST = colors.HexColor('#EDEDED')
CLR_FG_S_DIMORPHISM_FIRST = colors.HexColor('#233137')
CLR_FG_SUBJECT_FIRST = colors.HexColor('#121212')
CLR_BG_S_DIMORPHISM_SECOND = colors.HexColor('#ADC3CA')
CLR_FG_S_DIMORPHISM_SECOND = colors.HexColor('#233137')
CLR_FG_SUBJECT_SECOND = colors.HexColor('#FFFFFF')
STR_S_DIMORPHISM = 'Sexual Dimorphism'
CLR_DRAW = colors.HexColor('#121212')
CLR_TABLE = colors.HexColor('#626262')
CLR_FONT_ALPHA = colors.Color(1, 1, 1, 0.5)
FONT_GENERAL = 'NeueMontreal-Regular'
FONT_SPECIAL = 'F37ZagmaMonoTrial-Regular'

# Define HeaderCanvas class
class HeaderCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        canvas.Canvas.__init__(self, *args, **kwargs)
        self.pages = []
        self.width = PAGE_WIDTH
        self.height = PAGE_HEIGHT

    def showPage(self):
        self.pages.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        page_count = len(self.pages)
        for page in self.pages:
            self.__dict__.update(page)
            self.draw_header()
            self.draw_symbol()
            self.draw_figure_section()
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_symbol(self):
        self.saveState()
        clr_fg = None
        clr_bg = None
        if self.getPageNumber() == 1:
            clr_fg = CLR_FG_S_DIMORPHISM_FIRST
            clr_bg = CLR_BG_S_DIMORPHISM_FIRST
        else:
            clr_fg = CLR_FG_S_DIMORPHISM_SECOND
            clr_bg = CLR_BG_S_DIMORPHISM_SECOND
        obj_drawing = Drawing(91, 13)
        rect = Rect(0, 0, 91, 13)
        rect.fillColor = clr_bg
        rect.strokeColor = clr_bg
        str_s_dimorphism = String(5, 4, STR_S_DIMORPHISM)
        str_s_dimorphism.fillColor = clr_fg
        obj_drawing.add(rect)
        obj_drawing.add(str_s_dimorphism)
        obj_drawing.drawOn(self, 26, 743)
        self.restoreState()

    def draw_figure_section(self):
        if self.getPageNumber() != 1:
            return
        self.saveState()
        self.setFillAlpha(1)
        self.drawImage('test.png', 210, 41, width=174, height=171)
        self.drawImage('test.png', 395, 41, width=174, height=171)
        self.restoreState()

    def draw_header(self):
        page_number = "%02d" % (self.getPageNumber())
        str_preliminary = 'Preliminary'
        str_dimorphism = 'Dimorphism'
        str_theory = 'Theory'
        self.saveState()
        if self.getPageNumber() == 1:
            self.setFillColor(colors.black)
        else:
            self.setFillColor(colors.white)
        self.setFont('NeueMontreal-Regular', 15)
        self.drawString(554, 802, page_number)
        self.setFillAlpha(0.5)
        self.setFont('NeueMontreal-Regular', 10)
        self.drawString(26, 805, str_preliminary)
        self.drawString(93, 805, str_dimorphism)
        self.setFillAlpha(1)
        self.drawString(164, 805, str_theory)
        self.setLineWidth(1)  # Set line width
        self.setStrokeColor(CLR_DRAW, 0.1)
        self.setLineWidth(1)  # Set circle border width
        # Draw a line
        self.line(212, 808, 212 + 326, 808)  # (x1, y1, x2, y2)
        self.setStrokeColor(CLR_DRAW, 0.2)  # Set circle border color (black)
        self.setFillColor(CLR_DRAW, 0.2)  # Set circle fill color (gray)
        # Draw a circle
        self.circle(83, 808, 1, fill=1)
        self.circle(154, 808, 1, fill=1)
        self.restoreState()

# Define TestReport class
class TestReport:
    def __init__(self, path):
        self.path = path
        self.doc = SimpleDocTemplate(path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
        self.elements = []
        self.page_templates = []
        self.first_page()
        self.elements.append(Spacer(10, 10))
        self.elements.append(PageBreak())
        self.elements.append(Spacer(10, 10))
        # self.second_page()
        # Build
        self.doc.multiBuild(self.elements, canvasmaker=HeaderCanvas, onLaterPages=self.on_later_pages)

    def on_later_pages(self, canvas, doc):
        canvas.saveState()
        canvas.setFillColor(CLR_FG_S_DIMORPHISM_SECOND)
        canvas.rect(0, 0, PAGE_WIDTH, PAGE_HEIGHT, fill=1, stroke=0)
        canvas.restoreState()
        frame_subject = Frame(x1=26, y1=653, width=208, height=80, leftPadding=0, bottomPadding=0, rightPadding=0,
                              topPadding=0, id='frame_subject_second', showBoundary=0)
        frame_content_title = Frame(x1=26, y1=585, width=359, height=12, leftPadding=0, bottomPadding=0, rightPadding=0,
                                   topPadding=0, id='frame_content_second', showBoundary=0)
        frame_content = Frame(x1=26, y1=475, width=359, height=100, leftPadding=0, bottomPadding=0, rightPadding=0,
                              topPadding=0, id='frame_content_second', showBoundary=0)
        frame_table_title = Frame(x1=26, y1=134, width=62, height=10, leftPadding=0, bottomPadding=0, rightPadding=0,
                                  topPadding=0, id='frame_table_title_second', showBoundary=0)
        frame_table = Frame(x1=26, y1=50, width=543, height=76, leftPadding=0, bottomPadding=0, rightPadding=0,
                            topPadding=0, id='frame_table_second', showBoundary=0)
        str_subject = "Assessment Overview"
        str_content_title = """<font size="8" color='#626262'>02/</font> <font color='#FFFFFF' fontSize='10' >&nbsp;&nbsp;&nbsp;&nbsp;<b>Next Few Pages</b></font>"""
        space_chunk = "&nbsp;" * 15
        str_content = f"""<font color="#FFFFFF" fontname="NeueMontreal-Regular" size ="20">
        {space_chunk}Our main goal with Facial<br/>Proportions is to take an overall look at your facial configuration and dimensions. Later in chapter 2 we  look into individual proportions, feature-by-feature.</font>"""
        str_table_title = "Summary of Tests"
        pg_subject_style = ParagraphStyle(name='second_subject_style', textColor=colors.white, fontName='NeueMontreal-Regular', fontSize=38, leading=38)
        pg_subject = Paragraph(str_subject, pg_subject_style)
        pg_content_title = Paragraph(str_content_title)
        pg_content_style = ParagraphStyle(name='content_style_second', leading=20, justifyBreaks=1)
        pg_content = Paragraph(str_content, pg_content_style)
        pg_table_title_style = ParagraphStyle(name='table_title', textColor=colors.white, fontSize=8, fontName='NeueMontreal-Regular', leading=0)
        pg_table_title = Paragraph(str_table_title, pg_table_title_style)
        data = [
            [Paragraph(f"<font fontName={FONT_SPECIAL} fontSize='8' color={CLR_FONT_ALPHA}>TABLE III</font>"),
             Paragraph(f"<font fontName={FONT_SPECIAL} fontSize='8' color={CLR_FONT_ALPHA}>RAW RESULT</font>"),
             Paragraph(f"<font fontName={FONT_SPECIAL} fontSize='8' color={CLR_FONT_ALPHA}>EXPLANATION</font>"),],
            [Paragraph(f"<font fontName={FONT_GENERAL} fontSize='8' color={colors.white}>Euclidean Matrix Analysis</font>"),
             Paragraph(f"<font fontName={FONT_GENERAL} fontSize='8' color={colors.white}>Saller and colleagues </font> <font size=6 color={colors.white}><super>[22]</super></font>"),
             Paragraph(f"<font fontName={FONT_GENERAL} fontSize='8' color={colors.white}>The subject has a moderately juvenile face.</font>")],
            [Paragraph(
                f"<font fontName={FONT_GENERAL} fontSize='8' color={colors.white}>Dimorphism Analysis</font>"),
             Paragraph(
                 f"<font fontName={FONT_GENERAL} fontSize='8' color={colors.white}>Edmondson and colleagues </font> <font size=6 color={colors.white}><super>[22]</super></font>"),
             Paragraph(
                 f"<font fontName={FONT_GENERAL} fontSize='8' color={colors.white}>Measuring changes of the face as as masculinity<br/>is artificially increased or decreased </font>",
                 ParagraphStyle(name='table', justifyBreaks=1)
             )],
        ]
        table_style = TableStyle([
            ('LINEBELOW', (0, 0), (-1, -1), 1, CLR_TABLE),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.white),
            ('VALIGN', (0, 1), (-1, -1), 'MIDDLE'),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('LEFTPADDING', (0, 0), (-1, -1), 0),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.Color(1, 1, 1, 0.5))
        ])
        table = Table(data, colWidths=[180, 180, 181], rowHeights=[22, 22, 32])
        table.setStyle(table_style)
        frame_subject.addFromList([pg_subject], canvas)
        frame_content_title.addFromList([pg_content_title], canvas)
        frame_content.addFromList([pg_content], canvas)
        frame_table_title.addFromList([pg_table_title], canvas)
        frame_table.addFromList([table], canvas)

    def add_page_color(self, canvas, doc):
        canvas.saveState()
        if canvas.getPageNumber() == 1:
            canvas.setFillColor(colors.white)
        else:
            canvas.setFillColor(CLR_FG_S_DIMORPHISM_SECOND)
        canvas.rect(0, 0, PAGE_WIDTH, PAGE_HEIGHT, fill=1, stroke=0)
        canvas.restoreState()

    def first_page(self):
        frame_subject = Frame(x1=26, y1=693, width=150, height=40, leftPadding=0, bottomPadding=0, rightPadding=0,
                              topPadding=0, id='frame_subject_first', showBoundary=0)
        frame_content_title = Frame(x1=210, y1=721, width=174, height=12, leftPadding=0, bottomPadding=0, rightPadding=0,
                                   topPadding=0, id='frame_content_title_first', showBoundary=0)
        frame_content = Frame(x1=210, y1=PAGE_HEIGHT - 338 - 131, width=358, height=338, leftPadding=0, bottomPadding=0, rightPadding=0,
                              topPadding=0, id='frame_content_first', showBoundary=0)
        frame_figure_illustration = Frame(x1=26, y1=41, width=174, height=50, leftPadding=0, bottomPadding=0, rightPadding=0,
                                         topPadding=0, id='frame_figure_illustration', showBoundary=0)
        str_subject = "Theory"
        str_content_title = """<font size="8" color='#626262'>01/</font>&nbsp;&nbsp;&nbsp;&nbsp;<b>What is it?</b>"""
        str_content = """<font color="#233137" size ="10"><br/>Humans have long been fascinated by facial proportions as ultimately these proportions make up the geometry of one’s face. In short, you are your proportions, measurements and ratios.
                <br/><br/>
               Following this, it is easy to understand why proportions are so closely linked to beauty. An attractive face by definition would have to have different proportions to an unattractive one as they inherently look different and have different forms. While this idea has held true for millennia, our application of facial proportions has changed.
                <br/><br/>
               In the early BC years, Ancient Greeks believed in divine proportions and canons of beauty. Think of the ‘Golden Ratio’, ‘Perfect Thirds,’ or similar and we can link them back to the works of early Hellenistic philosophers. In fact, most famous renaissance works such as Michalengo’s ‘David’ statue followed these proportions of beauty..
               <br/><br/><br/>
               However, modern science shows us these proportions of beauty are misguided. They are simply too idealistic to be realistic. Schmid Et al’s research found only a weak link between these Golden Ratios and Neoclassical canons, meaning they are not as closely linked to beauty as humans once thought.
                <br/><br/>
               Instead, in contemporary science, plastic surgeons and orthodontists use ‘Modern Anthropometry,’ where instead of relying on arbitrary proportions and one-size-fits-all shapes, we use demographic data of populations to establish the actual proportions that contribute to attractiveness for that group.
                <br/><br/>
               For example, the features that makes a                  
               <b><u>White Male</u></b>
                of
                <b><u>30 years age</u></b>
                 attractive, may not necessarily be the same proportions that make a 
              <b><u>Black Woman</u></b> of 
               <b><u>20 years age</u></b>
                attractive, which is why Modern Anthropometry is needed. Clincians must compare apples to apples to be precise.</font>"""
        str_figure_illustration = "FIG 2 : Ratios greater than 1.10 (i.e. there is a 110% difference between you and the most extreme comparisons) are shown here as they are dimorphic traits"
        pg_subject_style = ParagraphStyle(name="subject_style", alignment=TA_LEFT, fontName="NeueMontreal-Regular", fontSize=38, textColor=colors.HexColor('#121212'))
        pg_subject = Paragraph(str_subject, pg_subject_style)
        pg_content_title = Paragraph(str_content_title)
        pg_content = Paragraph(str_content)
        bCols = BalancedColumns([pg_content], nCols=2, vLinesStrokeWidth=1, innerPadding=10)
        pg_figure_illustration_style = ParagraphStyle(name='illustration_style', fontName=FONT_SPECIAL, leading=8, fontSize=8, textColor=colors.HexColor('#626262'))
        pg_figure_illustration = Paragraph(str_figure_illustration.upper(), pg_figure_illustration_style)
        self.elements.append(bCols)
        self.elements.append(NextFrameFlowable('frame_content_title_first'))
        self.elements.append(pg_content_title)
        self.elements.append(NextFrameFlowable('frame_figure_illustration'))
        self.elements.append(pg_figure_illustration)
        self.elements.append(NextFrameFlowable('frame_subject_first'))
        self.elements.append(pg_subject)
        page_template = PageTemplate(id='page_first', frames=[frame_content, frame_content_title, frame_figure_illustration, frame_subject,])
        self.doc.addPageTemplates(page_template)

    def second_page(self):
        self.elements.append(PageBreak())
        self.elements.append(Spacer(10, 50))

if __name__ == "__main__":
    TestReport('python_test.pdf')
