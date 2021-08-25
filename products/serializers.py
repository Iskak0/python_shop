from rest_framework import serializers

from products.models import Product, ProductReview


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'title', 'price')


class ProductDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'title', 'description', 'price', 'image')


class CreateProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

        def validate_price(self, price):
            if price <0:
                raise serializers.ValidationError('Цена не может быть отрицательным')
            return price

        # def validate

class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = ProductReview
        fields = ('id', 'author',  'product', 'text',  'rating', 'created_at')

    def validate_product(self, product):
        request = self.context.get('request')
        user = request.user
        if self.Meta.model.objects.filter(product=product, author=user).exists():
            raise  serializers.ValidationError('Вы уже оставляли отзыв на дан')
        return product

        # queryset.count() - количество элементов
        # SELECT COUNT(*) FROM reviews;
        # queryset.exists() - есть ли хоть один результат
        # len(queryset)
        # len(SELECT * FROM reviews;)




    def validate_rating(self, rating):
        if rating not in range(1, 6):
            raise serializers.ValidationError('Рейтинг может быть от 1 до 5')
        return rating

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['author'] = request.user
        return super().create(validated_data)
