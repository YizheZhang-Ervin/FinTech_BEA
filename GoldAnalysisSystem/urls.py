from GoldAnalysisSystem.views import IndexHandler, DashboardHandler, EntryHandler, ToolsHandler,ErrorHandler

urlpatterns = [
    (r'/', IndexHandler),
    (r'/dashboard/', DashboardHandler),
    (r'/entry_point/', EntryHandler),
    (r'/tools/', ToolsHandler),
    (r'.*', ErrorHandler),
]
