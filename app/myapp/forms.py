# forms.py
from django import forms
from .models import Pdf, VideoMetadata

class PdfUploadForm(forms.ModelForm):
    class Meta:
        model = Pdf
        fields = ['file']

class VideoUploadForm(forms.ModelForm):
    class Meta:
        model = VideoMetadata
        fields = ['file', 'title', 'thumbnail']
