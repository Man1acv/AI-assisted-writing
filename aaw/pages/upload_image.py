import streamlit as st
from .base import BasePage
from ..callbacks import submit_essay, go_inputtype
from ..utils import image_to_text
from ..globals import STRINGS

__uploadpage__ = BasePage(name='upload_image')


def upload_image():
    __uploadpage__.sidebar()

    title_empty = st.empty()
    upload_file_empty = st.empty()
    upload_teacher_empty = st.empty()
    md_empty = st.empty()
    textarea_empty = st.empty()
    # teacher_empty = st.empty()
    btn_empty = st.empty()
    btn_back = st.empty()
    widgets = [
        title_empty,
        upload_file_empty,
        md_empty,
        textarea_empty,
        btn_empty,
        btn_back
    ]
    __uploadpage__.extend(li=widgets)

    title_empty.markdown("# {}".format(STRINGS["UPLOAD_IMAGE_HEADER"]))

    essay_picture = upload_file_empty.file_uploader("**{}**".format(STRINGS["UPLOAD_IMAGE_ESSAY"]),
                                                    type=['png', 'jpg', 'jpeg', 'pdf'])  # 'webp',
    # teacher_picture = upload_teacher_empty.file_uploader("**{}**".format(STRINGS["UPLOAD_IMAGE_TEACHER"]),
    #                                                     type=['png', 'jpg', 'jpeg', 'pdf'])  # 'webp',

    essay_text = None
    # teacher_text = None

    btn_back.button(label=STRINGS["BUTTON_BACK"], on_click=go_inputtype)

    @st.cache(show_spinner=False)
    def __ocr_cache__(image_input):
        with st.spinner(STRINGS["UPLOAD_IMAGE_WAITING"]):
            text_output = image_to_text(image_input)
        return text_output

    if essay_picture is not None:
        text = __ocr_cache__(essay_picture)
        md_empty.markdown('### {}:'.format(STRINGS["UPLOAD_IMAGE_CORRECT_MISTAKES"]))
        essay_text = textarea_empty.text_area('**{}**'.format(STRINGS["UPLOAD_IMAGE_ESSAY"]),
                                              value=text, height=500)

    # if teacher_picture is not None:
    #     filename = teacher_picture.name
    #     print(f'''uploaded: {filename}''')
    #     image = Image.open(teacher_picture)
    #     if not (filename.endswith('.jpg') or filename.endswith('.jpeg')):
    #         random_str = get_random_string(5)
    #         filename = random_str + '123.jpg'
    #         image = image.convert('RGB')
    #         image.save(filename)
    #         image = Image.open(filename)
    #
    #     text = __ocr_cache__(image)
    #     teacher_text = teacher_empty.text_area('**{}**'.format(STRINGS["UPLOAD_IMAGE_TEACHER"]),
    #     value=text, height=200)

    if essay_picture is not None:
        btn_empty.button(STRINGS["UPLOAD_IMAGE_BUTTON"], on_click=submit_essay, kwargs=dict(
            essay=essay_text,
            # teacher=teacher_text
        ))
