import json
import os

from django import template
from django.apps import apps
from django.templatetags.static import static
from django.utils.safestring import mark_safe

from walter import settings

register = template.Library()


@register.simple_tag()
def hmr_client():
    return mark_safe('<script type="module" src="http://localhost:5173/static/@vite/client"></script>')

@register.simple_tag()
def entrypoint_assets():
    if settings.DEBUG:
        return _get_static_entrypoint()

    assets = []
    for asset in _get_entrypoint_from_manifest():
        assets.append(asset)
        pass
    return mark_safe("\n".join(assets))

def _get_static_entrypoint():
    return mark_safe('<script type="module" src="http://localhost:5173/static/src/main.ts"></script>')

def _get_entrypoint_from_manifest():
    app_path = apps.get_app_config('frontend').path
    manifest_path = os.path.join(app_path, 'static', '.vite', 'manifest.json')
    result = []
    with open(manifest_path) as f:
        manifest = json.load(f)
        manifest_entrypoint = manifest['src/main.ts']
        entrypoint_path = static(manifest_entrypoint['file'])
        result.append(f"<script type=\"module\" src=\"{entrypoint_path}\"></script>")
        for css in manifest_entrypoint['css']:
            result.append(f"<link rel=\"stylesheet\" crossorigin href=\"{static(css)}\">")

    return result