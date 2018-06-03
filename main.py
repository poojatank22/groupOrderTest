from app import app, db
from app.models import Grouporder, Orders

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Grouporder': Grouporder, 'Orders': Orders}