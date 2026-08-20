import os

from django import template
from django.contrib.staticfiles import finders
from django.templatetags.static import static

register = template.Library()


@register.simple_tag
def static_v(path):
    """
    Igual que {% static %}, pero le agrega ?v=<mtime del archivo> al final.

    Sin esto, los navegadores (y a veces Cloudflare/el operador de datos
    móviles) cachean JS/CSS con el mismo nombre de archivo entre deploys,
    así que un fix ya subido no se ve hasta que el usuario borra caché a
    mano. Al cambiar el archivo, cambia su mtime, cambia el ?v=, y el
    navegador lo trata como una URL nueva — cache-bust automático, sin
    tener que acordarse de subir un número de versión a mano.
    """

    url = static(path)

    found = finders.find(path)

    if found:
        try:
            version = int(os.path.getmtime(found))
            return f"{url}?v={version}"
        except OSError:
            pass

    return url
