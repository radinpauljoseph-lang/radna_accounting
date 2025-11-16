"""
URL configuration for radna_accounting project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path

from .views import (
    chart_of_accounts,
    journal_entry,
    accounting_periods
)
urlpatterns = [
    path('admin/', admin.site.urls),
    path("accounts", chart_of_accounts.create_account_request),
    path("accounts/<str:id>", chart_of_accounts.get_update_account_request),
    path("journal-entry", journal_entry.create_journal_entry_request),
    path("journal-entry/<str:id>", journal_entry.get_update_journal_entry_request),
    path("journal-entry/transaction-id/<str:transaction_id>", journal_entry.get_delete_journal_entry_by_transaction_id_request),
    path("journal-entry/post/month/<int:month>/year/<int:year>", journal_entry.post_journal_entry_by_month_year_request),
    path("accounting-period/open", accounting_periods.create_accounting_period_request),
    path("accounting-period/close", accounting_periods.close_accounting_period_request)
]
