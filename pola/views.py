from django.core.exceptions import ImproperlyConfigured
from django.http import HttpResponseRedirect
from django.utils.encoding import force_text
from django.views.generic import TemplateView
from django.views.generic.detail import (
    BaseDetailView, SingleObjectTemplateResponseMixin)
from braces.views import LoginRequiredMixin
from company.models import Company
from product.models import Product
from report.models import Report
from pola.models import Stats
from django.utils import timezone
from datetime import datetime, timedelta
from django.core.exceptions import ObjectDoesNotExist


class FrontPageView(LoginRequiredMixin, TemplateView):
    template_name = 'pages/home-cms.html'

    def get_context_data(self, *args, **kwargs):
        c = super(FrontPageView, self).get_context_data(**kwargs)
        c['oldest_reports'] = (Report.objects.only_open()
                                     .order_by('created_at')[:10])
        c['newest_reports'] = (Report.objects.only_open()
                                     .order_by('-created_at')[:10])
        c['most_popular_products'] = (Product.objects
                                             .with_query_count()
                                             .filter(company__isnull=True)
                                             .order_by('-query_count')[:10])
        c['most_popular_companies'] = (Company.objects
                                              .with_query_count()
                                              .filter(verified=False)
                                              .order_by('-query_count')[:10])
        return c


class ActionMixin(object):
    success_url = None

    def action(self):
        raise ImproperlyConfigured("No action to do. Provide a action body.")

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.action()
        return HttpResponseRedirect(success_url)

    def get_success_url(self):
        if self.success_url:
            self.success_url = force_text(self.success_url)
            return self.success_url.format(**self.object.__dict__)
        else:
            raise ImproperlyConfigured(
                "No URL to redirect to. Provide a success_url.")


class BaseActionView(ActionMixin, BaseDetailView):
    """
    Base view for action on an object.
    Using this base class requires subclassing to provide a response mixin.
    """


class ActionView(SingleObjectTemplateResponseMixin, BaseActionView):
    template_name_suffix = '_action'


class StatsPageView(LoginRequiredMixin, TemplateView):
    template_name = 'pages/home-stats.html'

    def get_context_data(self, *args, **kwargs):
        c = super(StatsPageView, self).get_context_data(**kwargs)

        stats = []

        date = timezone.now()
        for i in range(0, 30):
            midnight = datetime(
                date.year, date.month, date.day) + timedelta(days=1)
            try:
                stat = Stats.objects.get(
                    year=date.year, month=date.month, day=date.day)
            except ObjectDoesNotExist:
                stat = Stats()
            if stat.year is None or stat.calculated_at < timezone.make_aware(midnight, timezone.get_default_timezone()):
                stat.calculate(date.year, date.month, date.day)
                Stats.save(stat)
            date = date - timedelta(days=1)

            stats.append(stat)

        c['stats'] = list(reversed(stats))
        return c
