from docx import Document
from docx.oxml.shared import OxmlElement
from docx.oxml.ns import qn
import re

def copiar_contenido(tabla):
    contenido = {}
    for fila in tabla.rows:
        etiqueta = fila.cells[0].text.strip()
        contenido[etiqueta] = fila.cells[1]
    return contenido

def reemplazar_etiquetas(documento, contenido):
    for parrafo in documento.paragraphs:
        for etiqueta, celda in contenido.items():
            if etiqueta in parrafo.text:
                if celda.text:
                    parrafo.text = parrafo.text.replace(etiqueta, celda.text)
                else:
                    for run in celda.paragraphs[0].runs:
                        if run.element.find('.//w:drawing') is not None:
                            nueva_run = parrafo.add_run()
                            nueva_run._element.append(run.element.find('.//w:drawing'))
                    parrafo.text = parrafo.text.replace(etiqueta, '')

def main():
    # Abrir el primer archivo
    doc1 = Document('test1.docx')
    tabla = doc1.tables[0]
    contenido = copiar_contenido(tabla)

    # Abrir el segundo archivo
    doc2 = Document('test2.docx')
    reemplazar_etiquetas(doc2, contenido)

    # Guardar el resultado
    doc2.save('generado.docx')

if __name__ == '__main__':
    main()
