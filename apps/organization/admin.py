import xadmin

from organization.models import CityDict, CourseOrg, Teacher


class CityDictAdmin(object):
    list_display = ['name', 'desc', 'add_time']
    list_filter = ['name', 'desc', 'add_time']
    search_fields = ['name', 'desc']


class CourseOrgAdmin(object):
    list_display = ['name', 'desc', 'click_nums', 'fav_nums', 'city', 'address', 'add_time']
    list_filter = ['name', 'desc', 'click_nums', 'fav_nums', 'city', 'address', 'add_time']
    search_fields = ['name', 'city', 'address', 'tag']
    
    
class TeacherAdmin(object):
    list_display = ['name', 'org', 'work_years', 'work_company', 'add_time']
    list_filter = ['name', 'org', 'work_years', 'work_company', 'add_time']
    search_fields = ['name', 'org', 'work_years', 'work_company']
    

xadmin.site.register(CityDict, CityDictAdmin)
xadmin.site.register(CourseOrg, CourseOrgAdmin)
xadmin.site.register(Teacher, TeacherAdmin)