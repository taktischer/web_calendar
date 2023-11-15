from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = "index.html"

class BalcinovicView(TemplateView):
    template_name = "balcinovic.html"