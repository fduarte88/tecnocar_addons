from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, KeepTogether
)
from reportlab.graphics.shapes import Drawing, Rect
from reportlab.lib.colors import HexColor

PRIMARY   = HexColor('#1a1a2e')
ACCENT    = HexColor('#f59e0b')
LIGHT     = HexColor('#f8fafc')
BORDER    = HexColor('#e2e8f0')
TEXT_MUTED = HexColor('#64748b')
WHITE     = colors.white

ACCESORIOS = [
    ('acc_gato',            'Gato'),
    ('acc_llave_rueda',     'Llave de Rueda'),
    ('acc_baliza',          'Baliza'),
    ('acc_extintor',        'Extintor'),
    ('acc_compresor',       'Compresor'),
    ('acc_rueda_auxilio',   'Rueda de Auxilio'),
    ('acc_alfombras',       'Alfombras'),
    ('acc_tuerca_seguridad','Tuerca de Seguridad'),
]


def _estilos():
    base = getSampleStyleSheet()
    estilos = {
        'titulo_empresa': ParagraphStyle(
            'titulo_empresa', fontSize=18, fontName='Helvetica-Bold',
            textColor=WHITE, leading=22,
        ),
        'subtitulo_empresa': ParagraphStyle(
            'subtitulo_empresa', fontSize=9, fontName='Helvetica',
            textColor=HexColor('#fbbf24'), leading=12,
        ),
        'hr_numero': ParagraphStyle(
            'hr_numero', fontSize=22, fontName='Helvetica-Bold',
            textColor=ACCENT, alignment=TA_RIGHT, leading=26,
        ),
        'hr_label': ParagraphStyle(
            'hr_label', fontSize=8, fontName='Helvetica',
            textColor=TEXT_MUTED, alignment=TA_RIGHT, leading=10,
        ),
        'seccion_titulo': ParagraphStyle(
            'seccion_titulo', fontSize=8, fontName='Helvetica-Bold',
            textColor=WHITE, leading=10, spaceAfter=0,
        ),
        'campo_label': ParagraphStyle(
            'campo_label', fontSize=7.5, fontName='Helvetica',
            textColor=TEXT_MUTED, leading=10,
        ),
        'campo_valor': ParagraphStyle(
            'campo_valor', fontSize=9, fontName='Helvetica-Bold',
            textColor=PRIMARY, leading=12,
        ),
        'solicitud': ParagraphStyle(
            'solicitud', fontSize=9, fontName='Helvetica',
            textColor=PRIMARY, leading=13, spaceAfter=4,
        ),
        'autorizacion': ParagraphStyle(
            'autorizacion', fontSize=9, fontName='Helvetica-Oblique',
            textColor=TEXT_MUTED, leading=13, alignment=TA_CENTER,
        ),
        'firma_label': ParagraphStyle(
            'firma_label', fontSize=9, fontName='Helvetica-Bold',
            textColor=PRIMARY, alignment=TA_CENTER, leading=12,
        ),
    }
    return estilos


def _header(ficha, st):
    """Cabecera con logo y número HR."""
    fecha_str = ficha.fecha_ingreso.strftime('%d/%m/%Y  %H:%M')

    # Columna izquierda: empresa
    col_izq = [
        Paragraph('TecnoCar', st['titulo_empresa']),
        Paragraph('Taller Automotriz', st['subtitulo_empresa']),
    ]
    # Columna derecha: número HR y fecha
    col_der = [
        Paragraph('HOJA DE RECEPCIÓN', st['hr_label']),
        Paragraph(f'HR-{ficha.pk:04d}', st['hr_numero']),
        Paragraph(fecha_str, st['hr_label']),
    ]

    header_table = Table(
        [[col_izq, col_der]],
        colWidths=[10*cm, 8.5*cm],
    )
    header_table.setStyle(TableStyle([
        ('BACKGROUND',  (0,0), (-1,-1), PRIMARY),
        ('VALIGN',      (0,0), (-1,-1), 'MIDDLE'),
        ('LEFTPADDING', (0,0), (0,0), 18),
        ('RIGHTPADDING',(-1,0),(-1,0), 18),
        ('TOPPADDING',  (0,0), (-1,-1), 14),
        ('BOTTOMPADDING',(0,0),(-1,-1), 14),
        ('ROUNDEDCORNERS', [6, 6, 6, 6]),
    ]))
    return header_table


def _titulo_seccion(texto):
    d = Drawing(18.5*cm, 1.3*cm)
    d.add(Rect(0, 0, 18.5*cm, 1.3*cm, fillColor=PRIMARY, strokeColor=None, rx=3, ry=3))
    return d, Paragraph(f'  {texto}', ParagraphStyle(
        'sec', fontSize=8, fontName='Helvetica-Bold',
        textColor=WHITE, leading=10,
    ))


