from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from images.forms import ImageCreateForm
from images.models import Image


@login_required
def image_create(request: HttpRequest):
    if request.method == 'POST':
        form = ImageCreateForm(data=request.POST)
        if form.is_valid():
            new_image = form.save(commit=False)
            new_image.user = request.user
            new_image.save()
            messages.success(request, "Image added successfully")
            return redirect(new_image.get_absolute_url())
    else:
        form = ImageCreateForm(data=request.GET)

    return render(request, 'images/image/create.html', {'section': 'images', 'form': form})


def image_detail(request: HttpRequest, id: int, slug: str):
    image = get_object_or_404(Image, id=id, slug=slug)
    return render(request, 'images/image/detail.html', {'secion': 'images', 'image': image})


@login_required
@require_POST
def image_like(request: HttpRequest):
    image_id = request.POST.get('id')
    action = request.POST.get('action')

    if image_id and action:
        try:
            image = Image.objects.get(id=image_id)
            if action == 'like':
                image.users_like.add(request.user)
            else:
                image.users_like.remove(request.user)
            return JsonResponse({'status': 'ok'})
        except Image.DoesNotExist:
            pass

    return JsonResponse({'status': 'error'})


@login_required
def image_list(request: HttpRequest):
    images = Image.objects.all()
    paginator = Paginator(images, 8)
    page = request.GET.get('page')
    images_only = request.GET.get('images_only')

    try:
        images = paginator.page(page if page else 1)
    except PageNotAnInteger:
        images = paginator.page(1)
    except EmptyPage:
        if images_only:
            return HttpResponse('')
        images = paginator.page(paginator.num_pages)
    
    if images_only:
        return render(request, 'images/image/list_images.html', {'section': 'images', 'images': images})
    
    return render(request, 'images/image/list.html', {'section': 'images', 'images': images})
