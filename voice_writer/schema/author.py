import graphene
from graphene_django import DjangoObjectType
from graphene_file_upload.scalars import Upload
from voice_writer.models import Author


# Define the AuthorType for queries
class AuthorType(DjangoObjectType):
    class Meta:
        model = Author
        fields = "__all__"


# Define Mutations
class CreateAuthor(graphene.Mutation):
    class Arguments:
        user_id = graphene.ID(required=True)
        first_name = graphene.String(required=True)
        last_name = graphene.String(required=True)
        pen_name = graphene.String()
        pronouns = graphene.String()
        date_of_birth = graphene.Date()
        nationality = graphene.String()
        location = graphene.String()
        biography = graphene.String()
        portrait = Upload()

    author = graphene.Field(AuthorType)

    def mutate(self, info, user_id, first_name, last_name, pen_name=None, pronouns=None, date_of_birth=None, nationality=None, location=None, biography=None , portrait=None):
        author = Author(
            first_name=first_name,
            last_name=last_name,
            pen_name=pen_name,
            pronouns=pronouns,
            date_of_birth=date_of_birth,
            nationality=nationality,
            location=location,
            biography=biography,
            user_id=user_id,
            portrait=portrait,
        )
        author.save()
        return CreateAuthor(author=author)


class UpdateAuthor(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        first_name = graphene.String()
        last_name = graphene.String()
        pen_name = graphene.String()
        pronouns = graphene.String()
        date_of_birth = graphene.Date()
        nationality = graphene.String()
        location = graphene.String()
        biography = graphene.String()
        portrait = Upload()

    author = graphene.Field(AuthorType)

    def mutate(self, info, id, first_name=None, last_name=None, pen_name=None, pronouns=None, date_of_birth=None, nationality=None, location=None, biography=None, portrait=None):
        author = Author.objects.get(pk=id)
        if first_name:
            author.first_name = first_name
        if last_name:
            author.last_name = last_name
        if pen_name:
            author.pen_name = pen_name
        if pronouns:
            author.pronouns = pronouns
        if date_of_birth:
            author.date_of_birth = date_of_birth
        if nationality:
            author.nationality = nationality
        if location:
            author.location = location
        if biography:
            author.biography = biography
        if portrait:
            author.portrait = portrait
        author.save()
        return UpdateAuthor(author=author)


class DeleteAuthor(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    ok = graphene.Boolean()

    def mutate(self, info, id):
        author = Author.objects.get(pk=id)
        author.delete()
        return DeleteAuthor(ok=True)


# Combine Queries and Mutations
class AuthorQuery(graphene.ObjectType):
    all_authors = graphene.List(AuthorType)
    author = graphene.Field(
        AuthorType,
        id=graphene.ID(required=True)
    )

    def resolve_all_authors(root, info):
        return Author.objects.all()

    def resolve_author(self, info, id):
        return Author.objects.get(pk=id)


class AuthorMutation(graphene.ObjectType):
    create_author = CreateAuthor.Field()
    update_author = UpdateAuthor.Field()
    delete_author = DeleteAuthor.Field()