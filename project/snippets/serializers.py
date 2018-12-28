from django.forms import widgets
from rest_framework import serializers
from .models import Snippet, LANGUAGE_CHOICES, STYLE_CHOICES


class SnippetSerializer(serializers.Serializer):
    pk = serializers.IntegerField(read_only=True)
    title = serializers.CharField(required=False, allow_blank=True, max_length=100)
    code = serializers.CharField(style={'base_template': 'textarea.html'})
    linenos = serializers.BooleanField(required=False)
    language = serializers.ChoiceField(choices=LANGUAGE_CHOICES, default='python')
    style = serializers.ChoiceField(choices=STYLE_CHOICES, default='friendly')

    def create(self, validated_data):
        """
        :param validated_data: 유효성 검증된 데이터
        :return: Snippet.objects.create(**validated_data)

        매개변수로 넘겨받은 검사완료된(validated) 데이터를 이용해서 모델 매니저를 통해
        새 snippets 인스턴스 (db_row)를 생성하여 리턴
        """
        return Snippet.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        :param instance: 모델의 객체
        :param validate_data: 검증된 데이터
        :return: instance
        특정 모델객체(row)과 검증된 데이터를 매개변수로 받아서
        특정 모델객체 안의 데이터를 검증된 데이터로 교체(update)시킨다.
        """
        instance.title = validated_data.get('title', instance.title)
        instance.code = validated_data.get('code', instance.code)
        instance.linenos = validated_data.get('linenos', instance.linenos)
        instance.language = validated_data.get('language', instance.language)
        instance.style = validated_data.get('style', instance.style)
        instance.save()
        return instance


# Model에 정의되어있는 필드정보를 가져와서 좀 더 손쉽게 시리얼라이징 할 수 있도록 만들어진 클래스.
# 맵핑할 model을 Meta InnerClass에 정의하고 사용할 필드를 지정하면 알아서 시리얼라이저가 생성됨.
class SnippetModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Snippet
        fields = ('id', 'title', 'code', 'linenos', 'language', 'style')