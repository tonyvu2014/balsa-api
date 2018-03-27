from rest_framework import serializers
from feeds.models import NewsFeed


class NewsFeedSerializer(serializers.Serializer):
    title = serializers.CharField()
    link = serializers.CharField()
    description = serializers.CharField()
    published_date = serializers.DateTimeField()


    def restore_object(self, attrs, instance=None):
        if instance is not None:
            instance.title = attrs.get('title', instance.title)
            instance.link = attrs.get('link', instance.link)
            instance.description = attrs.get('description',  instance.description)
            instance.published_date = attrs.get('published_date', instance.published_date)

        return NewsFeed(**attrs)    