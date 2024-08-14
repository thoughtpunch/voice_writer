import graphene
from graphene_django import DjangoObjectType
from voice_writer.models import User


class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = "__all__"


class CreateUser(graphene.Mutation):
    class Arguments:
        email = graphene.String(required=True)
        first_name = graphene.String(required=True)
        middle_name = graphene.String()
        last_name = graphene.String(required=True)
        password = graphene.String(required=True)
        is_active = graphene.Boolean()
        is_staff = graphene.Boolean()
        is_superuser = graphene.Boolean()

    user = graphene.Field(UserType)

    def mutate(self, info, email, first_name, last_name, password, middle_name=None, is_active=True, is_staff=False, is_superuser=False):
        user = User(
            email=email,
            first_name=first_name,
            last_name=last_name,
            middle_name=middle_name,
            is_active=is_active,
            is_staff=is_staff,
            is_superuser=is_superuser,
        )
        user.set_password(password)
        user.save()
        return CreateUser(user=user)


class UpdateUser(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        email = graphene.String()
        first_name = graphene.String()
        middle_name = graphene.String()
        last_name = graphene.String()
        password = graphene.String()
        is_active = graphene.Boolean()
        is_staff = graphene.Boolean()
        is_superuser = graphene.Boolean()

    user = graphene.Field(UserType)

    def mutate(self, info, id, email=None, first_name=None, last_name=None, password=None, middle_name=None, is_active=None, is_staff=None, is_superuser=None):
        user = User.objects.get(pk=id)
        if email:
            user.email = email
        if first_name:
            user.first_name = first_name
        if middle_name:
            user.middle_name = middle_name
        if last_name:
            user.last_name = last_name
        if password:
            user.set_password(password)
        if is_active is not None:
            user.is_active = is_active
        if is_staff is not None:
            user.is_staff = is_staff
        if is_superuser is not None:
            user.is_superuser = is_superuser
        user.save()
        return UpdateUser(user=user)


class DeleteUser(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    ok = graphene.Boolean()

    def mutate(self, info, id):
        user = User.objects.get(pk=id)
        user.delete()
        return DeleteUser(ok=True)


class UserQuery(graphene.ObjectType):
    all_users = graphene.List(UserType)
    user = graphene.Field(
        UserType,
        id=graphene.ID(required=True),
    )

    def resolve_all_users(root, info):
        return User.objects.all()

    def resolve_user(self, info, id):
        return User.objects.get(pk=id)


class UserMutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    update_user = UpdateUser.Field()
    delete_user = DeleteUser.Field()
