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
        if request.user.is_authenticated:
            user_id = request.user.id

        #print(user_id)
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
        #print(df_rating.head()) #rating dataframe 확인

        #pivot table 및 matrix만들기
        df_user_exhibit_ratings = df_rating.pivot(index='User', columns='Exhibition', values='Rate').fillna(0)
        #print(df_user_exhibit_ratings.head()) #피벗테이블 확인

        matrix = df_user_exhibit_ratings.as_matrix()
        user_rating_mean = np.mean(matrix, axis=1)
        matrix_user_mean = matrix - user_rating_mean.reshape(-1, 1)
        #print(matrix) #매트릭스 확인
        #print(pd.DataFrame(matrix_user_mean, columns=df_user_exhibit_ratings.columns).head()) #매트릭스 dataframe 형태로 확인
        
        #svd를 이용한 matrix factorization
        U, sigma, Vt = svds(matrix_user_mean, k=2)
        sigma = np.diag(sigma)
        svd_user_predicted_ratings = np.dot(np.dot(U, sigma), Vt) + user_rating_mean.reshape(-1, 1)
        df_svd_preds = pd.DataFrame(svd_user_predicted_ratings, columns=df_user_exhibit_ratings.columns)
        #print(df_svd_preds.head()) #예측 테이블 확인

        #사용자가 이미 본 것을 제외하고 추천
        user_row_number = user_id -1
        sorted_user_predictions = df_svd_preds.iloc[user_row_number].sort_values(ascending=False)
        user_data = df_rating[df_rating.User == user_id]
        user_data = user_data[user_data.Rate > 0]
        user_history = user_data.merge(df_exhibition, on='Exhibition').sort_values(['Rate'], ascending=False)
        recommendations = df_exhibition[~df_exhibition['Exhibition'].isin(user_history['Exhibition'])]
        recommendations = recommendations.merge(pd.DataFrame(sorted_user_predictions).reset_index(), on='Exhibition')
        recommendations = recommendations.rename(columns={user_row_number: 'Predictions'}).sort_values('Predictions', ascending=False).iloc[:4, :]
        #print(recommendations)  #추천 제대로 되는 지 확인
        recommend_return = list()
        recommend_return.append(Exhibition.objects.get(pk=recommendations.iloc[0]['Exhibition']))
        recommend_return.append(Exhibition.objects.get(pk=recommendations.iloc[1]['Exhibition']))
        recommend_return.append(Exhibition.objects.get(pk=recommendations.iloc[2]['Exhibition']))
        recommend_return.append(Exhibition.objects.get(pk=recommendations.iloc[3]['Exhibition']))

        #2.카테고리 기반 추천방식
        #전시회 당 카테고리를 1개만 지정해 놨다고 가정
        #카테고리 선호조사 데이터
        init_category = list(InitialLike.objects.filter(user=user_id))
        init_category_list = list()
        init_cid_list = list()
        init_cex_list = list()
        for element in init_category:
            init_category_list.append(element.category)
            init_cid_list.append(element.user)
            init_cex_list.append(0)
        category = {'User': init_cid_list, 'Exhibition': init_cex_list, 'Category': init_category_list}
        df_init_category = pd.DataFrame(category, columns=['User', 'Exhibition', 'Category'])
        print(df_init_category)
        #유저가 본 전시회들의 카테고리 데이터
        # mask = (user_history.Rate > 3)
        # category_like = user_history.loc[mask, :]
        # category_like.append(df_init_category)
        # category_like.append(df_init_category)
        # category_like.append(df_init_category)
        #print(category_like)
        # category_list = category_like['Category'].value_counts()
        # print(category_list) #좋아하는 카테고리 카운트 제대로 나왔는 지 확인
        # best_category = category_list.unique()
        # print(best_category)

        #유저가 보지 않은 전시회 중 best category와 일치하는 category를 가진 전시회 추천
        recommendations_2 = df_exhibition[~df_exhibition['Exhibition'].isin(user_history['Exhibition'])]
        recommendations_2 = recommendations_2[recommendations_2['Category'].isin(df_init_category['Category'])]
        print(recommendations_2)  #추천 제대로 되는 지 확인

        recommend2_return = list()
        recommend2_return.append(Exhibition.objects.get(pk=recommendations_2.iloc[0]['Exhibition']))
        recommend2_return.append(Exhibition.objects.get(pk=recommendations_2.iloc[1]['Exhibition']))
        recommend2_return.append(Exhibition.objects.get(pk=recommendations_2.iloc[2]['Exhibition']))
        recommend2_return.append(Exhibition.objects.get(pk=recommendations_2.iloc[3]['Exhibition']))

        #3.순위를 통한 추천
        exhibition_list = Exhibition.objects.all().order_by('-click_count')[:4]

        return render(
            request,
            'exhibition/common/recommend_page.html',
            {
               'user_exhibition_list': recommend_return, 'same_exhibition_list': recommend2_return, 'exhibition_list': exhibition_list,
            }
        )
