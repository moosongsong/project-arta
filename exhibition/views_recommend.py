from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from .models import Exhibition, Category, Material, Piece, Comment, GuestBook, ExhibitionLike, PieceLike, \
    ExhibitionClick, PieceClick, ExhibitionShare, PieceShare, InitialLike
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.models import User
import pandas as pd
from sklearn.decomposition import TruncatedSVD
from scipy.sparse.linalg import svds
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


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
        df_exhibition = pd.DataFrame(exhibit_temp, columns=['Exhibition', 'Category'])  #dataframe으로 변경

        #rating list 만들기
        rating_list_uid = list()
        rating_list_xid = list()
        rating_list_rate = list()
        count = 0

        for user_c in user_id_list:
            for exhibition_c in exhibition_id_list:
                num = ExhibitionClick.objects.filter(user=user_c, exhibition=exhibition_c).count()
                rating_list_uid.append(user_c)
                rating_list_xid.append(exhibition_c)
                rating_list_rate.append(num)
                if ExhibitionLike.objects.filter(user=user_c, exhibition=exhibition_c).count() > 0:
                    num += 5
                    rating_list_rate[count] = num
                    count += 1

        rating = {'User': rating_list_uid, 'Exhibition': rating_list_xid, 'Rate': rating_list_rate}
        df_rating = pd.DataFrame(rating, columns=['User', 'Exhibition', 'Rate'])
        print(df_rating.head()) #rating dataframe 확인

        #pivot table 및 matrix만들기
        df_user_exhibit_ratings = df_rating.pivot(index='User', columns='Exhibition', values='Rate').fillna(0)
        print(df_user_exhibit_ratings.head()) #피벗테이블 확인

        matrix = df_user_exhibit_ratings.as_matrix()
        user_rating_mean = np.mean(matrix, axis=1)
        matrix_user_mean = matrix - user_rating_mean.reshape(-1, 1)
        print(matrix) #매트릭스 확인
        print(pd.DataFrame(matrix_user_mean, columns=df_user_exhibit_ratings.columns).head()) #매트릭스 dataframe 형태로 확인
        
        #svd를 이용한 matrix factorization
        U, sigma, Vt = svds(matrix_user_mean, k=2)
        sigma = np.diag(sigma)
        svd_user_predicted_ratings = np.dot(np.dot(U, sigma), Vt) + user_rating_mean.reshape(-1, 1)
        df_svd_preds = pd.DataFrame(svd_user_predicted_ratings, columns=df_user_exhibit_ratings.columns)
        print(df_svd_preds.head()) #예측 테이블 확인

        #request가 추천을 원하는 유저의 id라고 생각, 4라고 기재해 놓은 것은 몇개 추천할지..?
        #user_row_number = request -1    #user_id가 0부터 시작하면 -1 안해도 됨
        user_row_number = 1
        sorted_user_predictions = df_svd_preds.iloc[user_row_number].sort_values(ascending=False)
        user_data = df_rating[df_rating.User == request]
        user_history = user_data.merge(df_exhibition, on='Exhibition').sort_values(['Rate'], ascending=False)
        recommendations = df_exhibition[~df_exhibition['Exhibition'].isin(user_history['Exhibition'])]
        recommendations = recommendations.merge(pd.DataFrame(sorted_user_predictions).reset_index(), on='Exhibition')
        recommendations = recommendations.rename(columns={user_row_number: 'Predictions'}).sort_values('Predictions', ascending=False).iloc[:3, :]
        print(recommendations)  #추천 제대로 되는 지 확인

        recommend_return = list()
        recommend_return.append(Exhibition.objects.filter(exhibition=recommendations.iloc[0]['Exhibition']))
        recommend_return.append(Exhibition.objects.filter(exhibition=recommendations.iloc[1]['Exhibition']))
        recommend_return.append(Exhibition.objects.filter(exhibition=recommendations.iloc[2]['Exhibition']))
        recommend_return.append(Exhibition.objects.filter(exhibition=recommendations.iloc[3]['Exhibition']))

        #2.카테고리 기반 추천방식
        #전시회 당 카테고리를 1개만 지정해 놨다고 가정
        #카테고리 선호조사 데이터
 #       init_category = list(InitialLike.objects.filter(user=1))
 #       init_category_list = list()
 #       init_cid_list = list()
 #       init_cex_list = list()
 #       for element in init_category:
 #           init_category_list.append(element.category)
 #           init_cid_list.append(element.user)
 #           init_cex_list.append(0)
 #       category = {'User': init_cid_list, 'Exhibition': init_cex_list, 'Category': init_category_list}
 #       df_init_category = pd.DataFrame(category, columns=['User', 'Exhibition', 'Category'])

        #유저가 본 전시회들의 카테고리 데이터
 #       mask = (user_history.Rate > 3)
 #       category_like = user_history.loc[mask, :]

#        category_like.append(df_init_category)
 #       category_like.append(df_init_category)
  #      category_like.append(df_init_category)
   #     category_like = category_like.groupby('Category').count
   #     category_like = category_like.sort_values(by=['Exhibition'], ascending=False)
        #위에 sort_values확인해보기...
   #     print(category_like)    #좋아하는 카테고리 카운트 제대로 나왔는 지 확인
   #     best_category = category_like.iloc[0, 2]

        #유저가 보지 않은 전시회 중 best category와 일치하는 category를 가진 전시회 추천
    #    recommendations_2 = df_exhibition[~df_exhibition['Exhibition'].isin(user_history['Exhibition'])]
    #    recommendations_2 = recommendations_2[recommendations_2['Category'].isin(best_category)]
    #    same_category = recommendations_2['Category'] == best_category
    #    recommendations_2 = recommendations_2[same_category]
    #    print(recommendations_2) #추천 제대로 되는 지 확인

        #3.순위를 통한 추천
        #exhibition_like에서 exhibition group으로 묶어서 top 4, exhibition_click에서 exhibition group으로 묶어서 top 4 두개 겹치는거 제외한 뒤, 랜덤 4개 추천(희망사항)
        #exhibition_like에서 exhibition group으로 묶어서 top 4 추천하는 것으로..



    #   아이템 기반 추천 (사용x, 예비용)
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
            'exhibition/common/recommend_page.html',
            {
               'exhibition_list': recommend_return,
            }
        )
