from GoldAnalysisSystem.database_handler import InsertsqlHandler
from GoldAnalysisSystem.views import IndexHandler, DashboardHandler, ToolsHandler, ErrorHandler, sqlcmdHandler

urlpatterns = [
    (r'/', IndexHandler),
    (r'/dashboard/', DashboardHandler),
    (r'/tools/', ToolsHandler),
    # (r'/sql/', InsertsqlHandler),
    (r'/sql/cmd/', sqlcmdHandler),
    (r'.*', ErrorHandler),

]
