from rest_framework import serializers
from packApp2.models import Pack_promocion


class PackPromocionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pack_promocion
        fields = '__all__'
