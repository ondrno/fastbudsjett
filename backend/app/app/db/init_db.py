from sqlalchemy.orm import Session

from app import crud, schemas
from app.core.config import settings
from app.db import base  # noqa: F401

# make sure all SQL Alchemy models are imported (app.db.base) before initializing DB
# otherwise, SQL Alchemy might fail to initialize relationships properly
# for more details: https://github.com/tiangolo/full-stack-fastapi-postgresql/issues/28


def init_db(db: Session) -> None:
    # Tables should be created with Alembic migrations
    # But if you don't want to use migrations, create
    # the tables un-commenting the next line
    # Base.metadata.create_all(bind=engine)

    user = crud.user.get_by_email(db, email=settings.FIRST_SUPERUSER)
    if not user:
        user_in = schemas.UserCreate(
            email=settings.FIRST_SUPERUSER,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            is_superuser=True,
        )
        crud.user.create(db, obj_in=user_in)  # noqa: F841

    # item_types = crud.itemtype.get_multi(db)
    # if not item_types:
    #     for name in ["revenue", "expenditure"]:
    #         type_in = schemas.ItemTypeCreate(
    #             name=name
    #         )
    #         crud.itemtype.create(db, obj_in=type_in)  # noqa: F841
    #
    # categories = crud.category.get_multi(db)
    # if not categories:
    #     item_types = crud.itemtype.get_multi(db)
    #     default_categories = {
    #         'expenditure': ["banking", "car", "clothes", "communication", "electronics", "food", "go out", "health",
    #                         "holidays", "housing", "kids", "pets", "sport", "leisure", "transport"],
    #         'revenue': ["salary", "gift", "other"]
    #     }
    #     for i in item_types:
    #         item_name = i.name
    #         item_id = i.id
    #         for cat_name in default_categories[name]:
    #             category_in = schemas.CategoryCreate(name=cat_name, itemtype_id=item_id)
    #             crud.category.create(db, obj_in=category_in)  # noqa: F841
    #
    # payments = crud.payment.get_multi(db)
    # if not payments:
    #     for name in ["cash", "payment card", "bank transfer"]:
    #         payment_in = schemas.PaymentCreate(
    #             name=name
    #         )
    #         crud.payment.create(db, obj_in=payment_in)  # noqa: F841
