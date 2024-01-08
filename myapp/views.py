from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.core import serializers
from .models import Item
from .forms import ItemForm
import json
from django.http import HttpResponse

def default_view(request):
    return HttpResponse("Welcome to myapp!")

@csrf_exempt
def item_list(request):
    if request.method == 'GET':
        items = Item.objects.all()
        data = serializers.serialize("json", items)
        return JsonResponse(data, safe=False)

@csrf_exempt
def item_detail(request, pk):
    item = get_object_or_404(Item, pk=pk)
    data = serializers.serialize("json", [item])
    return JsonResponse(data, safe=False)

@csrf_exempt
def item_new(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON in request body"}, status=400)

        form = ItemForm(data)
        if form.is_valid():
            item = form.save()
            return JsonResponse(serializers.serialize("json", [item]), safe=False, status=201)

    return JsonResponse({"error": "Invalid request"}, status=400)

@csrf_exempt
def item_edit(request, pk):
    item = get_object_or_404(Item, pk=pk)

    if request.method == 'PUT':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON in request body"}, status=400)

        form = ItemForm(data, instance=item)
        if form.is_valid():
            item = form.save()
            return JsonResponse(serializers.serialize("json", [item]), safe=False)

    return JsonResponse({"error": "Invalid request"}, status=400)

@csrf_exempt
def item_delete(request, pk):
    item = get_object_or_404(Item, pk=pk)

    if request.method == 'DELETE':
        item.delete()
        return JsonResponse({"message": "Item deleted successfully"})

    return JsonResponse({"error": "Invalid request"}, status=400)
