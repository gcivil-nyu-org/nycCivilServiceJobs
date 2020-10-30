from django.urls import path
from jobs.views import JobsView
from jobs.views import SearchResultsView

app_name = "jobs"
urlpatterns = [
    path("", JobsView.as_view(), name="jobs"),
    path("search/", SearchResultsView.as_view(), name="results"),
    path("fav/<int:job_id>/", JobsView.add_favorite, name="add_favorite"),
    # path("profile/favourites/", JobsView.favorite_list, name="favorite_list"),  # TO DO
    path("favorites", JobsView.as_view(template_name="jobs/favorites.html"), name="favorites_page"),  # REMOVE LATER
]
