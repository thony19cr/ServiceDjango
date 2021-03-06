# coding=utf-8
from django.shortcuts import render
from django.http import HttpResponse

# from reportlab.pdfgen.canvas import Canvas
# !/usr/bin/env python

from reportlab.pdfgen import canvas
from django.db.models import Q
#from reporte.reportes_models import *
from reportes_models import *

from reportlab.lib.pagesizes import A4, cm, inch
from reportlab.lib.units import mm
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.lib import utils
from reportlab.platypus.flowables import PageBreak, Spacer
from reportlab.platypus import BaseDocTemplate, Frame, PageTemplate, Image, Paragraph, Table, TableStyle
from io import BytesIO

from  reportlab.lib.styles import ParagraphStyle as PS
from django.http import HttpResponse
from django.views.generic import ListView
from reportlab.platypus import SimpleDocTemplate, Paragraph, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Table
import os
import os.path
from reportlab.graphics.barcode import code39
import barcode

width, height = A4

def get_image(path, width=1 * cm):
    img = utils.ImageReader(path)
    iw, ih = img.getSize()
    aspect = ih / float(iw)
    return Image(path, width=width, height=(width * aspect))


def coord(x, y, unit=1):
    x, y = x * unit, height - y * unit
    return x, y


def generar_pdf(request, ubigeo, aer, aer_fin):
    print "generar_pdf"
    MARGIN_SIZE = 17 * mm
    PAGE_SIZE = A4
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = "attachment; filename=" + ubigeo + "001" + ".pdf"
    # response['Content-Disposition'] = "attachment; filename="+ubigeo+"001"+".pdf"
    pdf_name = "clientes.pdf"
    styles = getSampleStyleSheet()
    stylesTitle = getSampleStyleSheet()
    stylesCabe = getSampleStyleSheet()

    styleTitle = stylesTitle["Normal"]
    styleTitle.alignment = TA_CENTER
    styleBH = styles["Normal"]
    styleBH.alignment = TA_LEFT
    styleCa = stylesCabe["Normal"]
    styleCa.alignment = TA_CENTER

    buff = BytesIO()
    # destino = "Lista/" + str(ubigeo)+"00100"+ str(aeut)+ ".pdf"
    #
    # doc2 = SimpleDocTemplate(destino, pagesize=A4,
    #                          rightMargin=70,
    #                          leftMargin=70,
    #                          topMargin=0.5 *cm,
    #                          bottomMargin=0.5 *cm, )
    doc = SimpleDocTemplate(buff,
                            pagesize=A4,
                            rightMargin=65,
                            leftMargin=65,
                            topMargin=0.5 *cm,
                            bottomMargin=0.5 *cm,
                            )

    h_sub_tile = PS(
        name='Heading1',
        fontSize=10,
        leading=14,
        alignment=TA_CENTER
    )

    h_sub_tile_2 = PS(
        name='Heading1',
        fontSize=11,
        leading=14,
        alignment=TA_CENTER
    )

    h_center = PS(
        name='Heading1',
        fontSize=7,
        leading=8,
        alignment=TA_CENTER
    )

    h1 = PS(
        name='Heading1',
        fontSize=7,
        leading=8
    )

    h11 = PS(
        name='Heading1',
        fontSize=7,
        leading=8,
        alignment=TA_CENTER
    )

    h2 = PS(
        name='Normal',
        fontSize=6,
        leading=16
    )

    h3 = PS(
        name='Normal',
        fontSize=7,
        leading=14,
        alignment=TA_CENTER)

    h4 = PS(
        name='Normal',
        fontSize=6,
        leading=16
    )

    h5 = PS(
        name='Normal',
        fontSize=8,
        leading=16,
        alignment=TA_CENTER
    )

    h_obser = PS(
        name='Normal',
        fontSize=8,
        leading=16
    )

    h_bar = PS(
        name='Normal',
        fontSize=7,
        leading=14,
        alignment=TA_CENTER
    )

    story = []

    distrito = Distrito.objects.get(ubigeo=ubigeo)  # ubigeo

    # vivi = ViviendaUrbana.objects.get(ubigeo=distrito.ubigeo, zona='00100', aeu_final=aeut)

    # cond_viv = Aeus.objects.filter(ubigeo=distrito.ubigeo, zona='00100', aeu_final=aeut)

    # total = Aeus.objects.filter(ubigeo=distrito.ubigeo, zona='00100', aeu_final=aeut).count()

    # viv_u = ViviendaU.objects.filter(ubigeo=ubigeo)

    rango_equivalencia = [[1, 'A'], [2, 'B'], [3, 'C'], [4, 'D'], [5, 'E'], [6, 'F'], [7, 'G'], [8, 'H'], [9, 'I'],
                          [10, 'J'], [11, 'K'], [12, 'L'], [13, 'M'], [14, 'N'], [15, 'O'], [16, 'P'], [17, 'Q'], [18, 'R'],
                          [19, 'S'], [20, 'T'], [21, 'U'], [22, 'V'], [23, 'W'], [24, 'X'], [25, 'Y'], [26, 'Z']
                          ]

    Z1 = Paragraph("<strong>OBSERVACIONES: .............................................................................."
                   "....................................................................................................."
                   "....................................................................................................."
                   "....................................................................................................."
                   "....................................................................................................."
                   "....................................................................................................."
                   "................................................................................</strong>", h_obser)

    table_obs = Table(
        data=[
            [Z1]
        ],
        colWidths=[18.8 * cm],
        rowHeights=[2 * cm],
        style=[
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]
    )

    Z2 = Paragraph("<strong>EMPADRONADOR</strong>", h5)

    Z3 = Paragraph("<strong>Todas las viviendas que estén dentro de los límites de tu A.E.U. deben ser empadronadas. Debes tener<br/>cuidado de no omitir ninguna vivienda</strong>",h5)

    table_empa_cuerp = Table(
        data=[
            [Z2],
            [Z3]
        ],
        colWidths=[18.8 * cm],
        rowHeights=[0.7 * cm, 1.5 * cm],
        style=[
            ('GRID', (0, 0), (0, 0), 1, colors.black),
            ('GRID', (0, 1), (0, 1), 1, colors.black),
            ('ALIGN', (0, 0), (0, 0), 'CENTER')
        ]
    )

    x = 0

    #caso = Seg_Esp_R_Aer.objects.filter(ubigeo=ubigeo, emp_aer=1, aer_ini_17= aer)                         #HABILITAR
    caso = Seg_Esp_R_Aer.objects.filter(ubigeo=ubigeo, aer_ini_17=aer)                                      #BORRAR

    for aeu_v in caso:
        idaer = aeu_v.idaer
        idscr = aeu_v.idscr

        print idaer
        print idscr

        cond = Vw_Seg_Esp_R_Aer.objects.filter(idaer=idaer)

        x = x + 1
        y = x
        lista_distritos = []
        lista_distritos.append(ubigeo)

        for ubigein in range(len(lista_distritos)):

            if os.path.exists("\\\srv-fileserver\\CPV2017\\list_seg_esp_rur\\" + str(lista_distritos[ubigein])) == False:
                os.mkdir("\\\srv-fileserver\\CPV2017\\list_seg_esp_rur\\" + str(lista_distritos[ubigein]))

        # for ubigein in range(tam_dis):
        #
        #     if os.path.exists("\\\srv-fileserver\\CPV2017\\list_segm_esp\\" + str(lista_distritos[ubigein])) == False:
        #         os.mkdir("\\\srv-fileserver\\CPV2017\\list_segm_esp\\" + str(lista_distritos[ubigein]))
        #
        #     total_zonas = int(str(Tab_Aeus.objects.filter(ubigeo=lista_distritos[ubigein]).values_list('zona',flat=True).distinct().count()))
        #
        #     for zona_t in range(total_zonas):
        #         zoner = str(zona_t + 1).zfill(3) + "00"
        #         listin.append(str(lista_distritos[ubigein]) + ": " + zoner + "<br/>")
        #         if os.path.exists("\\\srv-fileserver\\CPV2017\\list_segm_esp\\" + str(lista_distritos[ubigein]) + "\\" + zoner) == False:
        #             os.mkdir("\\\srv-fileserver\\CPV2017\\list_segm_esp\\" + str(lista_distritos[ubigein]) + "\\" + zoner)

        pdf = "{}-{}-{}-{}-{}.pdf".format(ubigeo, idscr[6:8], idscr[8:10], idaer[6:9], idaer[9:12])

        print pdf

        destino = "\\\srv-fileserver\\CPV2017\\list_seg_esp_rur\\" + str(ubigeo) + "\\" + str(pdf)


        print destino
        doc2 = SimpleDocTemplate(destino, pagesize=A4,
                                 rightMargin=70,
                                 leftMargin=70,
                                 topMargin=0.5 * cm,
                                 bottomMargin=0.5 * cm, )


        p = Paragraph(str(1) + " - " + str(1), h2)
        extra = Paragraph("-", h2)

        p_page = Table(
            data=[
                [extra, p]
            ],
            colWidths=[17 * cm, 2.3 * cm],
            style=[
                ('GRID', (0, 0), (-1, -1), 1, colors.white),
                ('ALIGN', (0, 0), (1, 0), 'RIGHT'),
            ]
        )
        #
        # string = str(ubigeo)+str(secc)+str(aeut)
        # st = code39.Extended39(string)
        #
        # bar_string = Paragraph(string, h_bar)

        pi = Paragraph("-", h2)
        # st_b = st

        # table_bar = Table(
        #     data = [
        #         [pi, st_b],
        #         ['', bar_string]
        #     ],
        #     colWidths= [13 * cm, 5 * cm],
        #     style=[
        #         ('ALIGN', (0, 0), (-1, -1),'CENTER')
        #     ]
        # )

        # story.append(table_bar)

        viviendas_totales = Vw_Seg_Esp_R_Aer.objects.filter(Q(idaer=idaer)).order_by('or_viv_aer')

        total_viv = 0

        secc = aeu_v.scr_ini
        aer = aeu_v.aer_ini_17

        print secc
        print aer
        for viviendon in viviendas_totales:
            total_viv = total_viv + 1

        data = [
            ['', '', '', '', Paragraph('<strong>Doc. CPV</strong>', h4),''],
            [Paragraph('<strong>A. UBICACION GEOGRAFICA</strong>', h11), '', '', '',Paragraph('<strong>B. UBICACION CENSAL</strong>', h11), ''],
            [Paragraph('<strong>DEPARTAMENTO</strong>', h1),Paragraph(str(distrito.ccdd.ccdd), h_center),Paragraph(str(distrito.ccdd.departamento), h1), '',Paragraph('<strong>SECCIÓN Nº</strong>', h1),Paragraph('Del '+secc+ ' Al '+secc, h1)],
            [Paragraph('<strong>PROVINCIA</strong>', h1), Paragraph(distrito.ccpp, h_center),Paragraph(str(distrito.cod_prov.provincia).decode('latin-1'), h1), '', Paragraph(str('<strong>A.E.R. Nº</strong>'), h1),Paragraph('Del '+ aer + ' Al '+aer_fin, h1)],
            [Paragraph('<strong>DISTRITO</strong>', h1), Paragraph(distrito.ccdi, h_center), Paragraph(distrito.distrito, h1),'', '',''],
            ['', '','', '',Paragraph('<strong>C. TOTAL DE VIVIENDAS DEL AER.</strong>', h1), Paragraph(str(total_viv), h1)],
        ]

        tables = Table(data, colWidths=[3.7 * cm, 1 * cm, 8.1 * cm, 0.3 * cm, 4.5 * cm, 2.2 * cm])
                       # ,
                       # rowHeights=[0.4 * cm, 0.4  * cm, 0.4  * cm, 0.4  * cm, 0.4  * cm, 0.4  * cm, 0.7  * cm])

        tables.setStyle(TableStyle([
            ('TEXTCOLOR', (0, 0), (5, 0), colors.black),
            #('ALIGN', (4, 0), (5, 0), 'RIGHT'),
            #('ALIGN', (1, 2), (1, 4), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),

            #('GRID', (0, 1), (2, 6), 1, colors.black),
            #('GRID', (4, 1), (5, 4), 1, colors.black),
            ('GRID', (0, 1), (2, 4), 1, colors.black),
            ('GRID', (4, 5), (5, 6), 1, colors.black),
            ('GRID', (4, 1), (5, 3), 1, colors.black),
            ('SPAN', (0, 1), (2, 1)),
            ('SPAN', (4, 1), (5, 1)),

            ('BACKGROUND', (0, 1), (2, 1), colors.Color(219.0 / 255, 229.0 / 255, 241.0 / 255)),
            ('BACKGROUND', (0, 2), (0, 4), colors.Color(219.0/255,229.0/255,241.0/255)),
            ('BACKGROUND', (4, 2), (4, 3), colors.Color(219.0 / 255, 229.0 / 255, 241.0 / 255)),
            ('BACKGROUND', (4, 5), (4, 5), colors.Color(219.0 / 255, 229.0 / 255, 241.0 / 255)),
            #('BACKGROUND', (4, 1), (5, 1), colors.Color(219.0/255,229.0/255,241.0/255)),
            ('BACKGROUND', (4, 1), (5, 1), colors.Color(219.0/255,229.0/255,241.0/255))
        ]))

        t1 = Paragraph("CENSOS NACIONALES 2017: XII DE POBLACIÓN, VII DE VIVIENDA<br/>Y III DE COMUNIDADES INDÍGENAS",h_sub_tile)
        t1_sub = Paragraph("<strong>LISTADO DE CENTROS POBLADOS Y VIVIENDAS DEL ÁREA DE EMPADRONAMIENTO RURAL</strong>", h_sub_tile_2)

        fichero_imagen_inei = 'Reporte/Img/inei.png'
        imagen_logo_inei = Image(os.path.realpath(fichero_imagen_inei), width=50, height=50)

        P2 = Paragraph('', styleBH)
        fichero_imagen = 'Reporte/Img/escudo.png'
        imagen_logo = Image(os.path.realpath(fichero_imagen), width=50, height=50)

        t1_croq = Paragraph("<strong>CROQUIS DEL ÁREA DE EMPADRONAMIENTO URBANO</strong>", h_sub_tile_2)
        t = Table(
            data=[
                # ['', t1, ''],
                [[imagen_logo, P2], t1, [imagen_logo_inei, P2]],
                ['', t1_croq, '']
            ],
            colWidths=[2 * cm, 14 * cm, 2 * cm],
            style=[
                ('GRID', (1, 1), (-2, -2), 1, colors.white),
                # ('SPAN', (0, 1), (2, 1)),
                # ('BOX', (0, 0), (1, -1), 2, colors.black),
                # ('LINEABOVE', (1, 2), (-2, 2), 1, colors.blue),
                # ('LINEBEFORE', (2, 1), (2, -2), 1, colors.pink),
                # ('BACKGROUND', (0, 0), (0, 1), colors.pink),
                # ('BACKGROUND', (1, 1), (1, 2), colors.lavender),
                # ('BACKGROUND', (2, 2), (2, 3), colors.orange),
                # ('BOX', (0, 0), (-1, -1), 2, colors.black),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.white),

            ]
        )

        obs_data = [
            [Paragraph(e, h3) for e in ["<strong>D. INFORMACIÓN DE CENTROS POBLADOS Y VIVIENDAS</strong>",
                                        "",
                                        "",
                                        "",
                                        "",
                                        "",
                                        "",
                                        "",
                                        "",
                                        ""]],
            [Paragraph(e, h3) for e in ["<strong>Viv Nº</strong>",
                                        "<strong>CENTRO POBLADO</strong>",
                                        "",
                                        "",
                                        "<strong>DIRECCIÓN DE LA VIVIENDA</strong>",
                                        "",
                                        "",
                                        "",
                                        "",
                                        "<strong>Nombres y Apellidos del JEFE DE HOGAR</strong>"]],
            [Paragraph(e, h3) for e in ["",
                                        "<strong>CÓD.</strong>",
                                        "<strong>Or. Reg.</strong>",
                                        "<strong>Nombre</strong>",
                                        "<strong>Tipo de Vía</strong>",
                                        "<strong>Nombre de Vía</strong>",
                                        "<strong>N° de Puerta</strong>",
                                        "<strong>Piso N°</strong>",
                                        "<strong>Km. N°</strong>",
                                        ""]],
            [Paragraph(e, h3) for e in ["<strong>(1)</strong>",
                                        "<strong>(2)</strong>",
                                        "<strong>(3)</strong>",
                                        "<strong>(4)</strong>",
                                        "<strong>(5)</strong>",
                                        "<strong>(6)</strong>",
                                        "<strong>(7)</strong>",
                                        "<strong>(8)</strong>",
                                        "<strong>(9)</strong>",
                                        "<strong>(10)</strong>"]],
         ]
        c = Table(obs_data,
                  colWidths=[0.9 * cm, 1.1 * cm, 1 * cm, 3.8 * cm, 1.8 * cm, 2.4 * cm, 1.1 * cm, 1 * cm, 0.9 * cm, 5.8 * cm])

        c.setStyle(TableStyle(
            [
                ('GRID', (1, 1), (-2, -2), 1, colors.black),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                #('VALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTSIZE', (0, 0), (-1, -1), 7),
                ('BACKGROUND', (0, 0), (-1, 0), colors.Color(219.0/255,229.0/255,241.0/255)),
                ('BACKGROUND', (0, 0), (-1, -1), colors.Color(219.0/255,229.0/255,241.0/255)),
                ('SPAN', (0, 0), (9, 0)),
                ('SPAN', (1, 1), (3, 1)),
                ('SPAN', (4, 1), (8, 1)),
                ('SPAN', (9, 1), (9, 2)),
                ('SPAN', (0, 1), (0, 2)),
                ('LINEBELOW', (0, 0), (-1, 0), 1, colors.black),
                ('BACKGROUND', (0, 0), (-1, 0), colors.Color(219.0/255,229.0/255,241.0/255)),
            ]
        ))

        i=0

        fichero_imagen_inei = 'Reporte/Img/inei.png'
        imagen_logo_inei = Image(os.path.realpath(fichero_imagen_inei), width=50, height=40)

        P2 = Paragraph('', styleBH)
        fichero_imagen = 'Reporte/Img/escudo.png'
        imagen_logo = Image(os.path.realpath(fichero_imagen), width=50, height=50)

        t = Table(
            data=[
                [[imagen_logo, P2], t1, [imagen_logo_inei, P2]],
                ['', t1_croq, '']
            ],
            colWidths=[2 * cm, 14 * cm, 2 * cm],
            style=[
                ('GRID', (1, 1), (-2, -2), 1, colors.white),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.white),
            ]
        )

        t_croq = Table(
            data=[
                [[imagen_logo, P2], t1, [imagen_logo_inei, P2]],
                ['',t1_sub, '']
            ],
            colWidths=[2 * cm, 14 * cm, 2 * cm],
            style=[
                ('GRID', (1, 1), (-2, -2), 1, colors.white),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.white),
            ]
        )

        # story.append(t)
        # story.append(Spacer(0, 1 * mm))
        # story.append(tables)
        # story.append(Spacer(0, 1 * mm))

        # story.append(Spacer(0, 1 * mm))
        # story.append(table_obs)
        # story.append(PageBreak())

        # story.append(table_bar)
        story.append(t_croq)
        story.append(Spacer(0, 2 * mm))
        story.append(tables)
        story.append(Spacer(0, 3 * mm))
        story.append(c)

        viviendas = Vw_Seg_Esp_R_Aer.objects.filter(Q(idaer=idaer)).order_by('or_viv_aer')[0:32]

        total_viviendas = int(Vw_Seg_Esp_R_Aer.objects.filter(Q(idaer=idaer)).order_by('or_viv_aer').count())

        for vivienda in viviendas:

            i=i+1
            # Bloque Listado
            table2 = [(
                    str(vivienda.or_viv_aer).decode('latin-1'),
                    str(vivienda.codccpp).decode('latin-1'),
                    vivienda.id_reg_or,
                    vivienda.nomccpp,
                    vivienda.p20_nombre,
                    vivienda.p21,
                    vivienda.p22_a,
                    vivienda.p26,
                    vivienda.p28,
                    vivienda.p32)
                      ]
            u = Table(table2,
                      colWidths=[0.9 * cm, 1.1 * cm, 1 * cm, 3.8 * cm, 1.8 * cm, 2.4 * cm, 1.1 * cm, 1 * cm, 0.9 * cm, 5.8 * cm],
                      rowHeights=[0.5 *cm])

            u.setStyle(TableStyle(
                [
                    ('GRID', (1, 1), (-2, -2), 1, colors.black),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                    ('FONTSIZE', (0, 0), (9, 0), 7),
                    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ]
            ))
            story.append(u)

        # viviendas_second = Vw_Seg_Esp_R_Aer.objects.filter(Q(idaer=idaer)).order_by('or_viv_aer')[32:]
        #

        if total_viviendas>33:
            #num_vuelt = total_viviendas/42
            #ini_val = 48
            #fin_val = 47

            #for i in range(num_vuelt):
            #ini = 32+ini_val
            #fin = 79+fin_val
            inicio = range(32,total_viviendas, 46)
            fin = range(80, total_viviendas, 46)
            nhojas = len(zip(inicio,fin))
            for i in range(nhojas):
                #inicio_val = range(32, total_viviendas, 48)
                #fin_val = range(79, total_viviendas, 48)
                story.append(c)
                viviendas_second = Vw_Seg_Esp_R_Aer.objects.filter(Q(idaer=idaer)).order_by('or_viv_aer')[inicio[i]:fin[i]]
                for vivienda in viviendas_second:
                    #i = i + 1
                    # Bloque Listado
                    table2 = [(
                            str(vivienda.or_viv_aer).decode('latin-1'),
                            str(vivienda.codccpp).decode('latin-1'),
                            vivienda.id_reg_or,
                            vivienda.nomccpp,
                            vivienda.p20_nombre,
                            vivienda.p21,
                            vivienda.p22_a,
                            vivienda.p26,
                            vivienda.p28,
                            vivienda.p32)
                              ]
                    u_second = Table(table2,
                              colWidths=[0.9 * cm, 1.1 * cm, 1 * cm, 3.8 * cm, 1.8 * cm, 2.4 * cm, 1.1 * cm, 1 * cm, 0.9 * cm, 5.8 * cm],
                              rowHeights=[0.5 * cm])
                    u_second.setStyle(TableStyle(
                        [
                            ('GRID', (1, 1), (-2, -2), 1, colors.black),
                            ('GRID', (0, 0), (-1, -1), 1, colors.black),
                            ('GRID', (0, 0), (-1, -1), 1, colors.black),
                            ('FONTSIZE', (0, 0), (9, 0), 7),
                            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                        ]
                    ))
                    story.append(u_second)
    #print story[4:]


    doc2.build(story)
    doc.build(story)
    response.write(buff.getvalue())
    buff.close()
    return response

def generar_lote(request):

    lista_distrito = []

    ubigeosa = os.listdir("\\\srv-fileserver\\CPV2017\\croquis_segm_esp\\rural")

    # lista_distrito.append('020601')

    lista =[]

    for ubigeos in ubigeosa:

        #total_pdf_ubigeo = int(str(Seg_Esp_R_Aer.objects.filter(ubigeo=ubigeos, emp_aer=1).count()))
        total_pdf_ubigeo = int(str(Seg_Esp_R_Aer.objects.filter(ubigeo=ubigeos).count()))

        for pos in range(total_pdf_ubigeo):
            #aer = Seg_Esp_R_Aer.objects.filter(ubigeo=ubigeos, emp_aer=1).values_list('aer_ini_17', flat='true')
            aer = Seg_Esp_R_Aer.objects.filter(ubigeo=ubigeos).values_list('aer_ini_17', 'aer_fin_17')

            #generar_pdf(request,lista_distrito[ubigeos],rur.aer_ini_17[zona_t])
            lista.append(str(pos)+": "+str(aer[pos][0])+str(aer[pos][1])  +"<br/>")

            generar_pdf(request, ubigeos, str(aer[pos][0]), str(aer[pos][1]))
    return HttpResponse(lista)

