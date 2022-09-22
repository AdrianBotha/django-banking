from django_banking.celery import app


@app.task()
def import_trades_csv(csv_import_id):
    # Would generally like to avoid in-function imports like this.
    from django_banking.models import CSVImport
    from django_banking.services import csv_import

    csv_import.import_trades_csv(CSVImport.objects.get(id=csv_import_id))
