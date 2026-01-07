from django.contrib import admin
from django.urls import include, path

from .views import (
    chart_of_accounts,
    journal_entry,
    accounting_periods
)
urlpatterns = [
    path('admin/', admin.site.urls),
    path("accounts", chart_of_accounts.createAccountRequest),
    path("accounts/<str:id>", chart_of_accounts.getUpdateAccountRequest),
    path("journal-entry", journal_entry.create_journal_entry_request),
    path("journal-entry/<str:id>", journal_entry.get_update_journal_entry_request),
    path("journal-entry/transaction-id/<str:transaction_id>", journal_entry.get_delete_journal_entry_by_transaction_id_request),
    path("journal-entry/post/month/<int:month>/year/<int:year>", journal_entry.post_journal_entry_by_month_year_request),
    path("accounting-period/open", accounting_periods.create_accounting_period_request),
    path("accounting-period/close", accounting_periods.close_accounting_period_request)
]
