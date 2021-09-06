from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from .models import Exhibition, Category, Material, Piece, Comment, GuestBook, ExhibitionLike, PieceLike, \
    ExhibitionClick, PieceClick, ExhibitionShare, PieceShare, Rating
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.models import User
import pandas as pd


class Recommend:
    def get_recommend_page(request):
        #user_id 가져오기
        user_list = list(User.objects.all())
        user_id_list = list()
        for element in user_list:
            user_id_list.append(element.id)

        #exhibition_id, category 가져오기
        exhibition_list = list(Exhibition.objects.all())
        exhibition_id_list = list()
        exhibition_info_list = list()
        for element in exhibition_list:
            exhibition_id_list.append(element.id)
            exhibition_info_list.append(element.category)

        exhibit_temp = {'Exhibition': exhibition_id_list, 'Category': exhibition_info_list}
        df_exhibition = pd.DataFrame(exhibit_temp, columns=['Exhibition', 'Category'])

        #rating list 만들기
        rating_list_uid = list()
        rating_list_exid = list()
        rating_list_rate = list()
        count = 0

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

        rating = {'User': rating_list_uid, 'Exhibition': rating_list_exid, 'Rate': rating_list_rate}
        df_rating = pd.DataFrame(rating, columns=['User', 'Exhibition', 'Rate'])
        print(df_rating.head()) #rating dataframe 확인

        #pivot table 및 matrix만들기
        df_user_exhibit_ratings = df_rating.pivot(index='User', columns='Exhibition', values='Rate').fillna(0)
        print(df_user_exhibit_ratings.head()) #피벗테이블 확인

        matrix = df_user_exhibit_ratings.as_matrix()
        user_rating_mean = np.mean(matrix, asix = 1)
        matrix_user_mean = matrix - user_rating_mean.reshape(-1,1)
        print(matrix) #매트릭스 확인
        print(pd.DataFrame(matrix_user_mean, columns = df_user_exhibit_ratings.columns).head()) #매트릭스 dataframe 형태로 확인
        
        #svd를 이용한 matrix factorization
        U, sigma, Vt = svds(matrix_user_mean, k = 12)
        sigma = np.diag(sigma)
        svd_user_predicted_ratings = np.dot(np.dot(U, sigma), Vt) + user_rating_mean.reshape(-1,1)
        df_svd_preds = pd.DataFrame(svd_user_predicted_ratings, columns = df_user_exhibit_ratings.columns)
        print(df_svd_preds.head()) #예측 테이블 확인

        #request가 추천을 원하는 유저의 id라고 생각, 4라고 기재해 놓은 것은 몇개 추천할지..?
        user_row_number = request -1    #user_id가 0부터 시작하면 -1 안해도 됨
        sorted_user_predictions = df_svd_preds.iloc[user_row_number].sort_values(ascending=False)
        user_data = df_rating[df_rating.User == request]
        user_history = user_data.merge(df_exhibition, on = 'Exhibition').sort_values(['Rate'], ascending=False)
        recommendations = df_exhibition[~df_exhibition['Exhibition'].isin(user_history['Exhibition'])]
        recommendations = recommendations.merge(pd.DataFrame(sorted_user_predictions).reset_index(), on = 'Exhibition')
        recommendations = recommendations.rename(columns = {user_row_number: 'Predictions'}).sort_values('Predictions', ascending=False).iloc[:4, :]
        print(recommendations)  #추천 제대로 되는 지 확인

    #   아이템 기반 추천
    #    user_exhibit_rating = df.pivot_table('Rate', index='User', columns='Exhibition').fillna(0)
    #    exhibit_user_rating = df.pivot_table('Rate', index='Exhibition', columns='User').fillna(0)
    #    print(user_exhibit_rating.head())
    #    print(exhibit_user_rating.head())
    #    item_based_collabor = cosine_similarity(exhibit_user_rating)
    #    print(item_based_collabor)
    #    item_based_collabor = pd.DataFrame(data = item_based_collabor, index = exhibit_user_rating.index, columns = exhibit_user_rating.index)
    #    def get_item_based_collabor(title):
    #        return item_based_collabor[title].sort_values(ascending=False)[:4]

        return render(
            request,
            'exhibition/common/recommend_page.html'
            # {
            # recommendations #exhibition_id, category, predictions로 이루어진 data frame..? 출력됨
            # 어떤 형식의 return값을 줘야하는지
            # }
        )
