import streamlit
from fpdf import FPDF
from pdf_annotate import PdfAnnotator, Appearance, Location
from PyPDF2 import PdfReader
from PIL import ImageFont
import streamlit as st


def data_submitted(qa_data: list,  uploaded_files, savePath):
    """
    :param qa_data:
    :return:
    """
    print(f"will submit {qa_data}")
    st.write("data submitted")
    pdf_output_path = write_to_pdf(qa_data, uploaded_files, savePath)
    streamlit.balloons()
    st.write(f"data written at {pdf_output_path}")
    return pdf_output_path


def get_pil_text_size(text, font_size, font_name):
    font = ImageFont.truetype(font_name, font_size)
    size = font.getsize(text)
    return size


def base_form() -> list:
    """
    update a pre-filled dictionary with user text answers
    :param list:
    :return:
    """
    blocks = [
        {"text": "ABC-1234", "x": 40, "y": 90, "field": "medicare_number"},
        {"text": "X", "x": 335, "y": 115, "field": "signed_up_medicare"},
        {"text": "John Doe", "x": 40, "y": 150, "field": "full_name"},
        {"text": "johndoe@gmail.com", "x": 40, "y": 180, "field": "mailing_address"},
        {"text": "Mountain View", "x": 40, "y": 220, "field": "city"},
        {"text": "C", "x": 410, "y": 220, "field": "state_first_char"},
        {"text": "A", "x": 425, "y": 220, "field": "state_second_char"},
        {"text": "9", "x": 465, "y": 220, "field": "zip_first_char"},
        {"text": "4", "x": 480, "y": 220, "field": "zip_second_char"},
        {"text": "0", "x": 495, "y": 220, "field": "zip_third_char"},
        {"text": "4", "x": 510, "y": 220, "field": "zip_fourth_char"},
        {"text": "3", "x": 525, "y": 220, "field": "zip_fifth_char"},
        {"text": "1", "x": 50, "y": 255, "field": "phone_first_char"},
        {"text": "2", "x": 65, "y": 255, "field": "phone_second_char"},
        {"text": "3", "x": 80, "y": 255, "field": "phone_third_char"},
        {"text": "4", "x": 115, "y": 255, "field": "phone_fourth_char"},
        {"text": "5", "x": 130, "y": 255, "field": "phone_fifth_char"},
        {"text": "6", "x": 145, "y": 255, "field": "phone_sixth_char"},
        {"text": "7", "x": 175, "y": 255, "field": "phone_seventh_char"},
        {"text": "8", "x": 195, "y": 255, "field": "phone_eighth_char"},
        {"text": "9", "x": 210, "y": 255, "field": "phone_ninth_char"},
        {"text": "0", "x": 225, "y": 255, "field": "phone_tenth_char"},
    ]
    return blocks


def split_zipcode(zipcode: str) -> list:
    """
    process zipcode
    :param zipcode:
    :return:
    """
    zipcode_vals = [*zipcode]
    return [{"field": "zip_first_char", "data": zipcode_vals[0]},
            {"field": "zip_second_char", "data": zipcode_vals[1]},
            {"field": "zip_third_char", "data": zipcode_vals[2]},
            {"field": "zip_fourth_char", "data": zipcode_vals[3]},
            {"field": "zip_fifth_char", "data": zipcode_vals[4]}]


def split_state(state: str) -> list:
    """
    process state: split into 2 characters
    :param state:
    :return:
    """
    state_vals = [*state]
    return [{"field": "state_first_char", "data": state_vals[0]},
            {"field": "state_second_char", "data": state_vals[1]}]


def split_phone_number(phonenumber: str) -> list:
    """
    process phonenumber: split into 2 characters
    :param phonenumber:
    :return:
    """
    phonenumber_vals = [*phonenumber]
    return [{"field": "phone_first_char", "data": phonenumber_vals[0]},
            {"field": "phone_second_char", "data": phonenumber_vals[1]},
            {"field": "phone_third_char", "data": phonenumber_vals[2]},
            {"field": "phone_fourth_char", "data": phonenumber_vals[3]},
            {"field": "phone_fifth_char", "data": phonenumber_vals[4]},
            {"field": "phone_sixth_char", "data": phonenumber_vals[5]},
            {"field": "phone_seventh_char", "data": phonenumber_vals[6]},
            {"field": "phone_eighth_char", "data": phonenumber_vals[7]},
            {"field": "phone_ninth_char", "data": phonenumber_vals[8]},
            {"field": "phone_tenth_char", "data": phonenumber_vals[9]}]


