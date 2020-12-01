from .auth import login_required
from . import rest


@login_required
def get_payments(sort_by_name: bool = True):
    raw = rest.iface.get_payments()
    if sort_by_name:
        raw = sorted(raw, key=lambda i: i['name'])
    payments = {}
    for p in raw:
        id = p['id']
        name = p['name']
        payments[id] = name
    return payments
