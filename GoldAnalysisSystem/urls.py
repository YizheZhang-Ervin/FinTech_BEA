from GoldAnalysisSystem.database_handler import InsertsqlHandler
from GoldAnalysisSystem.views import IndexHandler, DashboardHandler, ToolsHandler, ErrorHandler, sqlcmdHandler, \
    XAUDashboardHandler, pyjscmdHandler, webHandler, TranslatorHandler, MapHandler, MapEmbedHandler

urlpatterns = [
    (r'/', IndexHandler),
    (r'/dashboard/', DashboardHandler),
    (r'/xau/dashboard/', XAUDashboardHandler),
    (r'/tools/', ToolsHandler),
    (r'/translator/', TranslatorHandler),
    (r'/cmd/sql/', sqlcmdHandler),
    (r'/cmd/pyjs/', pyjscmdHandler),
    (r'/cmd/web/', webHandler),
    (r'/map/', MapHandler),
    (r'/map_embed/', MapEmbedHandler),
    # (r'/sql/', InsertsqlHandler),
    (r'.*', ErrorHandler),

]
