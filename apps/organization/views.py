# from django.core.paginator import PageNotAnInteger
from django.core.paginator import PageNotAnInteger, Paginator, EmptyPage
from django.shortcuts import render
from django.views import View

from organization.models import CourseOrg, CityDict


class OrgListView(View):
    def get(self, request):
        all_orgs = CourseOrg.objects.all()
        org_nums = all_orgs.count()
        all_citys = CityDict.objects.all()
        paginator = Paginator(all_orgs, 2)
        page = request.GET.get('page')
        try:
            orgs = paginator.page(page)
        except PageNotAnInteger:
            orgs = paginator.page(1)
        except EmptyPage:
            orgs = paginator.page(paginator.num_pages)
        
        return render(request, "org_list.html", {
            "all_orgs": orgs,
            "all_citys": all_citys,
            "org_nums": org_nums
        })