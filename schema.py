import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType
from models import BakeryItem, db  # Import your SQLAlchemy models

# Define your GraphQL types
class BakeryItemType(SQLAlchemyObjectType):
    class Meta:
        model = BakeryItem

class Query(graphene.ObjectType):
    # Query to get a list of all bakery items
    products = graphene.List(BakeryItemType)

    # Query to get a bakery item by ID
    bakery_item_by_id = graphene.Field(BakeryItemType, id=graphene.Int(required=True))

    def resolve_products(self, info):
        return BakeryItem.query.all()

    def resolve_bakery_item_by_id(self, info, id):
        return BakeryItem.query.get(id)

class CreateBakeryItem(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        quantity = graphene.Int(required=True)
        price = graphene.Float(required=True)
        category = graphene.String(required=True)

    bakery_item = graphene.Field(BakeryItemType)

    def mutate(self, info, name, quantity, price, category):
        bakery_item = BakeryItem(name=name, quantity=quantity, price=price, category=category)
        db.session.add(bakery_item)
        db.session.commit()
        return CreateBakeryItem(bakery_item=bakery_item)

class UpdateBakeryItem(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        name = graphene.String()
        quantity = graphene.Int()
        price = graphene.Float()
        category = graphene.String()

    bakery_item = graphene.Field(BakeryItemType)

    def mutate(self, info, id, name=None, quantity=None, price=None, category=None):
        bakery_item = BakeryItem.query.get(id)
        if name is not None:
            bakery_item.name = name
        if quantity is not None:
            bakery_item.quantity = quantity
        if price is not None:
            bakery_item.price = price
        if category is not None:
            bakery_item.category = category
        db.session.commit()
        return UpdateBakeryItem(bakery_item=bakery_item)

class DeleteBakeryItem(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)

    success = graphene.String()

    def mutate(self, info, id):
        bakery_item = BakeryItem.query.get(id)
        if bakery_item:
            db.session.delete(bakery_item)
            db.session.commit()
            return DeleteBakeryItem(success="Bakery item deleted successfully")
        return DeleteBakeryItem(success="Bakery item not found")

class Mutation(graphene.ObjectType):
    create_bakery_item = CreateBakeryItem.Field()
    update_bakery_item = UpdateBakeryItem.Field()
    delete_bakery_item = DeleteBakeryItem.Field()

# Define the schema
schema = graphene.Schema(query=Query, mutation=Mutation)
