from openpyxl.styles.borders import Border, Side
from openpyxl.styles import Alignment, Color, PatternFill, Font
from openpyxl.worksheet.datavalidation import DataValidation
from collections import defaultdict

UIDs = [
    "harare", "lusaka", "sahara", "cardiff", "hanoi",
    "caracas", "montevideo", "washington", "kampala", "funafuti",
    "ashgabat", "ankara", "tiraspol", "lome", "bangkok",
    "dodoma", "dushanbe", "damascus", "bern", "stockholm",
    "paramaribo", "khartoum", "madrid", "juba", "seoul",
    "pretoria", "hargeisa", "mogadishu", "honiara", "ljubljana",
    "bratislava", "philipsburg", "singapore", "freetown", "belgrade",
]
FILL_0A = PatternFill(
    patternType='solid',
    fill_type='solid', fgColor=Color('aaaaaa')
)
FILL_0B = PatternFill(
    patternType='solid',
    fill_type='solid', fgColor=Color('dddddd')
)
FILL_1A = PatternFill(
    patternType='solid',
    fill_type='solid', fgColor=Color('ffc488')
)
FILL_1B = PatternFill(
    patternType='solid',
    fill_type='solid', fgColor=Color('ffe0c1')
)
FILL_2A = PatternFill(
    patternType='solid',
    fill_type='solid', fgColor=Color('ff7382')
)
FILL_2B = PatternFill(
    patternType='solid',
    fill_type='solid', fgColor=Color('ffb5bd')
)
FILL_3A = PatternFill(
    patternType='solid',
    fill_type='solid', fgColor=Color('8574fb')
)
FILL_3B = PatternFill(
    patternType='solid',
    fill_type='solid', fgColor=Color('beb5ff')
)
FILL_4A = PatternFill(
    patternType='solid',
    fill_type='solid', fgColor=Color('3c974b')
)
FILL_4B = PatternFill(
    patternType='solid',
    fill_type='solid', fgColor=Color('729b78')
)


THIN_BORDER_ALL = Border(
    left=Side(style='thin'),
    right=Side(style='thin'),
    top=Side(style='thin'),
    bottom=Side(style='thin')
)
MEDIUM_BORDER_RIGHT = Border(
    left=Side(style='thin'),
    right=Side(style='medium'),
    top=Side(style='thin'),
    bottom=Side(style='thin')
)
MEDIUM_BORDER_ALL = Border(
    left=Side(style='medium'),
    right=Side(style='medium'),
    top=Side(style='medium'),
    bottom=Side(style='medium')
)
THICK_BORDER_RIGHT = Border(
    left=Side(style='thin'),
    right=Side(style='thick'),
    top=Side(style='thin'),
    bottom=Side(style='thin')
)
THICK_BORDER_BOTTOM = Border(
    left=Side(style='thin'),
    right=Side(style='thin'),
    top=Side(style='thin'),
    bottom=Side(style='thick')
)

VALIDATION_NUM = defaultdict(lambda: DataValidation(
    type="whole",
    operator="between",
    formula1=0,
    formula2=6,
    errorStyle="stop",
))

VALIDATION_NONE = defaultdict(lambda: DataValidation(
    type="textLength",
    operator="between",
    formula1=0,
    formula2=0,
    errorStyle="stop",
))

FONT_BOLD = Font(bold=True, name="Calibri")
FONT_NORMAL = Font(bold=False, name="Calibri")
