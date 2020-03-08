from GoldAnalysisSystem.database_handler import InsertsqlHandler
from GoldAnalysisSystem.views import IndexHandler, DashboardHandler, ToolsHandler, ErrorHandler

urlpatterns = [
    (r'/', IndexHandler),
    (r'/dashboard/', DashboardHandler),
    (r'/tools/', ToolsHandler),
    # (r'/sql/', InsertsqlHandler),
    (r'.*', ErrorHandler),

]
