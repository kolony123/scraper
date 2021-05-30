import requests
from datetime import timedelta
from bs4 import BeautifulSoup
from django.views import View
from django.shortcuts import render
from django.views.generic import ListView
from collections import Counter
from django.utils import timezone
from . import models
from . import utils


class SearchView(View):
    def get(self, request):

        query = request.GET.get("q", None)
        ctx = {"result": None}
        get_ip_results = utils.get_user_ip(request)

        if query is not None:
            cache = (
                models.SearchResult.objects.prefetch_related("link_set")
                .filter(keyword__iexact=query, ip_address=get_ip_results)
                .order_by("-id")
                .first()
            )
            time_limit = models.TimeLimit.objects.first()
            if (
                not cache
                or cache
                and cache.date + timedelta(minutes=time_limit.time) <= timezone.now()
            ):
                words_from_titles = []
                words_from_descriptions = []
                webiste_links = []

                (
                    top_10_titles,
                    top_10_descriptions,
                    webiste_links,
                    number_of_search,
                ) = utils.google_search(
                    words_from_titles=words_from_titles,
                    words_from_descriptions=words_from_descriptions,
                    webiste_links=webiste_links,
                    query=query,
                )

                search_result = models.SearchResult.objects.create(
                    number_of_search=number_of_search,
                    keyword=query,
                    most_common_descriptions=",".join(
                        [word[0] for word in top_10_titles]
                    ),
                    most_common_titles=",".join(
                        [word[0] for word in top_10_descriptions]
                    ),
                    ip_address=get_ip_results,
                )
                links = []
                for link in webiste_links:
                    links.append(models.Link(scrapper_search=search_result, link=link))

                models.Link.objects.bulk_create(links)
                ctx["search_result"] = search_result

            else:
                ctx["search_result"] = cache

        return render(request, "google_search_results.html", ctx)
