from sqlalchemy import create_engine, ForeignKey, String, Numeric, Boolean, select, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, sessionmaker


class Base(DeclarativeBase):
    __abstract__ = True
    id: Mapped[int] = mapped_column(primary_key=True)

class Category(Base):
    __tablename__ = 'categories'

    name: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(String(255))

    products: Mapped[list["Product"]] = relationship(back_populates="category")

    def __str__(self):
        return f'{self.id} {self.name}'


class Product(Base):
    __tablename__ = 'products'

    name: Mapped[str] = mapped_column(String(100))
    price: Mapped[float] = mapped_column(Numeric(10, 2))
    in_stock: Mapped[bool] = mapped_column(Boolean)

    category_id: Mapped[int] = mapped_column(ForeignKey('categories.id'))
    category: Mapped["Category"] = relationship(back_populates="products")

    def __str__(self):
        return f'{self.name} {self.price}'


engine = create_engine('sqlite:///shop.db')
Base.metadata.create_all(engine)
LocalSession = sessionmaker(bind=engine)

#Task 1 Наполнение данными
with LocalSession() as session:

    electronics = Category(name='Электроника', description='Гаджеты и устройства.')
    books = Category(name='Книги', description='Печатные книги и электронные книги.')
    clothes = Category(name='Одежда', description='Одежда для мужчин и женщин.')

    session.add_all([electronics, books, clothes])
    session.flush()

    session.add_all([Product(name='Смартфон', price=299.99, in_stock=True, category_id=electronics.id),
                     Product(name='Ноутбук', price=499.99, in_stock=True, category_id=electronics.id),
                     Product(name='Научно-фантастический роман', price=15.99, in_stock=True, category_id=books.id),
                     Product(name='Джинсы', price=40.50, in_stock=True, category_id=clothes.id),
                     Product(name='Футболка', price=20.00, in_stock=True, category_id=clothes.id)])

    session.commit()

# Task 2 Чтение данных
with LocalSession() as session:

    categories = session.execute(select(Category)).scalars().all()
    for category in categories:
        print(category.name)
        for product in category.products:
            print(product.name, product.price)
        print('-' * 30)

# Task 3 Обновление данных
with LocalSession() as session:

    product = session.execute(select(Product).where(Product.name == 'Смартфон')).scalars().first()
    if product:
        product.price = 349.99
        session.commit()
        print(f'Цена обновлена: {product.name} - {product.price}')

# Task 4 Агрегация и группировка
with LocalSession() as session:

    query = (select(Category.name, func.count(Product.id)).join(Product).group_by(Category.name))
    result = session.execute(query).all()
    for row in result:
        print(row)

# Task 5 Группировка с фильтрацией
with LocalSession() as session:

    query = (select(Category.name, func.count(Product.id)).join(Product).group_by(Category.name)
             .having(func.count(Product.id) > 1))
    result = session.execute(query).all()
    for row in result:
        print(row)