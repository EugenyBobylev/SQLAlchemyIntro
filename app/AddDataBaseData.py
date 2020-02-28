from sqlalchemy.orm import sessionmaker

from app.db import engine, Cookie

Session = sessionmaker(bind=engine)
session = Session()

cc_cookie = Cookie(cookie_name='chocolate chip',
                   cookie_recipe_url='http://some.aweso.me/cookie/recipe.html',
                   cookie_sku='CC01',
                   quantity=12,
                   unit_cost=0.50)
session.add(cc_cookie)
session.commit()