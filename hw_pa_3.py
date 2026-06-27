from sqlalchemy import create_engine, ForeignKey, Numeric, String, Boolean
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
        return f'{self.id} {self.name} {self.price} {self.in_stock}'


engine = create_engine('sqlite:///:memory:')
Base.metadata.create_all(engine)
LocalSession = sessionmaker(bind=engine)


with LocalSession() as session:
    electronics = Category(name='Electronics', description='Electronic devices')
    books = Category(name='Books', description='Books and other')

    session.add_all([electronics, books])
    session.commit()

    product_1 = Product(
        name='Book',
        price=39.99,
        in_stock=True,
        category_id=books.id
    )
    product_2 = Product(
        name="Laptop",
        price=1500.19,
        in_stock=True,
        category_id=electronics.id
    )
    session.add(product_1)
    session.add(product_2)
    session.commit()

    products = session.query(Product).all()
    for p in products:
        print(f"Product: {p.name} | Price: {p.price} | In stock: {p.in_stock} | Category: {p.category.name}")

    categories = session.query(Category).all()
    for c in categories:
        print(f"Category: {c.name} | Description: {c.description}")