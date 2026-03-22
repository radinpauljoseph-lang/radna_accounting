from django.contrib import admin
from django.urls import include, path

from .views import (
    chart_of_accounts,
    journal_entry,
    accounting_periods,
    journal_voucher
)
urlpatterns = [
    path('admin/', admin.site.urls),
    path("accounts", chart_of_accounts.createAccountRequest),
    path("accounts/<str:id>", chart_of_accounts.getUpdateAccountRequest),
    path("journalEntry", journal_entry.createJournalEntryRequest),
    path("journalEntry/<str:id>", journal_entry.getUpdateJournalEntryRequest),
    path("journalEntry/transactionId/<str:transaction_id>", journal_entry.getJournalEntryByTransactionIdRequest),
    path("journalEntry/<str:id>/checkAmounts", journal_entry.getTransactionIdCreditDebitAmountRequest),
    path("journalEntry/<str:id>/forReview", journal_entry.setTransactionIdForReviewRequest),
    path("journalEntry/<str:id>/approve", journal_entry.approveJournalEntriesByTransactionIdRequest),
    path("journalEntry/<str:id>/reject", journal_entry.rejectJournalEntriesByTransactionIdRequest),
    path("journalEntry/<str:id>/post", journal_entry.postJournalEntriesByTransactionIdRequest),
    path("journalVoucher/<str:id>/download", journal_voucher.downloadJournalVoucherFileRequest),
    # path("journal-entry/transaction-id/<str:transaction_id>", journal_entry.get_delete_journal_entry_by_transaction_id_request),
    # path("journal-entry/post/month/<int:month>/year/<int:year>", journal_entry.post_journal_entry_by_month_year_request),
    path("accountingPeriod", accounting_periods.createAccountingPeriodRequest),
    path("accountingPeriod/close", accounting_periods.closeAccountingPeriodRequest)
    # path("accounting-period/open", accounting_periods.create_accounting_period_request),
    # path("accounting-period/close", accounting_periods.close_accounting_period_request)
]
