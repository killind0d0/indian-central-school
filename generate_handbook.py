import os
import sys
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.units import inch, cm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# ----------------------------------------------------------------------
# Register Fonts & Font Families
# ----------------------------------------------------------------------
FONTS_DIR = "/usr/share/fonts/truetype/dejavu"
pdfmetrics.registerFont(TTFont('DejaVuSerif', os.path.join(FONTS_DIR, 'DejaVuSerif.ttf')))
pdfmetrics.registerFont(TTFont('DejaVuSerif-Bold', os.path.join(FONTS_DIR, 'DejaVuSerif-Bold.ttf')))
pdfmetrics.registerFont(TTFont('DejaVuSerif-Italic', os.path.join(FONTS_DIR, 'DejaVuSerif-Italic.ttf')))
pdfmetrics.registerFont(TTFont('DejaVuSerif-BoldItalic', os.path.join(FONTS_DIR, 'DejaVuSerif-BoldItalic.ttf')))

pdfmetrics.registerFont(TTFont('DejaVuSans', os.path.join(FONTS_DIR, 'DejaVuSans.ttf')))
pdfmetrics.registerFont(TTFont('DejaVuSans-Bold', os.path.join(FONTS_DIR, 'DejaVuSans-Bold.ttf')))
pdfmetrics.registerFont(TTFont('DejaVuSans-Oblique', os.path.join(FONTS_DIR, 'DejaVuSans-Oblique.ttf')))
pdfmetrics.registerFont(TTFont('DejaVuSans-BoldOblique', os.path.join(FONTS_DIR, 'DejaVuSans-BoldOblique.ttf')))

pdfmetrics.registerFont(TTFont('DejaVuSansMono', os.path.join(FONTS_DIR, 'DejaVuSansMono.ttf')))
pdfmetrics.registerFont(TTFont('DejaVuSansMono-Bold', os.path.join(FONTS_DIR, 'DejaVuSansMono-Bold.ttf')))

pdfmetrics.registerFontFamily(
    'DejaVuSerif',
    normal='DejaVuSerif',
    bold='DejaVuSerif-Bold',
    italic='DejaVuSerif-Italic',
    boldItalic='DejaVuSerif-BoldItalic'
)

pdfmetrics.registerFontFamily(
    'DejaVuSans',
    normal='DejaVuSans',
    bold='DejaVuSans-Bold',
    italic='DejaVuSans-Oblique',
    boldItalic='DejaVuSans-BoldOblique'
)

# ----------------------------------------------------------------------
# Numbered Canvas for "Page X of Y" and Running Headers/Footers
# ----------------------------------------------------------------------
class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        page_w, page_h = self._pagesize

        # Do not draw headers/footers on cover page (page 1)
        if self._pageNumber > 1:
            # Running Header
            self.setFont("DejaVuSans-Bold", 7.5)
            self.setFillColor(colors.HexColor("#0B192C"))
            self.drawString(40, page_h - 30, "INDIAN CENTRAL SCHOOL, GAYA JI")
            
            self.setFont("DejaVuSans", 7.5)
            self.setFillColor(colors.HexColor("#64748B"))
            self.drawString(200, page_h - 30, "— Administrative Portal Operations & Handover Manual")
            
            # Gold mini-badge right
            self.setFont("DejaVuSans-Bold", 7)
            self.setFillColor(colors.HexColor("#B45309"))
            self.drawRightString(page_w - 40, page_h - 30, "SJ ENTERPRISES HANDOVER")

            # Top thin divider line
            self.setStrokeColor(colors.HexColor("#D4AF37"))
            self.setLineWidth(1)
            self.line(40, page_h - 35, page_w - 40, page_h - 35)

            # Running Footer
            self.setStrokeColor(colors.HexColor("#E2E8F0"))
            self.setLineWidth(0.75)
            self.line(40, 42, page_w - 40, 42)

            # Footer text left
            self.setFont("DejaVuSans", 7.5)
            self.setFillColor(colors.HexColor("#64748B"))
            self.drawString(40, 30, "Confidential • Strictly for School Leadership & IT Administration • Indian Central School, Gaya Ji")

            # Footer text right (Page X of Y)
            self.setFont("DejaVuSans-Bold", 8)
            self.setFillColor(colors.HexColor("#0B192C"))
            self.drawRightString(page_w - 40, 30, f"Page {self._pageNumber} of {page_count}")
        
        self.restoreState()

