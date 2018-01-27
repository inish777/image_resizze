import requests
from io import BytesIO

from django.shortcuts import render, reverse
from django.core.files.images import ImageFile
from django.http import Http404, HttpResponseRedirect
from django.template.backends.utils import csrf_token_lazy

from basic_actions.models import Image
from basic_actions.utils import check_size_for_image, check_content_type_by_response


def main_page(request):
    context = dict()
    context['images'] = Image.objects.all()
    return render(request, 'index.html', context=context)


def upload(request):
    context = dict()
    if request.method == 'GET':
        context['csrf_token'] = csrf_token_lazy(request)
    if request.method == 'POST':
        if request.FILES.get('upload_image', None):
            Image.objects.create(image_field=request.FILES.get('upload_image'))
            return HttpResponseRedirect(reverse('main_page'))
        if request.POST.get('image_url', None):
            image_url = request.POST.get('image_url')
            try:
                response = requests.get(image_url)
                if response.status_code == 200 and check_content_type_by_response(response.headers):
                    buf_file = BytesIO()
                    buf_file.write(response.content)
                    filename = image_url.split('/')[-1]
                    image_ex = Image()
                    image_ex.image_field.save(filename, ImageFile(buf_file))
                    image_ex.save()
                    return HttpResponseRedirect(reverse('main_page'))
                else:
                    context['warning'] = 'this URL does not contain a image'
            except requests.ConnectionError:
                context['warning'] = 'Connection refused, use other url'
    return render(request, 'upload_page.html', context=context)


def image_page(request, image_hash):
    context = dict()
    try:
        image = Image.objects.get(key=image_hash)
    except Image.DoesNotExist:
        raise Http404('Image does not exist')
    width = request.GET.get('width')
    height = request.GET.get('height')
    size = request.GET.get('size', '1024x768')
    if width and height:
        if check_size_for_image(width, height, size):
            context['right_size'] = '%sx%s,C' % (width, height)
        else:
            context['warning'] = 'cannot change the size, max size: %s' % size
    context['image'] = image
    return render(request, 'image_page.html', context=context)
