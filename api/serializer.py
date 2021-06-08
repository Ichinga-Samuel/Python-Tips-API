from rest_framework import serializers
from tips.models import Tips, Tags, Links
import re


link = re.compile(r"\bhttp(?:s)?:\S*\b")
tag = re.compile(r"#\b.+?\b")


def jaccard_similarity(v1, v2, index=70):
    """
    :param v1: The first text
    :param v2: The second text
    :param index: Benchmark to check for similarity
    :return: Bool
    """
    a = {*v1.split()}
    b = {*v2.split()}
    c = a.intersection(b)
    d = (len(c)/(len(a)+len(b)-len(c))) * 100
    return d <= index


class TipsSerializer(serializers.ModelSerializer):

    def validate_tip(self, value):
        """
        Use jaccard similarity to compare tip with other tips in the database.
        since existing tips has more than 140 chars. character limitation can be carried out here
        :param value: tip
        :return: value or serializers.ValidationError
        """
        if len(value) > 140: raise serializers.ValidationError('Tip Can not be More Than 140 Characters')
        res = all(jaccard_similarity(value, tip['tip']) for tip in Tips.objects.all().values('tip'))
        if not res:
            raise serializers.ValidationError('This Tip is Similar to an Existing Tip')
        return value

    def create(self, validated_data):
        tip = validated_data['tip']
        tags = re.findall(tag, tip)
        tags = [t.strip('#').title() for t in tags]
        tags = [Tags.objects.update_or_create(name=t, defaults={"name": t})[0] for t in tags]
        links = re.findall(link, tip)
        tip_md = Tips(**validated_data)
        links_md = [Links.objects.update_or_create(name=l, defaults={'name': l, 'tip': tip_md}) for l in links]
        tip_md.save()
        tip_md.tags.add(*tags)
        return tip_md

    class Meta:
        model = Tips
        fields = ['timestamp', 'tip', 'account', 'email', 'links_set', 'tags', 'retweets', 'likes']
        read_only_fields = ['retweets', 'likes']
        depth = 1


class TagsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tags
        fields = ['name', 'tips_set']
        depth = 1