# ----------------------------------------------------------------------
# PDF Generation Function
# ----------------------------------------------------------------------
def build_handbook(output_pdf_path):
    doc = SimpleDocTemplate(
        output_pdf_path,
        pagesize=A4,
        leftMargin=40,
        rightMargin=40,
        topMargin=46,
        bottomMargin=48
    )

    # Palette
    C_NAVY = colors.HexColor("#0B192C")
    C_DEEP_BLUE = colors.HexColor("#1B365D")
    C_GOLD = colors.HexColor("#D4AF37")
    C_AMBER = colors.HexColor("#B45309")
    C_CREAM = colors.HexColor("#FAF8F5")
    C_CREAM_ALT = colors.HexColor("#F5F0E8")
    C_SLATE = colors.HexColor("#334155")
    C_LIGHT_SLATE = colors.HexColor("#64748B")
    C_BORDER = colors.HexColor("#E2E8F0")
    C_EMERALD = colors.HexColor("#059669")
    C_EMERALD_BG = colors.HexColor("#ECFDF5")
    C_ROSE = colors.HexColor("#DC2626")

    # Typography Styles
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='DejaVuSerif-Bold',
        fontSize=20,
        leading=24,
        textColor=C_NAVY,
        spaceAfter=6
    )

    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='DejaVuSans',
        fontSize=10.5,
        leading=15,
        textColor=C_AMBER,
        spaceAfter=12
    )

    h1_style = ParagraphStyle(
        'SectionHeading1',
        parent=styles['Heading1'],
        fontName='DejaVuSerif-Bold',
        fontSize=14,
        leading=18,
        textColor=C_NAVY,
        spaceBefore=12,
        spaceAfter=6,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'SectionHeading2',
        parent=styles['Heading2'],
        fontName='DejaVuSerif-Bold',
        fontSize=11,
        leading=15,
        textColor=C_DEEP_BLUE,
        spaceBefore=8,
        spaceAfter=4,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'BodyDark',
        parent=styles['BodyText'],
        fontName='DejaVuSans',
        fontSize=8.5,
        leading=12.5,
        textColor=C_SLATE,
        spaceAfter=6
    )

    body_bold = ParagraphStyle(
        'BodyDarkBold',
        parent=body_style,
        fontName='DejaVuSans-Bold'
    )

    code_style = ParagraphStyle(
        'CodeStyle',
        parent=styles['Code'],
        fontName='DejaVuSansMono-Bold',
        fontSize=8.5,
        leading=11,
        textColor=C_NAVY
    )

    callout_text = ParagraphStyle(
        'CalloutText',
        parent=styles['Normal'],
        fontName='DejaVuSans',
        fontSize=8.5,
        leading=12,
        textColor=C_NAVY
    )

    table_header = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='DejaVuSans-Bold',
        fontSize=8,
        leading=10,
        textColor=colors.white
    )

    table_cell = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='DejaVuSans',
        fontSize=7.8,
        leading=10.5,
        textColor=C_SLATE
    )

    table_cell_bold = ParagraphStyle(
        'TableCellBold',
        parent=styles['Normal'],
        fontName='DejaVuSans-Bold',
        fontSize=8,
        leading=11,
        textColor=C_NAVY
    )

    story = []

    # =========================================================================
    # COVER PAGE
    # =========================================================================
    # Top Decorative Strip
    banner_data = [
        [
            Paragraph("<font color='#D4AF37' size='8'><b>HANDOVER DOCUMENT • CONFIDENTIAL &amp; RESTRICTED</b></font>", ParagraphStyle('H1', fontName='DejaVuSans-Bold', textColor=C_GOLD)),
            Paragraph("<font color='#FFFFFF' size='7.5'>DOCUMENT REF: SJ-ICS-2026-ADM</font>", ParagraphStyle('H2', fontName='DejaVuSans-Bold', alignment=2, textColor=colors.white))
        ]
    ]
    banner_table = Table(banner_data, colWidths=[330, 185])
    banner_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), C_NAVY),
        ('PADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('ALIGN', (1,0), (1,0), 'RIGHT'),
    ]))
    story.append(banner_table)
    story.append(Spacer(1, 15))

    # Crest & Header Section
    logo_path = "/home/killindodo/Projects/indian-central-school/assets/logo.png"
    if os.path.exists(logo_path):
        img = Image(logo_path, width=1.1*inch, height=1.1*inch)
    else:
        img = Paragraph("<b>[ICS LOGO]</b>", body_bold)

    crest_data = [
        [
            img,
            [
                Paragraph("INDIAN CENTRAL SCHOOL", ParagraphStyle('C1', fontName='DejaVuSerif-Bold', fontSize=18, leading=21, textColor=C_NAVY)),
                Paragraph("A.T. Gate, Gaya Ji (Gaya - Sherghati Road, Bihar)", ParagraphStyle('C2', fontName='DejaVuSans', fontSize=9, leading=12, textColor=C_LIGHT_SLATE)),
                Spacer(1, 4),
                Paragraph("<font color='#D4AF37'><b>OFFICIAL ADMINISTRATIVE PORTAL OPERATIONS MANUAL</b></font>", ParagraphStyle('C3', fontName='DejaVuSans-Bold', fontSize=9.5, leading=13, textColor=C_GOLD)),
                Paragraph("Comprehensive Guide for Portal Authentication, Content Management, Staff Delegation & Approval Queue Governance", ParagraphStyle('C4', fontName='DejaVuSans-Oblique', fontSize=8, leading=11, textColor=C_SLATE))
            ]
        ]
    ]
    crest_table = Table(crest_data, colWidths=[1.3*inch, 5.8*inch])
    crest_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('LEFTPADDING', (1,0), (1,0), 10),
        ('PADDING', (0,0), (-1,-1), 2),
    ]))
    story.append(crest_table)
    story.append(Spacer(1, 10))
    story.append(HRFlowable(width="100%", thickness=1.5, color=C_GOLD, spaceBefore=4, spaceAfter=14))

    # Handover Metadata Box
    meta_data = [
        [
            Paragraph("<b>Issuing Agency:</b>", table_cell_bold),
            Paragraph("<b>SJ Enterprises / SJ Digitals</b> (Digital Architecture & Web Engineering)", table_cell),
            Paragraph("<b>Portal Version:</b>", table_cell_bold),
            Paragraph("<b>v2.4 (Security Hardened)</b>", table_cell)
        ],
        [
            Paragraph("<b>Authorized Recipient:</b>", table_cell_bold),
            Paragraph("Director, Principal & Administrative Council — ICS Gaya Ji", table_cell),
            Paragraph("<b>Release Date:</b>", table_cell_bold),
            Paragraph("October 30, 2026 (Academic Session 2026–27)", table_cell)
        ],
        [
            Paragraph("<b>Production Domain:</b>", table_cell_bold),
            Paragraph("<font color='#0B192C'><b>https://icsgayaji.org/admin.html</b></font>", table_cell),
            Paragraph("<b>Offline Environment:</b>", table_cell_bold),
            Paragraph("http://localhost:8085/admin.html", table_cell)
        ]
    ]
    meta_table = Table(meta_data, colWidths=[110, 200, 95, 110])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), C_CREAM),
        ('BOX', (0,0), (-1,-1), 1, C_BORDER),
        ('INNERGRID', (0,0), (-1,-1), 0.5, C_BORDER),
        ('PADDING', (0,0), (-1,-1), 5.5),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 14))

    # Executive Summary / Foreword
    foreword_html = (
        "<b>Executive Handover Notice from SJ Enterprises:</b><br/>"
        "SJ Enterprises is proud to deliver this upgraded, institutional-grade administrative control platform "
        "tailored exclusively for <b>Indian Central School, Gaya Ji</b>. This manual provides complete operational "
        "instructions for school administrators to manage all public digital assets—including urgent circulars, "
        "faculty records, academic achievements, and campus infrastructure—while delegating publishing duties safely "
        "to teachers via our newly engineered <b>Toggleable Approval Queue Engine</b>."
    )
    fwd_table = Table([[Paragraph(foreword_html, callout_text)]], colWidths=[515])
    fwd_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#EFF6FF")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#93C5FD")),
        ('PADDING', (0,0), (-1,-1), 8),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(fwd_table)
    story.append(Spacer(1, 14))

    # Credentials Quick Reference (Boxed & Highlighted)
    story.append(Paragraph("1. QUICK CREDENTIALS & ACCESS KEYS (STRICTLY CONFIDENTIAL)", h1_style))
    story.append(Paragraph("Keep these credentials secure. Never distribute the master administrator passcode outside the executive board.", body_style))

    creds_data = [
        [
            Paragraph("ROLE IDENTITY", table_header),
            Paragraph("USER IDENTITY", table_header),
            Paragraph("PASSCODE / KEY", table_header),
            Paragraph("CONTROL SCOPE & PERMISSIONS", table_header)
        ],
        [
            Paragraph("<b>School Administrator</b><br/><font color='#D97706' size='7'>MASTER LEVEL</font>", table_cell_bold),
            Paragraph("Director / Principal / IT Head<br/><i>(Primary Console)</i>", table_cell),
            Paragraph("<font color='#0B192C' size='9'><b>ics@2026</b></font><br/><font color='#64748B' size='6.5'>Default Admin Passcode</font>", table_cell_bold),
            Paragraph("<b>Unrestricted Master Control.</b> Direct edits across all 5 modules, approve or decline staff proposals, toggle approval queue ON/OFF, reset teacher passcodes, review audit logs.", table_cell)
        ],
        [
            Paragraph("<b>Teacher / Faculty</b><br/><font color='#059669' size='7'>DELEGATED LEVEL</font>", table_cell_bold),
            Paragraph("Class Teachers, Academic Heads, Exam In-charges", table_cell),
            Paragraph("<font color='#0B192C' size='9'><b>staff@2026</b></font><br/><font color='#64748B' size='6.5'>Default Staff Passcode</font>", table_cell_bold),
            Paragraph("<b>Delegated Operations.</b> Create, edit, and delete notices or faculty records. When queue is ON, submissions require Admin approval. When OFF, publishes directly to live site.", table_cell)
        ]
    ]
    creds_table = Table(creds_data, colWidths=[95, 115, 95, 210])
    creds_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), C_NAVY),
        ('BACKGROUND', (0,1), (-1,1), colors.HexColor("#FEF3C7")),
        ('BACKGROUND', (0,2), (-1,2), C_CREAM),
        ('BOX', (0,0), (-1,-1), 1, C_GOLD),
        ('INNERGRID', (0,0), (-1,-1), 0.5, C_BORDER),
        ('PADDING', (0,0), (-1,-1), 6),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(creds_table)
    story.append(Spacer(1, 10))

    # Portal URLs summary
    url_box = [
        [
            Paragraph("<b>Live Website Portal:</b>", table_cell_bold),
            Paragraph("<b>https://icsgayaji.org/admin.html</b> (Official Production Admin Panel)", table_cell),
        ],
        [
            Paragraph("<b>Offline Local Portal:</b>", table_cell_bold),
            Paragraph("<b>http://localhost:8085/admin.html</b> (Safe offline sandbox powered by <code>python3 server.py</code>)", table_cell),
        ]
    ]
    url_table = Table(url_box, colWidths=[120, 395])
    url_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), C_CREAM_ALT),
        ('BOX', (0,0), (-1,-1), 1, C_BORDER),
        ('INNERGRID', (0,0), (-1,-1), 0.5, C_BORDER),
        ('PADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(url_table)

    story.append(PageBreak())

    # =========================================================================
    # SECTION 2: THE TOGGLEABLE APPROVAL QUEUE ENGINE
    # =========================================================================
    story.append(Paragraph("2. STAFF DELEGATION & THE TOGGLEABLE APPROVAL QUEUE", h1_style))
    story.append(Paragraph(
        "A cornerstone feature engineered into the ICS portal is the <b>Toggleable Admin Approval Queue</b>. "
        "School leadership requested the ability to empower teachers to submit circulars and directory updates, "
        "while retaining executive authority to decide whether submissions require administrative sign-off "
        "or publish directly to the live website.", body_style
    ))

    # Two Modes Explanation Table
    modes_data = [
        [
            Paragraph("OPERATING MODE", table_header),
            Paragraph("HOW IT WORKS", table_header),
            Paragraph("STAFF EXPERIENCE", table_header),
            Paragraph("ADMIN CONTROL", table_header)
        ],
        [
            Paragraph("<b>1. Approval Required<br/>(Queue Mode)</b><br/><font color='#D97706'><b>[DEFAULT & RECOMMENDED]</b></font>", table_cell_bold),
            Paragraph("Teacher proposals are quarantined in the <b>Pending Approvals Queue</b> in <code>data/permissions.json</code>. Live website is NOT touched until approved.", table_cell),
            Paragraph("Save button shows: <i>'Submit for Admin Approval'</i>. Staff sees proposal in their tracking list with status <i>'Under Review'</i>.", table_cell),
            Paragraph("Administrator receives pending badge, inspects proposed changes, and clicks <b>Approve</b> (goes live immediately) or <b>Reject</b> (with feedback note).", table_cell)
        ],
        [
            Paragraph("<b>2. Direct Publish<br/>(Live Direct Mode)</b><br/><font color='#059669'><b>[RAPID EVENTS MODE]</b></font>", table_cell_bold),
            Paragraph("Teacher updates bypass the approval queue and write <b>immediately</b> to the live website JSON datasets (<code>data/notices.json</code>, etc.).", table_cell),
            Paragraph("Save button updates dynamically to: <i>'Save Notice Live'</i> or <i>'Post New Notice (Direct)'</i>. Updates reflect instantly.", table_cell),
            Paragraph("<b>Complete audit visibility:</b> The system logs every staff action with actor name, timestamp, and details in the <b>Activity Audit Log</b> for review.", table_cell)
        ]
    ]
    modes_table = Table(modes_data, colWidths=[110, 140, 130, 135])
    modes_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), C_NAVY),
        ('BACKGROUND', (0,1), (-1,1), colors.HexColor("#FFFBEB")),
        ('BACKGROUND', (0,2), (-1,2), C_EMERALD_BG),
        ('BOX', (0,0), (-1,-1), 1, C_BORDER),
        ('INNERGRID', (0,0), (-1,-1), 0.5, C_BORDER),
        ('PADDING', (0,0), (-1,-1), 6),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(modes_table)
    story.append(Spacer(1, 10))

    # How to Toggle Guide
    story.append(Paragraph("How the Administrator Can Toggle the Approval Setting at Any Time:", h2_style))
    step_items = [
        "<b>Step 1:</b> Log in as <b>School Administrator</b> at <code>/admin.html</code> using passcode <code>ics@2026</code>.",
        "<b>Step 2:</b> In the sidebar navigation, click on <b>'Approvals & Staff Control'</b>.",
        "<b>Step 3:</b> Click on the <b>'Portal Security & Access'</b> sub-tab.",
        "<b>Step 4:</b> Locate the card titled <b>'Require Admin Approval for Staff Updates'</b>:",
        "&nbsp;&nbsp;&bull; <b>TOGGLE ON:</b> Switches system to <i>Queue Mode</i>. Teachers cannot publish live without admin sign-off.",
        "&nbsp;&nbsp;&bull; <b>TOGGLE OFF:</b> Switches system to <i>Direct Publish Mode</i>. Teachers can post updates directly.",
        "<b>Step 5:</b> The change takes effect immediately across all devices, updates the live badge, and is recorded in the permanent audit trail."
    ]
    for s in step_items:
        story.append(Paragraph(s, body_style))

    story.append(Spacer(1, 6))

    # Granular Module Permissions
    story.append(Paragraph("Granular Staff Permission Switches:", h2_style))
    story.append(Paragraph(
        "Beneath the approval toggle, administrators can selectively toggle permissions for individual modules. "
        "For example, you can allow teachers to post <b>Notices & Circulars</b> and update <b>Faculty Profiles</b>, "
        "while restricting access to <b>Campus Facilities</b> and <b>Advisory Committee</b>.", body_style
    ))

    # Emergency Master Switch
    em_html = (
        "<b>Emergency Portal Gatekeeper ('Teacher Login Allowed' switch):</b><br/>"
        "If the administrator toggles off 'Teacher Login Allowed', all staff members are locked out of the portal "
        "instantly. Use this during summer vacations, examination grading periods, or security rotations."
    )
    em_table = Table([[Paragraph(em_html, callout_text)]], colWidths=[515])
    em_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#FEF2F2")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#FCA5A5")),
        ('PADDING', (0,0), (-1,-1), 7),
    ]))
    story.append(em_table)

    story.append(PageBreak())

    # =========================================================================
    # SECTION 3: STEP-BY-STEP MODULE WORKFLOWS
    # =========================================================================
    story.append(Paragraph("3. MODULE MANAGEMENT & LIVE PUBLISHING GUIDE", h1_style))
    story.append(Paragraph("The portal controls five core modules powering the public website:", body_style))

    module_data = [
        [
            Paragraph("MODULE NAME", table_header),
            Paragraph("LIVE LOCATION ON WEBSITE", table_header),
            Paragraph("KEY ATTRIBUTES & FEATURES", table_header)
        ],
        [
            Paragraph("<b>1. Notices & Circulars</b>", table_cell_bold),
            Paragraph("Homepage Ticker, Spotlight Card & <code>notices.html</code>", table_cell),
            Paragraph("Headline, Category (Olympiad, Academic, Parent Advisory, Media Press), Academic Session, Urgent Alert Tag, Description, and High-Resolution Circular Image.", table_cell)
        ],
        [
            Paragraph("<b>2. Faculty Directory</b>", table_cell_bold),
            Paragraph("<code>faculty.html</code> & Academics page", table_cell),
            Paragraph("Teacher Name, Department, Academic Subject, Educational Qualifications (M.Sc, B.Ed, etc.), Bio, and Professional Photograph.", table_cell)
        ],
        [
            Paragraph("<b>3. Hall of Fame / Awards</b>", table_cell_bold),
            Paragraph("<code>achievements.html</code> & Homepage", table_cell),
            Paragraph("Student Name, Competition Title, Medal / Award Category, Year, and Certificate / Trophy Photograph.", table_cell)
        ],
        [
            Paragraph("<b>4. Campus & Facilities</b>", table_cell_bold),
            Paragraph("<code>facilities.html</code> & Virtual Tour", table_cell),
            Paragraph("Facility Name (Smart Classrooms, Science Labs, Library, Fleet GPS), Description, Features list, and Gallery Image.", table_cell)
        ],
        [
            Paragraph("<b>5. Advisory Committee</b>", table_cell_bold),
            Paragraph("<code>about.html</code> Leadership section", table_cell),
            Paragraph("Committee Member Name, Institutional Designation, Academic Background, and Advisory Statement.", table_cell)
        ]
    ]
    mod_table = Table(module_data, colWidths=[120, 160, 235])
    mod_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), C_NAVY),
        ('BACKGROUND', (0,1), (-1,1), C_CREAM),
        ('BACKGROUND', (0,2), (-1,2), colors.white),
        ('BACKGROUND', (0,3), (-1,3), C_CREAM),
        ('BACKGROUND', (0,4), (-1,4), colors.white),
        ('BACKGROUND', (0,5), (-1,5), C_CREAM),
        ('BOX', (0,0), (-1,-1), 1, C_BORDER),
        ('INNERGRID', (0,0), (-1,-1), 0.5, C_BORDER),
        ('PADDING', (0,0), (-1,-1), 5.5),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(mod_table)
    story.append(Spacer(1, 10))

    # Spotlight on Health Checkup Camp Notice
    story.append(Paragraph("Spotlight: The Multi-Specialty Health Checkup Camp Notice", h2_style))
    health_text = (
        "As part of this update, the <b>Multi-Specialty Health Checkup Camp</b> notice has been successfully "
        "published live to <code>icsgayaji.org</code>. It is highlighted with a <b>🚨 Urgent</b> badge "
        "and is synchronized across the top of <code>notices.html</code>, the JSON database (<code>data/notices.json</code>), "
        "and the homepage spotlight card in <code>index.html</code>. "
        "The original high-resolution banner is archived at <code>assets/notices/checkupics.jpeg</code>."
    )
    story.append(Paragraph(health_text, body_style))

    # How to Add a Notice (Step-by-step)
    story.append(Paragraph("Standard Procedure to Post a Notice:", h2_style))
    n_steps = [
        "1. Click <b>'Notices & Circulars'</b> in the dashboard sidebar.",
        "2. Click the gold <b>'+ Post New Notice'</b> button in the top right.",
        "3. Enter the <b>Notice Title</b>, select the <b>Category</b>, and specify the <b>Session</b> (e.g. <i>Session 2026–27</i>).",
        "4. Check <b>'Mark as Urgent'</b> if the notice requires immediate parental attention (creates a red emergency banner).",
        "5. Attach an image: Either upload directly from your computer or provide a file path.",
        "6. Click <b>'Publish Notice'</b> (if Admin or Direct Mode) or <b>'Submit for Admin Approval'</b> (if Staff in Queue Mode)."
    ]
    for ns in n_steps:
        story.append(Paragraph(ns, body_style))

    story.append(Spacer(1, 10))

    # Moderating the Pending Approvals Queue
    story.append(Paragraph("Moderating the Pending Approvals Queue (Admin Workflow):", h2_style))
    m_steps = [
        "1. Open <b>'Approvals & Staff Control'</b> &rarr; <b>'Pending Approvals Queue'</b>.",
        "2. Pending proposals submitted by teachers display the teacher's name, target module, proposed title, and attached image.",
        "3. To accept: Click <b>'Approve Proposal'</b>. The system automatically inserts or edits the live dataset, creates an audit entry, and updates the website.",
        "4. To decline: Click <b>'Reject'</b>. Enter an administrative feedback note explaining what the teacher needs to adjust."
    ]
    for ms in m_steps:
        story.append(Paragraph(ms, body_style))

    story.append(PageBreak())

    # =========================================================================
    # SECTION 4: SECURITY ARCHITECTURE & AUDIT TRAIL
    # =========================================================================
    story.append(Paragraph("4. SECURITY GOVERNANCE & AUDIT LOGGING", h1_style))
    story.append(Paragraph(
        "To ensure institutional transparency and prevent unauthorized tampering, the portal incorporates "
        "several layers of enterprise security:", body_style
    ))

    sec_items = [
        ("<b>Permanent Activity Audit Log:</b>", 
         "Every single action performed in the console—including admin approvals, teacher direct posts, edits, deletions, and passcode updates—is permanently recorded in <code>data/permissions.json</code>. The log records the actor's name, assigned role, exact timestamp, action category, and detailed description."),
        
        ("<b>Input Sanitization (Anti-XSS Engine):</b>", 
         "All text inputs (titles, summaries, captions, doctor names) are filtered through a robust HTML entity sanitization pipeline (<code>escapeHtml</code>) that neutralizes script injections, quotes, and malicious tags before rendering."),

        ("<b>Passcode Protection & Rotation:</b>", 
         "The administrator can change the staff passcode at any time directly in the console. Updating the passcode immediately applies to all teachers across all devices without needing to touch server configuration files."),

        ("<b>Zero Plaintext Secret Exposure:</b>", 
         "Administrative hints (such as <code>Default: ics@2026</code>) have been hardened so they are automatically hidden on public production domains (<code>icsgayaji.org</code>) and only visible in local offline development."),

        ("<b>Local Testing Safety Net (server.py):</b>", 
         "The included Python backend (<code>server.py</code>) allows school administrators to preview, test, and verify complex updates on a secure offline computer before publishing them to the public internet.")
    ]

    for title, desc in sec_items:
        story.append(Paragraph(f"{title} {desc}", body_style))
        story.append(Spacer(1, 3))

    story.append(Spacer(1, 10))

    # Audit Log Table Sample
    story.append(Paragraph("Sample Activity Audit Log View (as seen in Admin Dashboard):", h2_style))
    audit_data = [
        [
            Paragraph("TIMESTAMP", table_header),
            Paragraph("ACTOR & ROLE", table_header),
            Paragraph("ACTION PERFORMED", table_header),
            Paragraph("DETAILS & METADATA", table_header)
        ],
        [
            Paragraph("2026-10-30 13:00", table_cell),
            Paragraph("<b>Dr. Mirdula Kumari</b><br/><font color='#059669'>Teacher / Staff</font>", table_cell),
            Paragraph("Notice Published (Staff Direct)", table_cell_bold),
            Paragraph("Annual Science Exhibition 2026 [Direct publish by Dr. Mirdula Kumari]", table_cell)
        ],
        [
            Paragraph("2026-10-30 12:45", table_cell),
            Paragraph("<b>School Administrator</b><br/><font color='#D97706'>Administrator</font>", table_cell),
            Paragraph("Approval Requirement Changed", table_cell_bold),
            Paragraph("Teacher updates will now publish directly to live website without queue", table_cell)
        ],
        [
            Paragraph("2026-10-30 10:55", table_cell),
            Paragraph("<b>School Administrator</b><br/><font color='#D97706'>Administrator</font>", table_cell),
            Paragraph("Notice Added", table_cell_bold),
            Paragraph("Multi-Specialty Health Checkup Camp notice published live", table_cell)
        ]
    ]
    audit_table = Table(audit_data, colWidths=[80, 110, 140, 185])
    audit_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), C_NAVY),
        ('BACKGROUND', (0,1), (-1,1), C_CREAM),
        ('BACKGROUND', (0,2), (-1,2), colors.white),
        ('BACKGROUND', (0,3), (-1,3), C_CREAM),
        ('BOX', (0,0), (-1,-1), 1, C_BORDER),
        ('INNERGRID', (0,0), (-1,-1), 0.5, C_BORDER),
        ('PADDING', (0,0), (-1,-1), 5),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(audit_table)
    story.append(Spacer(1, 14))

    # =========================================================================
    # HANDOVER SIGN-OFF & ENGINEERING SEAL
    # =========================================================================
    sign_html = (
        "<b>CERTIFICATE OF SYSTEM HANDOVER & ENGINEERING CONFORMANCE</b><br/>"
        "This administrative portal, documentation, and underlying data structures have been designed, hardened, "
        "and formally verified by <b>SJ Enterprises / SJ Digitals</b>. All systems conform to institutional web safety "
        "standards, zero-downtime static delivery, and modern responsive design guidelines.<br/><br/>"
        "<b>Lead Engineering Architect:</b> SJ Enterprises Digital Engineering Team<br/>"
        "<b>Client Institution:</b> Indian Central School, A.T. Gate, Gaya Ji, Bihar<br/>"
        "<b>Support Channel:</b> contact@sjenterprises.in • https://sjdigitals.vercel.app"
    )
    sign_table = Table([[Paragraph(sign_html, callout_text)]], colWidths=[515])
    sign_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), C_CREAM_ALT),
        ('BOX', (0,0), (-1,-1), 1.5, C_GOLD),
        ('PADDING', (0,0), (-1,-1), 9),
    ]))
    story.append(sign_table)

    # Build the document using the NumberedCanvas
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Successfully generated {output_pdf_path}!")

if __name__ == '__main__':
    target = sys.argv[1] if len(sys.argv) > 1 else "ICS_Admin_Portal_Handbook_SJEnterprises.pdf"
    build_handbook(target)