def write_to_pdf(blocks: list, uploaded_file, savePath) -> str:
    """
    write template form with user data
    :param blocks:
    :return: location of file
    """
    print(f"input from user:{blocks}")
    # pdf_reader = PdfReader("/Users/jonathanbouchet/Downloads/CMS-40B.pdf")

    pdf_reader = PdfReader(uploaded_file)

    dim_page_0 = pdf_reader.pages[1].mediabox
    offset = [37, 10]
    FONT_SIZE = 10
    FONT = "Arial.ttf"

    # annotator = PdfAnnotator('/Users/jonathanbouchet/Downloads/CMS-40B.pdf')
    annotator = PdfAnnotator(savePath)
    base_template = base_form()
    prefilled = [x['field'] for x in base_template]
    print(f"prefilled fields: {prefilled}")

    for block in blocks:
        print(f"writing block: {block}")
        if block['field'] == 'state':
            state_vals = split_state(block['data'])
            for block_state in state_vals:
                prefilled_block = [d for d in base_template if d['field'] == block_state['field']][0]
                print(f"prefilled block: {prefilled_block}")
                x = int(prefilled_block['x'])
                y = int(prefilled_block['y']) + offset[1]
                text_size = get_pil_text_size(block_state['data'], FONT_SIZE, FONT)
                annotator.add_annotation(
                    'text',
                    Location(
                        x1=x,
                        y1=int(dim_page_0[3] - y),
                        x2=int(x + text_size[0]),
                        y2=int(dim_page_0[3] - y + text_size[1]), page=1),
                    Appearance(content=block_state['data'], font_size=FONT_SIZE, fill=(0, 0, 0)),
                )
        elif block['field'] == 'zipcode':
            zipcode_vals = split_zipcode(block['data'])
            for block_zip in zipcode_vals:
                prefilled_block = [d for d in base_template if d['field'] == block_zip['field']][0]
                print(f"prefilled block: {prefilled_block}")
                x = int(prefilled_block['x'])
                y = int(prefilled_block['y']) + offset[1]
                text_size = get_pil_text_size(block_zip['data'], FONT_SIZE, FONT)
                annotator.add_annotation(
                    'text',
                    Location(
                        x1=x,
                        y1=int(dim_page_0[3] - y),
                        x2=int(x + text_size[0]),
                        y2=int(dim_page_0[3] - y + text_size[1]), page=1),
                    Appearance(content=block_zip['data'], font_size=FONT_SIZE, fill=(0, 0, 0)),
                )
        elif block['field'] == 'phone_number':
            phonenumber_vals = split_phone_number(block['data'])
            for block_phone in phonenumber_vals:
                prefilled_block = [d for d in base_template if d['field'] == block_phone['field']][0]
                print(f"prefilled block: {prefilled_block}")
                x = int(prefilled_block['x'])
                y = int(prefilled_block['y']) + offset[1]
                text_size = get_pil_text_size(block_phone['data'], FONT_SIZE, FONT)
                annotator.add_annotation(
                    'text',
                    Location(
                        x1=x,
                        y1=int(dim_page_0[3] - y),
                        x2=int(x + text_size[0]),
                        y2=int(dim_page_0[3] - y + text_size[1]), page=1),
                    Appearance(content=block_phone['data'], font_size=FONT_SIZE, fill=(0, 0, 0)),
                )
        elif block['field'] in prefilled:
            prefilled_block = [d for d in base_template if d['field'] == block['field']][0]
            print(f"prefilled block: {prefilled_block}")
            x = int(prefilled_block['x'])
            y = int(prefilled_block['y']) + offset[1]
            if block['field'] == "signed_up_medicare":
                if block['data'].lower() in ["yes", "y"]:
                    text_size = get_pil_text_size("X", FONT_SIZE, FONT)
                    content = "X"
                else:
                   text_size = get_pil_text_size("", FONT_SIZE, FONT)
                   content = ""
            else:
                text_size = get_pil_text_size(block['data'], FONT_SIZE, FONT)
                content = block['data']
            annotator.add_annotation(
               'text',
                Location(
                    x1=x,
                    y1=int(dim_page_0[3] - y),
                    x2=int(x + text_size[0]),
                    y2=int(dim_page_0[3] - y + text_size[1]), page=1),
                Appearance(content=content, font_size=FONT_SIZE,  fill=(0, 0, 0)),
                )
        else:
            pass
    output_dir = savePath.split('/')[0]
    output_name = savePath.split('/')[1]
    output_path = f"{output_dir}/filled_{output_name}"
    annotator.write(output_path)
    return output_path
    #
    # annotator.write('/Users/jonathanbouchet/Documents/LLM_PROJECT/LLM_TEST/OPENAI/STREAMLIT_SUMMARY_APP/experiments/test_CMS-40B.pdf')
    # return '/Users/jonathanbouchet/Documents/LLM_PROJECT/LLM_TEST/OPENAI/STREAMLIT_SUMMARY_APP/experiments/test_CMS-40B.pdf'