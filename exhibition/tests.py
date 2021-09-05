from django.test import TestCase
from .models import Exhibition, ExhibitionClick, ExhibitionLike
from django.contrib.auth.models import User
from django.db.models import Count
import pandas as pd
# Create your tests here.

user_list = list(User.objects.all())
user_id_list = list()
for element in user_list:
    user_id_list.append(element.id)

# exhibition_id 가져오기
exhibition_list = list(Exhibition.objects.all())
exhibition_id_list = list()
for element in exhibition_list:
    exhibition_id_list.append(element.id)

rating_list_uid = list()
rating_list_exid = list()
rating_list_rate = list()
count = 0

#rating list 만들기
for user_c in user_id_list:
    for exhibition_c in exhibition_id_list:
        num = ExhibitionClick.objects.filter(user=user_c, exhibition=exhibition_c).count()
        rating_list_uid.append(user_c)
        rating_list_exid.append(exhibition_c)
        rating_list_rate.append(num)
        if ExhibitionLike.objects.filter(user=user_c, exhibition=exhibition_c).count() > 0:
            num += 5
            rating_list_rate[count] = num
            count += 1


products = {'User': rating_list_uid, 'Exhibition': rating_list_exid, 'Rate': rating_list_rate}
df = pd.DataFrame(products, columns=['User', 'Exhibition', 'Rate'])
print(df.head())