def _fila(label, valor):
    st = _estilos()
    return [Paragraph(label, st['campo_label']), Paragraph(str(valor) if valor else '—', st['campo_valor'])]


def _tabla_datos(filas, col_widths):
    t = Table(filas, colWidths=col_widths)
    t.setStyle(TableStyle([
        ('BACKGROUND',   (0,0), (-1,-1), LIGHT),
        ('LINEBELOW',    (0,0), (-1,-1), 0.3, BORDER),
        ('TOPPADDING',   (0,0), (-1,-1), 5),
        ('BOTTOMPADDING',(0,0), (-1,-1), 5),
        ('LEFTPADDING',  (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ('VALIGN',       (0,0), (-1,-1), 'TOP'),
    ]))
    return t


def generar_pdf_hoja_recepcion(ficha):
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        leftMargin=1.5*cm,
        rightMargin=1.5*cm,
        topMargin=1.5*cm,
        bottomMargin=1.5*cm,
    )
    st = _estilos()
    v = ficha.vehiculo
    c = v.cliente
    W = 18.5*cm   # ancho útil
    C2 = W / 2    # mitad
    C3 = W / 3    # tercio

    elements = []

    # ── CABECERA ──────────────────────────────────────────────────
    elements.append(_header(ficha, st))
    elements.append(Spacer(1, 0.4*cm))

    # ── CLIENTE ───────────────────────────────────────────────────
    elements.append(Paragraph('▌ DATOS DEL CLIENTE', ParagraphStyle(
        's', fontSize=8, fontName='Helvetica-Bold', textColor=PRIMARY,
        borderPad=4, leading=10, spaceAfter=3,
        backColor=HexColor('#fff7ed'), borderColor=ACCENT, borderWidth=0,
        leftIndent=6, borderLeftWidth=3, borderLeftColor=ACCENT,
    )))
    cliente_rows = [
        [_fila('Nombre', c.nombre_completo)[0], _fila('Nombre', c.nombre_completo)[1],
         _fila('Documento', c.cedula)[0],        _fila('Documento', c.cedula)[1]],
        [_fila('Teléfono', c.telefono)[0], _fila('Teléfono', c.telefono)[1],
         _fila('Ciudad', c.ciudad or '—')[0],    _fila('Ciudad', c.ciudad or '—')[1]],
    ]
    if c.ruc:
        cliente_rows.append([
            _fila('RUC', c.ruc)[0], _fila('RUC', c.ruc)[1],
            _fila('Email', c.email or '—')[0], _fila('Email', c.email or '—')[1],
        ])
    elements.append(_tabla_datos(cliente_rows, [C2*0.28, C2*0.72, C2*0.28, C2*0.72]))
    elements.append(Spacer(1, 0.35*cm))

    # ── VEHÍCULO ──────────────────────────────────────────────────
    elements.append(Paragraph('▌ DATOS DEL VEHÍCULO', ParagraphStyle(
        's', fontSize=8, fontName='Helvetica-Bold', textColor=PRIMARY,
        backColor=HexColor('#fff7ed'), leading=10, spaceAfter=3,
        leftIndent=6, borderLeftWidth=3, borderLeftColor=ACCENT,
    )))
    vehiculo_rows = [
        [_fila('Marca', v.marca)[0],   _fila('Marca', v.marca)[1],
         _fila('Modelo', v.modelo)[0], _fila('Modelo', v.modelo)[1],
         _fila('Año', v.año)[0],       _fila('Año', v.año)[1]],
        [_fila('Chapa', v.placa)[0],   _fila('Chapa', v.placa)[1],
         _fila('Color', v.color)[0],   _fila('Color', v.color)[1],
         _fila('Chassis', v.chassis or '—')[0], _fila('Chassis', v.chassis or '—')[1]],
        [_fila('Km Entrada', f"{v.km_entrada:,}".replace(',','.'))[0],
         _fila('Km Entrada', f"{v.km_entrada:,}".replace(',','.'))[1],
         Paragraph('', st['campo_label']), Paragraph('', st['campo_valor']),
         Paragraph('', st['campo_label']), Paragraph('', st['campo_valor'])],
    ]
    elements.append(_tabla_datos(vehiculo_rows, [C3*0.28, C3*0.72, C3*0.28, C3*0.72, C3*0.28, C3*0.72]))
    elements.append(Spacer(1, 0.35*cm))

    # ── ACCESORIOS ────────────────────────────────────────────────
    elements.append(Paragraph('▌ ACCESORIOS AL INGRESO', ParagraphStyle(
        's', fontSize=8, fontName='Helvetica-Bold', textColor=PRIMARY,
        backColor=HexColor('#fff7ed'), leading=10, spaceAfter=3,
        leftIndent=6, borderLeftWidth=3, borderLeftColor=ACCENT,
    )))
    acc_items = []
    for campo, label in ACCESORIOS:
        presente = getattr(v, campo, False)
        marca = '✓' if presente else '✗'
        color_marca = HexColor('#16a34a') if presente else HexColor('#dc2626')
        acc_items.append((marca, color_marca, label))

    # Distribuir en 4 columnas
    cols_acc = 4
    acc_rows = []
    for i in range(0, len(acc_items), cols_acc):
        row = []
        for j in range(cols_acc):
            if i + j < len(acc_items):
                marca, col, label = acc_items[i + j]
                celda = Paragraph(
                    f'<font color="{col.hexval()}" size="11"><b>{marca}</b></font>'
                    f'<font size="8"> {label}</font>',
                    ParagraphStyle('acc', leading=12, fontSize=8)
                )
            else:
                celda = Paragraph('', ParagraphStyle('acc', fontSize=8))
            row.append(celda)
        acc_rows.append(row)

    t_acc = Table(acc_rows, colWidths=[W/cols_acc]*cols_acc)
    t_acc.setStyle(TableStyle([
        ('BACKGROUND',    (0,0), (-1,-1), LIGHT),
        ('TOPPADDING',    (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING',   (0,0), (-1,-1), 12),
        ('LINEBELOW',     (0,0), (-1,-1), 0.3, BORDER),
    ]))
    elements.append(t_acc)
    elements.append(Spacer(1, 0.35*cm))

    # ── SOLICITUD ─────────────────────────────────────────────────
    elements.append(Paragraph('▌ SOLICITUD DEL CLIENTE', ParagraphStyle(
        's', fontSize=8, fontName='Helvetica-Bold', textColor=PRIMARY,
        backColor=HexColor('#fff7ed'), leading=10, spaceAfter=3,
        leftIndent=6, borderLeftWidth=3, borderLeftColor=ACCENT,
    )))
    t_sol = Table(
        [[Paragraph(ficha.solicitud or '—', st['solicitud'])]],
        colWidths=[W],
    )
    t_sol.setStyle(TableStyle([
        ('BACKGROUND',    (0,0), (-1,-1), LIGHT),
        ('TOPPADDING',    (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING',   (0,0), (-1,-1), 10),
        ('RIGHTPADDING',  (0,0), (-1,-1), 10),
        ('LINEBELOW',     (0,0), (-1,-1), 0.3, BORDER),
        ('MINROWHEIGHT',  (0,0), (-1,-1), 1.5*cm),
    ]))
    elements.append(t_sol)
    elements.append(Spacer(1, 0.35*cm))

    # ── INFO ADICIONAL ────────────────────────────────────────────
    fecha_est = ficha.fecha_estimada.strftime('%d/%m/%Y') if ficha.fecha_estimada else '—'
    info_rows = [[
        _fila('Fecha de Ingreso', ficha.fecha_ingreso.strftime('%d/%m/%Y %H:%M'))[0],
        _fila('Fecha de Ingreso', ficha.fecha_ingreso.strftime('%d/%m/%Y %H:%M'))[1],
        _fila('Fecha Est. Entrega', fecha_est)[0],
        _fila('Fecha Est. Entrega', fecha_est)[1],
        _fila('Estado', ficha.get_estado_display())[0],
        _fila('Estado', ficha.get_estado_display())[1],
    ]]
    elements.append(_tabla_datos(info_rows, [C3*0.38, C3*0.62, C3*0.38, C3*0.62, C3*0.38, C3*0.62]))
    elements.append(Spacer(1, 0.6*cm))

    # ── FIRMAS ────────────────────────────────────────────────────
    firmas_block = KeepTogether([
        HRFlowable(width=W, thickness=0.5, color=BORDER),
        Spacer(1, 0.3*cm),
        Paragraph(
            'Autorizo la realización del trabajo y las pruebas viales luego del mantenimiento/reparación.',
            st['autorizacion'],
        ),
        Spacer(1, 1.5*cm),
        Table(
            [[
                Paragraph('_______________________________', st['firma_label']),
                Paragraph('', st['firma_label']),
                Paragraph('_______________________________', st['firma_label']),
            ],[
                Paragraph('CLIENTE', st['firma_label']),
                Paragraph('', st['firma_label']),
                Paragraph('RECEPTOR', st['firma_label']),
            ]],
            colWidths=[W*0.4, W*0.2, W*0.4],
        ),
        Spacer(1, 0.2*cm),
    ])
    elements.append(firmas_block)

    doc.build(elements)
    buffer.seek(0)
    return buffer
