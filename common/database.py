from flask import g
from flask_sqlalchemy import SQLAlchemy,model

class MultiTenantSQLAlchemy(SQLAlchemy):
    Model = model
    def choose_tenant(self, bind_key):
        if hasattr(g, 'tenant'):
            raise RuntimeError('Switch Tenant in the middle of the request')
        g.tenant = bind_key

    def get_engine(self, app=None, bind=None):
        if bind is None:
            if not hasattr(g, 'tenant'):
                raise RuntimeError('No tenant chosen')
            bind = g.tenant
        return super().get_engine(app=app, bind=bind)

db=MultiTenantSQLAlchemy()