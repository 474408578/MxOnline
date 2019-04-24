import xadmin
from xadmin import views
from .models import EmailVerifyRecord, Banner


# 创建xadmin的最基本管理器配置，并与view绑定
class BaseSetting(object):
    # 开启主题功能
    enable_themes = True
    use_bootswatch = True
    

class GlobalSettings(object):
    site_title = 'NOC后台'
    site_footer = '携程'
    menu_style = 'accordion'
    

class EmailVerifyRecordAdmin(object):
    list_display = ['code', 'email', 'send_type', 'send_time']
    list_filter = ['code', 'email', 'send_type', 'send_time']
    search_fields = ['code', 'email', 'send_type']


class BannerAdmin(object):
    list_display = ['title', 'image', 'url','index', 'add_time']
    list_filter = ['title', 'image', 'url','index', 'add_time']
    search_fields = ['title', 'image', 'url','index']


# 将基本配置管理与view绑定
xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.base.CommAdminView, GlobalSettings)
xadmin.site.register(EmailVerifyRecord, EmailVerifyRecordAdmin)
xadmin.site.register(Banner, BannerAdmin)
