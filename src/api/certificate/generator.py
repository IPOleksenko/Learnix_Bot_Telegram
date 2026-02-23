from io import BytesIO

from pypdf import PdfReader, PdfWriter
from pypdf.generic import NameObject, NumberObject


def set_fields_read_only(writer):

    if "/AcroForm" in writer._root_object:

        acroform = writer._root_object["/AcroForm"]

        if "/Fields" in acroform:

            for field in acroform["/Fields"]:

                field_obj = field.get_object()

                field_obj.update(
                    {
                        NameObject("/Ff"): NumberObject(1)
                    }
                )


def fill_pdf_form(input_pdf, data):

    reader = PdfReader(input_pdf)
    writer = PdfWriter()

    writer.clone_reader_document_root(reader)

    writer.set_need_appearances_writer()

    writer.update_page_form_field_values(
        writer.pages[0],
        data
    )

    return writer


def get_pdf_bytes(writer) -> BytesIO:

    pdf_buffer = BytesIO()

    writer.write(pdf_buffer)

    pdf_buffer.seek(0)

    return pdf_buffer


