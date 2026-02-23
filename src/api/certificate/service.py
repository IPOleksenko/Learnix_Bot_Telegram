from io import BytesIO

from api.certificate.generator import fill_pdf_form, get_pdf_bytes, set_fields_read_only

from config.config import templates_path

def generate_certificate(name: str, course: str, date: str) -> BytesIO:

    path = templates_path + r'\pdf\certificate_template.pdf'

    writer = fill_pdf_form(
        path,
        {
            "Name": name,
            "Course": course,
            "Date": date
        }
    )

    set_fields_read_only(writer)

    return get_pdf_bytes(writer)