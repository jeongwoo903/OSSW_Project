from django.shortcuts import render
from googletrans import Translator


def home(request):
    if request.method == 'POST':
        result_post = request.POST.get('input_text')
        result_translation = translate(result_post)

        print("[debug] POST 결과 (입력):", result_post)
        print("[debug] 번역 결과:", result_translation)

        if result_post == "테스트":
            return render(request, 'result_ex.html', result_translation)

        return render(request, 'index.html', result_translation)

    return render(request, 'index.html')


def translate(input_text):
    translator = Translator()
    text_mid = translator.translate(input_text, dest='en')
    text_last = translator.translate(text_mid.text, dest='ko')

    return {
        'text_first': {'lang': text_mid.src, 'text': text_mid.origin},
        'text_mid': {'lang': text_mid.dest, 'text': text_mid.text},
        'text_last': {'lang': text_last.dest, 'text': text_last.text}
    }
