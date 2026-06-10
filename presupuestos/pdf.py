from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, KeepTogether
)
from reportlab.lib.colors import HexColor

PRIMARY    = HexColor('#1a1a2e')
ACCENT     = HexColor('#f59e0b')
LIGHT      = HexColor('#f8fafc')
BORDER     = HexColor('#e2e8f0')
TEXT_MUTED = HexColor('#64748b')
WHITE      = colors.white
SUCCESS    = HexColor('#16a34a')


def _gs(n):
    """Formatea entero como Guaraní: 1500000 → Gs. 1.500.000"""
    try:
        return f'Gs. {int(round(float(n))):,}'.replace(',', '.')
    except Exception:
        return 'Gs. 0'


def _st():
    return {
        'empresa': ParagraphStyle('emp', fontSize=18, fontName='Helvetica-Bold',
                                  textColor=WHITE, leading=22),
        'sub_emp': ParagraphStyle('sub', fontSize=9, fontName='Helvetica',
                                  textColor=HexColor('#fbbf24'), leading=12),
        'num_label': ParagraphStyle('nl', fontSize=8, fontName='Helvetica',
                                    textColor=TEXT_MUTED, alignment=TA_RIGHT, leading=10),
        'num_val':   ParagraphStyle('nv', fontSize=22, fontName='Helvetica-Bold',
                                    textColor=ACCENT, alignment=TA_RIGHT, leading=26),
        'sec':       ParagraphStyle('sec', fontSize=8, fontName='Helvetica-Bold',
                                    textColor=PRIMARY, leading=10, spaceAfter=3,
                                    leftIndent=6, borderLeftWidth=3, borderLeftColor=ACCENT,
                                    backColor=HexColor('#fff7ed')),
        'lbl':       ParagraphStyle('lbl', fontSize=7.5, fontName='Helvetica',
                                    textColor=TEXT_MUTED, leading=10),
        'val':       ParagraphStyle('val', fontSize=9, fontName='Helvetica-Bold',
                                    textColor=PRIMARY, leading=12),
        'body':      ParagraphStyle('body', fontSize=9, fontName='Helvetica',
                                    textColor=PRIMARY, leading=13),
        'th':        ParagraphStyle('th', fontSize=8, fontName='Helvetica-Bold',
                                    textColor=WHITE, leading=10),
        'td_left':   ParagraphStyle('tdl', fontSize=9, fontName='Helvetica',
                                    textColor=PRIMARY, leading=12),
        'td_right':  ParagraphStyle('tdr', fontSize=9, fontName='Helvetica-Bold',
                                    textColor=PRIMARY, leading=12, alignment=TA_RIGHT),
        'total_lbl': ParagraphStyle('tl', fontSize=11, fontName='Helvetica-Bold',
                                    textColor=PRIMARY, alignment=TA_RIGHT, leading=14),
        'total_val': ParagraphStyle('tv', fontSize=14, fontName='Helvetica-Bold',
                                    textColor=SUCCESS, alignment=TA_RIGHT, leading=18),
        'firma_lbl': ParagraphStyle('fl', fontSize=9, fontName='Helvetica-Bold',
                                    textColor=PRIMARY, alignment=TA_CENTER, leading=12),
        'nota':      ParagraphStyle('nota', fontSize=8, fontName='Helvetica-Oblique',
                                    textColor=TEXT_MUTED, alignment=TA_CENTER, leading=11),
    }


