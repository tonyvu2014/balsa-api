import json
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from feeds.models import NewsFeed
from feeds.serializers import NewsFeedSerializer
from feeds.service import read_all_news_feeds

# Create your views here.
@api_view(['POST'])
def get_news_feeds(request):
    data = json.loads(request.body.decode(encoding='UTF-8'))
    terms = data.get('terms', [])
    limit = data.get('limit', None)
    feeds = list(read_all_news_feeds(terms))
    feeds.sort(key=lambda x: x.published_date, reverse=True)
    results = feeds[:limit] if limit else feeds
    serializer = NewsFeedSerializer(results, many=True)
    return Response(serializer.data)
