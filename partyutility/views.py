# partyutility/views.py
from django.views.generic import TemplateView
from django.utils.timezone import now


class IndexView(TemplateView):
    template_name = "partyutility/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["now"] = now()
        return context
