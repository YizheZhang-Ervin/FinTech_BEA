from GoldAnalysisSystem.database_handler import InsertsqlHandler
from GoldAnalysisSystem.views import IndexHandler, DashboardHandler, ToolsHandler, ErrorHandler, sqlcmdHandler, \
    XAUDashboardHandler, pyjscmdHandler, webHandler

urlpatterns = [
    (r'/', IndexHandler),
    (r'/dashboard/', DashboardHandler),
    (r'/xau/dashboard/', XAUDashboardHandler),
    (r'/tools/', ToolsHandler),
    # (r'/sql/', InsertsqlHandler),
    (r'/cmd/sql/', sqlcmdHandler),
    (r'/cmd/pyjs/', pyjscmdHandler),
    (r'/cmd/web/', webHandler),
    (r'.*', ErrorHandler),

]
