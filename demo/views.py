import json

from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from demo import models

from .pmz.pmz import FaceDetection
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import os 


model_face = FaceDetection()

type2level = {
    "face": 3
}


class Upload(View):
    def get(self, request):
        return render(request, 'upload.html')

    def post(self, request):
        img_file = request.FILES['image']
        # save to var/upload/imgs
        path = default_storage.save(f'imgs/{img_file.name}', ContentFile(img_file.read()))
        # set img_path
        models.Image.img_path = os.path.join('var/upload/imgs', img_file.name)

        image = models.Image.objects.create(file=img_file)
        return redirect('image', id=image.id)


class Image(View):
    def get(self, request, id):
        image = get_object_or_404(models.Image, id=id)
        if not image.scanned:
            return render(request, 'scan.html', {'image': image})
        if not image.corrected:
            return render(request, 'correct.html', {'image': image})
        return render(request, 'download.html', {'image': image})


class Scan(View):
    def post(self, request, id):
        image = get_object_or_404(models.Image, id=id)
        res_face = model_face.inference(img_path=image.img_path)
        for r in res_face:
            x1, y1, x2, y2 = r['box_points']
            image.rect_set.create(
                type='Face',
                left=x1,
                top=y1,
                right=x2,
                bottom=y2,
                level=type2level[r['name']],
                description="这里有人脸"
            )
        
        # image.rect_set.create(
        #     type='A',
        #     description='图片的左上角容易泄露隐私',
        #     top=0,
        #     left=0,
        #     right=100,
        #     bottom=100,
        #     level=1,
        # )
        # image.rect_set.create(
        #     type='B',
        #     description='这里更容易泄露隐私',
        #     top=100,
        #     left=100,
        #     right=200,
        #     bottom=200,
        #     level=3,
        # )
        image.scanned = True
        image.save()
        return redirect('image', id=image.id)


class Correct(View):
    def post(self, request, id):
        image = get_object_or_404(models.Image, id=id)
        for rect in image.rect_set.all():
            rect.level_corrected = int(request.POST[f'{rect.id}/level'])
            rect.save()
        image.corrected = True
        image.save()
        return redirect('image', id=image.id)


@method_decorator(csrf_exempt, name='dispatch')
class ApiImage(View):
    def get(self, request, id):
        image = get_object_or_404(models.Image, id=id)
        return JsonResponse(image.json())

    def post(self, request, id=None):
        if id is None:
            image = models.Image.objects.create(file=request.FILES['image'])
            return JsonResponse(image.json())
        else:
            image = get_object_or_404(models.Image, id=id)
            data = json.load(request)
            for rect in image.rect_set.all():
                rect.level_corrected = data[str(rect.id)]
                rect.save()
            image.corrected = True
            image.save()
            return JsonResponse(image.json())


@method_decorator(csrf_exempt, name='dispatch')
class ApiRects(View):
    def post(self, request, id):
        image = get_object_or_404(models.Image, id=id)
        data = json.load(request)
        if not image.scanned:
            for rect in data['rects']:
                image.rect_set.create(
                    type=rect['type'],
                    description=rect['description'],
                    top=rect['top'],
                    left=rect['left'],
                    right=rect['right'],
                    bottom=rect['bottom'],
                    level=rect['level'],
                )
            image.scanned = True
            image.save()
        return JsonResponse(image.json())
