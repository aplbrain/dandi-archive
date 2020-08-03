from django.contrib.auth.models import User
import factory.django

from dandi.publish.models import Asset, Dandiset, Version


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker('user_name')
    email = factory.Faker('safe_email')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')


class DandisetFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Dandiset

    draft_folder_id = factory.Faker('hexify', text='^' * 24)


class VersionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Version

    dandiset = factory.SubFactory(DandisetFactory)
    metadata = factory.Faker('pydict', value_types=['str', 'float', 'int'])
    name = factory.Faker('sentence')
    description = factory.Faker('paragraph')


class AssetFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Asset

    version = factory.SubFactory(VersionFactory)
    path = factory.Faker('file_path', extension='nwb')
    # size = factory.LazyAttribute(lambda asset: asset.blob.size)
    size = factory.SelfAttribute('blob.size')
    # TODO: This sha256 is technically invalid for the blob
    sha256 = factory.Faker('hexify', text='^' * 64)
    metadata = factory.Faker('pydict', value_types=['str', 'float', 'int'])
    blob = factory.django.FileField(data=b'somefilebytes')