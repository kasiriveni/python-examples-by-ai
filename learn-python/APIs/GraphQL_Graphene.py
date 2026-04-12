# GraphQL with Graphene

from graphene import ObjectType, String, Schema

class Query(ObjectType):
    hello = String(name=String(default_value="stranger"))

    def resolve_hello(root, info, name):
        return f"Hello, {name}!"

schema = Schema(query=Query)

query = '{ hello(name: "Alice") }'
result = schema.execute(query)
print(result.data["hello"])
