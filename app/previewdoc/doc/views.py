from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from .models import Document
from .forms import DocumentForm
from .utils import term_frequency, inverse_document_frequency
# Create your views here.
import json
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from .forms import DocumentForm
from .models import Document
from .utils import term_frequency, inverse_document_frequency

def read_utf(file):
    """Читаем файл в UTF-8."""
    # Проверяем, что файл в кодировке UTF-8
    # Если файл не в кодировке UTF-8, то возвращаем ошибку
    try:
        file.open()
        text = file.read().decode('utf-8')
        file.close()
        return text
    except Exception:
        return None

def get_recent_texts(limit=100):
    """Возвращает тексты последних N документов."""
    documents = Document.objects.order_by('-uploaded_at')[:limit]# только последние 100
    texts = []
    for doc in documents:
        content = read_utf(doc.file)
        if content:
            texts.append(content)
    return texts

def upload_file(request):
    """Обрабатывает загрузку файла и вычисляет TF-IDF."""
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save()
            file = document.file

            # Проверяем, что файл в кодировке UTF-8
            uploaded_text = read_utf(file)
            # Если файл не в кодировке UTF-8, то возвращаем ошибку
            if not uploaded_text:
                form.add_error('file', 'Файл должен быть в кодировке UTF-8.')
                return render(request, 'doc/file.html', {'form': form})
            
            # Получаем TF по загруженному тексту
            tf_scores = term_frequency(uploaded_text)
            # Получаем тексты всех документов
            all_texts = get_recent_texts(limit=100)
            # IDF по всем документам
            idf_scores = inverse_document_frequency(all_texts)


            result = []
            # Сохраняем результаты в формате JSON
            for word, count in tf_scores.items():
                idf = idf_scores.get(word, 0.0)
                result.append({
                    'word': word,
                    'tf': round(count, 5),
                    'idf': round(idf, 5)
                })

            # Сортировка по убыванию idf
            result.sort(key=lambda x: x['idf'], reverse=True)

            # Сохраняем результаты в сессии
            request.session['analysis_result'] = json.dumps(result)
            return redirect('file_page', page=1)
            
    # Если метод не POST, то создаем пустую форму    
    else:
        form = DocumentForm()
    return render(request, 'doc/file.html', {'form': form})


def upload_file_paginated(request, page):
    """Отображает результаты анализа с пагинацией."""
    # Получаем результаты анализа из сессии
    result_json = request.session.get('analysis_result')
    if not result_json:
        return redirect('file')
    # Десериализуем JSON-строку в Python-объект
    result = json.loads(result_json)
    paginator = Paginator(result, 50)
    page_obj = paginator.get_page(page)

    # Отображаем результаты на странице с пагинацией
    return render(request, 'doc/preview.html', {
        'page_obj': page_obj,
    })