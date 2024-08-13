import graphene
from graphene_django import DjangoObjectType
from voice_writer.models import Document


class DocumentType(DjangoObjectType):
    class Meta:
        model = Document
        fields = "__all__"


class CreateDocument(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        order = graphene.Int(required=True)
        content = graphene.String()
        content_json = graphene.JSONString()
        metadata = graphene.JSONString()
        manuscript_id = graphene.ID(required=True)
        section_id = graphene.ID(required=True)

    document = graphene.Field(DocumentType)

    def mutate(self, info, title, order, manuscript_id, section_id, content=None, content_json=None, metadata=None):
        document = Document(
            title=title,
            order=order,
            manuscript_id=manuscript_id,
            section_id=section_id,
            content=content,
            content_json=content_json,
            metadata=metadata,
        )
        document.save()
        return CreateDocument(document=document)


class UpdateDocument(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        title = graphene.String()
        order = graphene.Int()
        content = graphene.String()
        content_json = graphene.JSONString()
        metadata = graphene.JSONString()

    document = graphene.Field(DocumentType)

    def mutate(self, info, id, title=None, order=None, content=None, content_json=None, metadata=None):
        document = Document.objects.get(pk=id)
        if title:
            document.title = title
        if order is not None:
            document.order = order
        if content:
            document.content = content
        if content_json is not None:
            document.content_json = content_json
        if metadata is not None:
            document.metadata = metadata
        document.save()
        return UpdateDocument(document=document)


class DeleteDocument(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    ok = graphene.Boolean()

    def mutate(self, info, id):
        document = Document.objects.get(pk=id)
        document.delete()
        return DeleteDocument(ok=True)


class DocumentQuery(graphene.ObjectType):
    all_documents = graphene.List(DocumentType)

    def resolve_all_documents(root, info):
        return Document.objects.all()


class DocumentMutation(graphene.ObjectType):
    create_document = CreateDocument.Field
