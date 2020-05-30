import json

from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from demo import models


class Upload(View):
    def get(self, request):
        return render(request, 'upload.html')

    def post(self, request):
        image = models.Image.objects.create(file=request.FILES['image'])
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
        image.rect_set.create(
            type='A',
            description='图片的左上角容易泄露隐私',
            top=0,
            left=0,
            right=100,
            bottom=100,
            level=1,
        )
        image.rect_set.create(
            type='B',
            description='这里更容易泄露隐私',
            top=100,
            left=100,
            right=200,
            bottom=200,
            level=3,
        )
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
