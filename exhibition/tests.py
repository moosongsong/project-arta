from django.test import TestCase
from .models import Exhibition, ExhibitionClick
from django.contrib.auth.models import User
from django.db.models import Count
# Create your tests here.

print(User.objects.count())
print(Exhibition.objects.count())
users = 2
#print(Exhibition.objects.values('id'))
# exhibition_list = Exhibition.objects.values('id')
# exhibition_id_list = exhibition_list.
exhibition_list = list(Exhibition.objects.all())
exhibition_id_list = list()
for element in exhibition_list:
    exhibition_id_list.append(element.id)
print(exhibition_id_list)

ex = list(exhibition_list)
exhibition = 66
print("check")

for c_user in range(0, users):
    for c_exhibition in ex:
        num = ExhibitionClick.objects.filter(user=c_user, exhibition=c_exhibition).count()
        if num > 0:
            print(c_user , c_exhibition, num)
