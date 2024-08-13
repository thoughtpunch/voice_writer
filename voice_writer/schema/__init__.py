# voice_writer/schema/__init__.py
import graphene
from .query import Query
from .mutations import Mutation

# If you have mutations, you would also include them here
# class Mutation(graphene.ObjectType):
#     # Define your mutations here

schema = graphene.Schema(query=Query, mutation=Mutation)