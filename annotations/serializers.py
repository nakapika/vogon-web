from rest_framework import serializers
from annotations.models import VogonUser
from models import *
from concepts.models import Concept, Type


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = VogonUser
        fields = ('username', 'email', 'id', 'affiliation', 'location',
                  'full_name', 'link')


class RemoteCollectionSerializer(serializers.Serializer):
    source = serializers.IntegerField()
    id_or_uri = serializers.CharField(max_length=255)
    name = serializers.CharField(max_length=255)


class RemoteResourceSerializer(serializers.Serializer):
    source = serializers.IntegerField()
    id_or_uri = serializers.CharField(max_length=255)
    title = serializers.CharField(max_length=255)


class RepositorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Repository


class RelationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Relation


class AppellationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appellation
        fields = ('asPredicate', 'created', 'createdBy', 'endPos', 'id',
                  'interpretation', 'interpretation_type', 'occursIn',
                  'startPos', 'stringRep', 'tokenIds', 'interpretation_label',
                  'interpretation_type_label')


class ConceptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Concept
        fields = ('id', 'url', 'uri', 'label', 'authority', 'typed',
                  'description', 'pos', 'resolved', 'typed_label')


class TypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Type
        fields = ('id', 'url', 'uri', 'label', 'authority', 'typed',
                  'description')


class RelationSetSerializer(serializers.ModelSerializer):
    appellations = AppellationSerializer(many=True)
    concepts = ConceptSerializer(many=True)
    class Meta:
        model = RelationSet
        fields = ('id', 'label', 'created', 'template', 'createdBy', 'occursIn', 'appellations', 'concepts')


class TemporalBoundsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TemporalBounds


class TextSerializer(serializers.ModelSerializer):
    class Meta:
        model = Text
        fields = ('id', 'uri', 'title', 'created', 'added',
                  'addedBy', 'source', 'annotators', 'annotation_count')

    def create(self, validated_data):
        repository = Repository.objects.get(pk=validated_data['source'])
        # TODO: Make retrieval/tokenization/other processing asynchronous.
        tokenizedContent = tokenize(retrieve(repository, validated_data['uri']))

        text = Text(uri=validated_data['uri'],
                    title=validated_data['title'],
                    source=repository,
                    addedBy=self.context['request'].user,
                    tokenizedContent=tokenizedContent)
        text.save()
        return HttpResponse(text.id)


class TextCollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TextCollection