def generar_pdf_presupuesto(presupuesto):
    buffer = BytesIO()
    st = _st()
    W = 18.5 * cm

    doc = SimpleDocTemplate(buffer, pagesize=A4,
                            leftMargin=1.5*cm, rightMargin=1.5*cm,
                            topMargin=1.5*cm, bottomMargin=1.5*cm)

    p  = presupuesto
    v  = p.ficha.vehiculo
    c  = v.cliente
    items = list(p.items.all())

    elems = []

    # ── CABECERA ──────────────────────────────────────────────────
    header = Table([[
        [Paragraph('TecnoCar', st['empresa']),
         Paragraph('Taller Automotriz', st['sub_emp'])],
        [Paragraph('PRESUPUESTO', st['num_label']),
         Paragraph(f'P-{p.pk:04d}', st['num_val']),
         Paragraph(p.fecha.strftime('%d/%m/%Y'), st['num_label'])],
    ]], colWidths=[10*cm, 8.5*cm])
    header.setStyle(TableStyle([
        ('BACKGROUND',   (0,0), (-1,-1), PRIMARY),
        ('VALIGN',       (0,0), (-1,-1), 'MIDDLE'),
        ('LEFTPADDING',  (0,0), (0,0),  18),
        ('RIGHTPADDING', (1,0), (1,0),  18),
        ('TOPPADDING',   (0,0), (-1,-1), 14),
        ('BOTTOMPADDING',(0,0), (-1,-1), 14),
    ]))
    elems.append(header)
    elems.append(Spacer(1, 0.4*cm))

    # ── CLIENTE ───────────────────────────────────────────────────
    elems.append(Paragraph('▌ DATOS DEL CLIENTE', st['sec']))
    cli_t = Table([
        [Paragraph('Nombre', st['lbl']),
         Paragraph(c.nombre_completo, st['val']),
         Paragraph('Documento', st['lbl']),
         Paragraph(c.cedula, st['val'])],
        [Paragraph('Teléfono', st['lbl']),
         Paragraph(c.telefono or '—', st['val']),
         Paragraph('Ciudad', st['lbl']),
         Paragraph(c.ciudad or '—', st['val'])],
    ], colWidths=[2.5*cm, 6.5*cm, 2.5*cm, 6.5*cm])
    cli_t.setStyle(TableStyle([
        ('BACKGROUND',    (0,0),(-1,-1), LIGHT),
        ('TOPPADDING',    (0,0),(-1,-1), 5),
        ('BOTTOMPADDING', (0,0),(-1,-1), 5),
        ('LEFTPADDING',   (0,0),(-1,-1), 8),
        ('LINEBELOW',     (0,0),(-1,-1), 0.3, BORDER),
    ]))
    elems.append(cli_t)
    elems.append(Spacer(1, 0.3*cm))

    # ── VEHÍCULO / HR ─────────────────────────────────────────────
    elems.append(Paragraph('▌ VEHÍCULO — HOJA DE RECEPCIÓN', st['sec']))
    veh_t = Table([
        [Paragraph('Marca', st['lbl']),    Paragraph(v.marca, st['val']),
         Paragraph('Modelo', st['lbl']),   Paragraph(v.modelo, st['val']),
         Paragraph('Año', st['lbl']),      Paragraph(str(v.año), st['val'])],
        [Paragraph('Chapa', st['lbl']),    Paragraph(v.placa, st['val']),
         Paragraph('Color', st['lbl']),    Paragraph(v.color, st['val']),
         Paragraph('HR', st['lbl']),       Paragraph(f'HR-{p.ficha.pk:04d}', st['val'])],
    ], colWidths=[2*cm, 4.5*cm, 2*cm, 4.5*cm, 1.5*cm, 4*cm])
    veh_t.setStyle(TableStyle([
        ('BACKGROUND',    (0,0),(-1,-1), LIGHT),
        ('TOPPADDING',    (0,0),(-1,-1), 5),
        ('BOTTOMPADDING', (0,0),(-1,-1), 5),
        ('LEFTPADDING',   (0,0),(-1,-1), 8),
        ('LINEBELOW',     (0,0),(-1,-1), 0.3, BORDER),
    ]))
    elems.append(veh_t)
    elems.append(Spacer(1, 0.35*cm))

    # ── ITEMS ─────────────────────────────────────────────────────
    elems.append(Paragraph('▌ DETALLE DE TRABAJOS', st['sec']))

    # encabezado de tabla
    item_rows = [[
        Paragraph('Cant.', st['th']),
        Paragraph('Descripción del Trabajo', st['th']),
        Paragraph('P. Unitario', st['th']),
        Paragraph('Subtotal', st['th']),
    ]]
    for item in items:
        item_rows.append([
            Paragraph(str(item.cantidad), ParagraphStyle('n', fontSize=9, textColor=TEXT_MUTED,
                                             fontName='Helvetica-Bold', leading=12,
                                             alignment=TA_CENTER)),
            Paragraph(item.descripcion, st['td_left']),
            Paragraph(_gs(item.precio), ParagraphStyle('tdr2', fontSize=9, fontName='Helvetica',
                                             textColor=TEXT_MUTED, leading=12, alignment=TA_RIGHT)),
            Paragraph(_gs(item.total), st['td_right']),
        ])

    # fila vacía si no hay items
    if not items:
        item_rows.append([
            Paragraph('', st['td_left']),
            Paragraph('Sin items registrados.', ParagraphStyle(
                'empty', fontSize=9, fontName='Helvetica-Oblique',
                textColor=TEXT_MUTED, leading=12)),
            Paragraph('', st['td_right']),
            Paragraph('', st['td_right']),
        ])

    items_t = Table(item_rows, colWidths=[1.5*cm, 10*cm, 3.5*cm, 3.5*cm])
    row_styles = [
        ('BACKGROUND',    (0,0),  (-1,0),   PRIMARY),
        ('TEXTCOLOR',     (0,0),  (-1,0),   WHITE),
        ('TOPPADDING',    (0,0),  (-1,-1),  6),
        ('BOTTOMPADDING', (0,0),  (-1,-1),  6),
        ('LEFTPADDING',   (0,0),  (-1,-1),  8),
        ('RIGHTPADDING',  (0,0),  (-1,-1),  8),
        ('LINEBELOW',     (0,1),  (-1,-1),  0.3, BORDER),
        ('VALIGN',        (0,0),  (-1,-1),  'MIDDLE'),
    ]
    # alternar fondo
    for idx in range(1, len(item_rows)):
        if idx % 2 == 0:
            row_styles.append(('BACKGROUND', (0,idx), (-1,idx), LIGHT))
    items_t.setStyle(TableStyle(row_styles))
    elems.append(items_t)

    # ── TOTAL ─────────────────────────────────────────────────────
    total_val = p.total
    total_t = Table([[
        Paragraph('TOTAL', st['total_lbl']),
        Paragraph(_gs(total_val), st['total_val']),
    ]], colWidths=[13.5*cm, 5*cm])
    total_t.setStyle(TableStyle([
        ('TOPPADDING',    (0,0),(-1,-1), 10),
        ('BOTTOMPADDING', (0,0),(-1,-1), 10),
        ('RIGHTPADDING',  (0,0),(-1,-1), 8),
        ('LINEABOVE',     (0,0),(-1,-1), 1.5, ACCENT),
        ('BACKGROUND',    (0,0),(-1,-1), HexColor('#fefce8')),
    ]))
    elems.append(total_t)
    elems.append(Spacer(1, 0.4*cm))

    # ── OBSERVACIONES ─────────────────────────────────────────────
    if p.observaciones:
        elems.append(Paragraph('▌ OBSERVACIONES', st['sec']))
        obs_t = Table([[Paragraph(p.observaciones, st['body'])]],
                      colWidths=[W])
        obs_t.setStyle(TableStyle([
            ('BACKGROUND',    (0,0),(-1,-1), LIGHT),
            ('TOPPADDING',    (0,0),(-1,-1), 8),
            ('BOTTOMPADDING', (0,0),(-1,-1), 8),
            ('LEFTPADDING',   (0,0),(-1,-1), 10),
            ('LINEBELOW',     (0,0),(-1,-1), 0.3, BORDER),
        ]))
        elems.append(obs_t)
        elems.append(Spacer(1, 0.4*cm))

    # ── ESTADO ────────────────────────────────────────────────────
    estado_color = {
        'aprobado':  HexColor('#16a34a'),
        'rechazado': HexColor('#dc2626'),
        'facturado': HexColor('#2563eb'),
        'enviado':   HexColor('#0891b2'),
    }.get(p.estado, TEXT_MUTED)

    estado_t = Table([[
        Paragraph('Estado del presupuesto:', st['lbl']),
        Paragraph(p.get_estado_display(), ParagraphStyle(
            'est', fontSize=10, fontName='Helvetica-Bold',
            textColor=estado_color, leading=12)),
    ]], colWidths=[5*cm, 13.5*cm])
    estado_t.setStyle(TableStyle([
        ('VALIGN', (0,0),(-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0),(-1,-1), 4),
    ]))
    elems.append(estado_t)
    elems.append(Spacer(1, 0.6*cm))

    # ── FIRMAS ────────────────────────────────────────────────────
    elems.append(KeepTogether([
        HRFlowable(width=W, thickness=0.5, color=BORDER),
        Spacer(1, 0.3*cm),
        Paragraph(
            'Este presupuesto tiene validez de 30 días a partir de la fecha de emisión.',
            st['nota'],
        ),
        Spacer(1, 1.4*cm),
        Table([[
            Paragraph('_______________________________', st['firma_lbl']),
            Paragraph('', st['firma_lbl']),
            Paragraph('_______________________________', st['firma_lbl']),
        ],[
            Paragraph('CLIENTE', st['firma_lbl']),
            Paragraph('', st['firma_lbl']),
            Paragraph('TALLER / RECEPTOR', st['firma_lbl']),
        ]], colWidths=[W*0.4, W*0.2, W*0.4]),
    ]))

    doc.build(elems)
    buffer.seek(0)
    return buffer
