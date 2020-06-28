from django.urls import path
from .views import war_greetings, create_avatar, summary, battle, rest

urlpatterns = [
    path('', war_greetings, name='greetings'),
    path('avatar/', create_avatar, name="create"),
    path('battle/<int:beast_id>/<int:avatar_id>/', battle, name="battle"),
    path('rest/<int:beast_id>/<int:avatar_id>/', rest, name="rest"),
    path('avatar/<int:avatar_id>/', summary, name="summary"),
]
