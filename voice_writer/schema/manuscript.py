import graphene
from graphene_django import DjangoObjectType
from voice_writer.models import Manuscript


class ManuscriptType(DjangoObjectType):
    class Meta:
        model = Manuscript
        fields = "__all__"


class CreateManuscript(graphene.Mutation):
    class Arguments:
        user_id = graphene.ID(required=True)
        title = graphene.String(required=True)
        type = graphene.String(required=True)
        genre = graphene.String()
        summary = graphene.String()
        manuscript_id = graphene.ID(required=True)
        user_id = graphene.ID(required=True)

    manuscript = graphene.Field(ManuscriptType)

    def mutate(self, info, title, type, manuscript_id, user_id, genre=None, summary=None):
        manuscript = Manuscript(
            title=title,
            type=type,
            genre=genre,
            summary=summary,
            manuscript_id=manuscript_id,
            user_id=user_id,
        )
        manuscript.save()
        return CreateManuscript(manuscript=manuscript)


class UpdateManuscript(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        title = graphene.String()
        type = graphene.String()
        genre = graphene.String()
        summary = graphene.String()

    manuscript = graphene.Field(ManuscriptType)

    def mutate(self, info, id, title=None, type=None, genre=None, summary=None):
        manuscript = Manuscript.objects.get(pk=id)
        if title:
            manuscript.title = title
        if type:
            manuscript.type = type
        if genre:
            manuscript.genre = genre
        if summary:
            manuscript.summary = summary
        manuscript.save()
        return UpdateManuscript(manuscript=manuscript)


class DeleteManuscript(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    ok = graphene.Boolean()

    def mutate(self, info, id):
        manuscript = Manuscript.objects.get(pk=id)
        manuscript.delete()
        return DeleteManuscript(ok=True)


class ManuscriptQuery(graphene.ObjectType):
    all_manuscripts = graphene.List(ManuscriptType)
    manuscript = graphene.Field(
        ManuscriptType,
        id=graphene.ID(required=True)
    )

    def resolve_all_manuscripts(root, info):
        return Manuscript.objects.all()

    def resolve_manuscript(self, info, id):
        return manuscript.objects.get(pk=id)


class ManuscriptMutation(graphene.ObjectType):
    create_manuscript = CreateManuscript.Field()
    update_manuscript = UpdateManuscript.Field()
    delete_manuscript = DeleteManuscript.Field()
