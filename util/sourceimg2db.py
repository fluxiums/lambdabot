import os
import django
import re

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lamdabotweb.settings")
django.setup()

from lamdabotweb.settings import SOURCEIMG_DIR, ALLOWED_EXTENSIONS
from memeviewer.models import MemeSourceImageOverride, MemeContext

imgdir = os.path.join(SOURCEIMG_DIR, "manual")
context = input("Context? (empty for any)\n")
if context == "":
    context = None
else:
    context = MemeContext.objects.get(short_name=context)

for file in os.listdir(imgdir):
    if re.match(ALLOWED_EXTENSIONS, file, re.IGNORECASE):
        print(file)
        img = MemeSourceImageOverride.submit(os.path.join(imgdir, file))
        img.friendly_name = file
        if context is not None:
            img.contexts.add(context)
        img.save()
