from django.contrib import admin
from .models import PaginaHome, PaginaPerfil, PaginaInscricao, PaginaResumoHoras, Evento


admin.site.register(PaginaHome)
admin.site.register(PaginaPerfil)
admin.site.register(PaginaInscricao)
admin.site.register(PaginaResumoHoras)
admin.site.register(Evento)
