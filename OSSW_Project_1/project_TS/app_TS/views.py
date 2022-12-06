from django.shortcuts import render
from googletrans import Translator


def home(request):
    if request.method == 'POST':
        result_post = request.POST
        result_translation = translate(result_post)

        return render(request, 'index.html', result_translation)

    return render(request, 'index.html')


def translate(input_data):
    input_text = input_data.get('input_text')
    mid_language = input_data.get('language')
    language_list = {'EN': 'en', 'JP': 'ja', 'CH': 'zh-cn'}

    translator = Translator()
    text_mid = translator.translate(
        input_text, dest=language_list[mid_language])
    text_last = translator.translate(text_mid.text, dest=text_mid.src)

    return {
        'text_first': {'text': input_text},
        'text_mid': {'text': text_mid.text},
        'text_last': {'text': text_last.text}
    }
