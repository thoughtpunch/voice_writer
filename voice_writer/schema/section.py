import graphene
from graphene_django import DjangoObjectType
from voice_writer.models import Section


class SectionType(DjangoObjectType):
    class Meta:
        model = Section
        fields = "__all__"


class CreateSection(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        type = graphene.String(required=True)
        order = graphene.Int(required=True)
        manuscript_id = graphene.ID(required=True)

    section = graphene.Field(SectionType)

    def mutate(self, info, title, type, order, manuscript_id):
        section = Section(
            title=title,
            type=type,
            order=order,
            manuscript_id=manuscript_id,
        )
        section.save()
        return CreateSection(section=section)


class UpdateSection(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        title = graphene.String()
        type = graphene.String()
        order = graphene.Int()

    section = graphene.Field(SectionType)

    def mutate(self, info, id, title=None, type=None, order=None):
        section = Section.objects.get(pk=id)
        if title:
            section.title = title
        if type:
            section.type = type
        if order is not None:
            section.order = order
        section.save()
        return UpdateSection(section=section)


class DeleteSection(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    ok = graphene.Boolean()

    def mutate(self, info, id):
        section = Section.objects.get(pk=id)
        section.delete()
        return DeleteSection(ok=True)


class SectionQuery(graphene.ObjectType):
    all_sections = graphene.List(SectionType)
    section = graphene.Field(
        SectionType,
        id=graphene.ID(required=True)
    )

    def resolve_all_sections(root, info):
        return Section.objects.all()

    def resolve_section(root, info, id):
        return Section.objects.get(pk=id)


class SectionMutation(graphene.ObjectType):
    create_section = CreateSection.Field()
    update_section = UpdateSection.Field()
    delete_section = DeleteSection.Field()
