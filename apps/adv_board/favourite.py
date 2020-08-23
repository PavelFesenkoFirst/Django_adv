from apps.adv_board.models import Advertisement


class Favourite:

    def __init__(self, request):
        self.session = request.session
        favourite = self.session.get('favourite', {})
        self.fav = favourite

    def add(self, favorite):
        """ Добавление объявления """
        favorite_id = str(favorite.id)
        if favorite_id not in self.fav:
            self.fav[favorite_id] = {
                'price': str(favorite.price)
            }
        self.save()

    def save(self):
        """ Сохранение данных в сессию """
        self.session['favourite'] = self.fav
        self.session.modified = True  # Указываем, что сессия изменена

    def remove(self, favorite):
        favorite_id = str(favorite.id)
        if favorite_id in self.fav:
            del self.fav[favorite_id]
            self.save()

    def __iter__(self):
        favorite_ids = self.fav.keys()
        favourites = Advertisement.objects.filter(id__in=favorite_ids)
        for favo in favourites:
            self.fav[str(favo.id)]['favo'] = favo

        for item in self.fav.values():
            item['price'] = round(
                float(item['price'])
            )
            yield item

    def clear(self):
        del self.session['favourite']
        self.session.modified = True
