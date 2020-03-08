from GoldAnalysisSystem.postgresql_handler import InsertsqlHandler
from GoldAnalysisSystem.views import IndexHandler, DashboardHandler, ToolsHandler, ErrorHandler

urlpatterns = [
    (r'/', IndexHandler),
    (r'/dashboard/', DashboardHandler),
    # (r'/entry_point/', EntryHandler),
    (r'/tools/', ToolsHandler),
    (r'.*', ErrorHandler),
    (r'/sql/', InsertsqlHandler),
]
