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
from demo import level
from pmz.pmz import FaceDetection, ObjectDetection, SceneClassification

# load models
model_face = FaceDetection()
model_obj = ObjectDetection(cfg_path="pmz/pmz/object/yolov3/config/yolov3.cfg",
                            weights_path="pmz/pmz/object/yolov3/weights/yolov3.weights",
                            class_path="pmz/pmz/object/yolov3/data/coco.names")
model_scene = SceneClassification(model_path="pmz/pmz/scene/data/resnet50_places365.pth.tar",
                                  json_path="pmz/pmz/scene/data/model_class.json")
model_scene.loadFullModel()


@method_decorator(csrf_exempt, name='dispatch')
class ApiImage(View):
    def get(self, request, id):
        image = get_object_or_404(models.Image, id=id)
        return JsonResponse(image.json())

    def post(self, request, id=None):
        if id is None:
            image = models.Image.objects.create(file=request.FILES['image'], scanned=True)
            scenes = model_scene.inference(image_input=image.file.path)
            faces = model_face.inference(img_path=image.file.path)
            objects = model_obj.inference(img_path=image.file.path)
            level.guess(scenes, faces, objects)
            for i in scenes:
                image.scene_set.create(
                    name=i['name'],
                    score=i['score'],
                )
            for i in faces:
                x1, y1, x2, y2 = i['box_points']
                image.rect_set.create(
                    type='face',
                    left=x1,
                    top=y1,
                    right=x2,
                    bottom=y2,
                    level=i['level'],
                    description='',
                )
            for i in objects:
                x1, y1, x2, y2 = i['box_points']
                image.rect_set.create(
                    type=i['name'],
                    left=x1,
                    top=y1,
                    right=x2,
                    bottom=y2,
                    level=i['level'],
                    description='',
                )
            return JsonResponse(image.json())
        else:
            image = get_object_or_404(models.Image, id=id)
            data = json.load(request)
            for rect in image.rect_set.all():
                rect.level_corrected = data[str(rect.id)]
                rect.save()
            level.update(image.json())
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
