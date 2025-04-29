from .models import Document
from django import forms
from django.core.exceptions import ValidationError

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ('file',)
    def clean_file(self):
        file = self.cleaned_data.get('file')
        if not file:
            raise ValidationError("Пожалуйста, загрузите файл.")
        
        valid_extensions = ['.txt', '.pdf']
        if not any(file.name.lower().endswith(ext) for ext in valid_extensions):
            raise ValidationError("Разрешены только файлы с расширением .txt и .pdf.")

        
        valid_mime_types = ['text/plain', 'application/pdf']
        if file.content_type not in valid_mime_types:
            raise ValidationError("Вы загрузили файл неверного типа.")

        
        max_size = 5 * 1024 * 1024
        if file.size > max_size:
            raise ValidationError("Максимальный размер файла — 5 MB.")

        return file