from openpyxl.styles.borders import Border, Side
from openpyxl.styles import Alignment, Color, PatternFill, Font
from openpyxl.worksheet.datavalidation import DataValidation

UIDs = [
    "harare", "lusaka", "sahara", "cardiff", "hanoi",
    "caracas", "montevideo", "washington", "kampala", "funafuti",
    "ashgabat", "ankara", "tiraspol", "lome", "bangkok",
    "dodoma", "dushanbe", "damascus", "bern", "stockholm",
    "paramaribo", "khartoum", "madrid", "juba", "seoul",
    "pretoria", "hargeisa", "mogadishu", "honiara", "ljubljana",
    "bratislava", "philipsburg", "singapore", "freetown", "belgrade",
]
FILL_A_0 = PatternFill(
    patternType='solid',
    fill_type='solid', fgColor=Color('aaaaaa')
)
FILL_A_1 = PatternFill(
    patternType='solid',
    fill_type='solid', fgColor=Color('dddddd')
)
FILL_B_0 = PatternFill(
    patternType='solid',
    fill_type='solid', fgColor=Color('ffc488')
)
FILL_B_1 = PatternFill(
    patternType='solid',
    fill_type='solid', fgColor=Color('ffe0c1')
)
FILL_F_0 = PatternFill(
    patternType='solid',
    fill_type='solid', fgColor=Color('ff7382')
)
FILL_F_1 = PatternFill(
    patternType='solid',
    fill_type='solid', fgColor=Color('ffb5bd')
)
FILL_J_0 = PatternFill(
    patternType='solid',
    fill_type='solid', fgColor=Color('8574fb')
)
FILL_J_1 = PatternFill(
    patternType='solid',
    fill_type='solid', fgColor=Color('beb5ff')
)
FILL_N_0 = PatternFill(
    patternType='solid',
    fill_type='solid', fgColor=Color('3c974b')
)
FILL_N_1 = PatternFill(
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

NUM_VALIDATION = DataValidation(
    type="whole",
    operator="between",
    formula1=0,
    formula2=6,
)
