

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from pymongo import MongoClient
from bson import ObjectId
import json

# Connect to MongoDB Atlas
client = MongoClient("mongodb+srv://gayathribint:gayathri123@gayathri.tqrnqj7.mongodb.net/")
db = client["tododb"]
collection = db["todos"]

@csrf_exempt
def todos(request):
    if request.method == "GET":
        # Fetch all todos
        data = list(collection.find({}, {"_id": 1, "title": 1, "category": 1, "priority": 1, "due_date": 1, "completed": 1}))
        for item in data:
            item["_id"] = str(item["_id"])  # Convert ObjectId to string for frontend
        return JsonResponse(data, safe=False)

    elif request.method == "POST":
        # Add new todo
        try:
            data = json.loads(request.body)
            collection.insert_one(data)
            return JsonResponse({"message": "Task added"}, status=201)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

@csrf_exempt
def todo_detail(request, id):
    try:
        object_id = ObjectId(id)
    except:
        return JsonResponse({"error": "Invalid ID"}, status=400)

    if request.method == "PUT":
        # Edit/update todo
        try:
            data = json.loads(request.body)
            data.pop("_id", None)  # Don't allow _id to be updated
            collection.update_one({"_id": object_id}, {"$set": data})
            return JsonResponse({"message": "Task updated"}, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    elif request.method == "DELETE":
        # Delete todo
        collection.delete_one({"_id": object_id})
        return JsonResponse({"message": "Task deleted"}, status=200)
