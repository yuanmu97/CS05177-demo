import json

from django.core.files.base import ContentFile
from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

import PIL.Image
import PIL.ImageDraw

from demo import models
from pmz.pmz import FaceDetection

model_face = FaceDetection()

type2level = {
    'face': 3,
}


@method_decorator(csrf_exempt, name='dispatch')
class ApiImage(View):
    def get(self, request, id):
        image = get_object_or_404(models.Image, id=id)
        return JsonResponse(image.json())

    def post(self, request, id=None):
        if id is None:
            image = models.Image.objects.create(file=request.FILES['image'], scanned=True)
            res_face = model_face.inference(img_path=image.file.path)
            for r in res_face:
                x1, y1, x2, y2 = r['box_points']
                image.rect_set.create(
                    type='face',
                    left=x1,
                    top=y1,
                    right=x2,
                    bottom=y2,
                    level=type2level[r['name']],
                    description='这里有人脸',
                )
            return JsonResponse(image.json())
        else:
            image = get_object_or_404(models.Image, id=id)
            data = json.load(request)
            for rect in image.rect_set.all():
                rect.level_corrected = data[str(rect.id)]
                rect.save()
            image.corrected.save(image.file.name, ContentFile(''))
            with PIL.Image.open(image.file.path) as im:
                draw = PIL.ImageDraw.Draw(im)
                for rect in image.rect_set.all():
                    if rect.level_corrected:
                        draw.rectangle(
                            (rect.left, rect.top, rect.right+1, rect.bottom+1),
                            fill=(128, 128, 128),
                        )
                im.save(image.corrected.path)
            return JsonResponse(image.json())
