from django.contrib.auth.models import User
from django.db.models import OuterRef, Subquery
from django.http import Http404
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from guardian.shortcuts import assign_perm, get_objects_for_user
from guardian.utils import get_40x_or_None
from rest_framework import filters, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from rest_framework.viewsets import ReadOnlyModelViewSet

from dandiapi.api.models import Dandiset, Version, VersionMetadata
from dandiapi.api.views.common import DandiPagination
from dandiapi.api.views.serializers import (
    DandisetSerializer,
    UserSerializer,
    VersionMetadataSerializer,
)


class DandisetFilterBackend(filters.OrderingFilter):
    ordering_fields = ['created', 'name']
    ordering_description = (
        'Which field to use when ordering the results. '
        'Options are created, -created, name, and -name.'
    )

    def filter_queryset(self, request, queryset, view):
        orderings = self.get_ordering(request, queryset, view)
        if orderings:
            ordering = orderings[0]
            # ordering can be either 'created' or '-created', so test for both
            if ordering[-7:] == 'created':
                return queryset.order_by(ordering)
            elif ordering[-4:] == 'name':
                # name refers to the name of the most recent version, so a subquery is required
                latest_version = Version.objects.filter(dandiset=OuterRef('pk')).order_by(
                    '-created'
                )[:1]
                queryset = queryset.annotate(name=Subquery(latest_version.values('metadata__name')))
                return queryset.order_by(ordering)

        return queryset


class DandisetViewSet(ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = DandisetSerializer
    pagination_class = DandiPagination
    filter_backends = [DandisetFilterBackend]

    lookup_value_regex = Dandiset.IDENTIFIER_REGEX
    # This is to maintain consistency with the auto-generated names shown in swagger.
    lookup_url_kwarg = 'dandiset__pk'

    def get_queryset(self):
        # TODO: This will filter the dandisets list if there is a query parameter user=me.
        # This is not a great solution but it is needed for the My Dandisets page.
        queryset = Dandiset.objects.all().order_by('created')
        user_kwarg = self.request.query_params.get('user', None)
        if user_kwarg == 'me':
            return get_objects_for_user(self.request.user, 'owner', queryset, with_superuser=False)
        return queryset

    def get_object(self):
        # Alternative to path converters, which DRF doesn't support
        # https://docs.djangoproject.com/en/3.0/topics/http/urls/#registering-custom-path-converters

        lookup_url = self.kwargs[self.lookup_url_kwarg]
        try:
            lookup_value = int(lookup_url)
        except ValueError:
            raise Http404('Not a valid identifier.')
        self.kwargs[self.lookup_url_kwarg] = lookup_value

        return super().get_object()

    @swagger_auto_schema(
        request_body=VersionMetadataSerializer(),
        responses={200: DandisetSerializer()},
    )
    def create(self, request):
        serializer = VersionMetadataSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        version_metadata, created = VersionMetadata.objects.get_or_create(
            name=serializer.validated_data['name'],
            metadata=serializer.validated_data['metadata'],
        )
        if created:
            version_metadata.save()

        dandiset = Dandiset()
        dandiset.save()
        assign_perm('owner', request.user, dandiset)
        version = Version(dandiset=dandiset, metadata=version_metadata, version='draft')
        version.save()

        serializer = DandisetSerializer(instance=dandiset)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(method='GET', responses={200: UserSerializer(many=True)})
    @swagger_auto_schema(
        method='PUT',
        request_body=UserSerializer(many=True),
        responses={
            200: UserSerializer(many=True),
            400: 'User not found, or cannot remove all owners',
        },
    )
    # TODO move these into a viewset
    @action(methods=['GET', 'PUT'], detail=True)
    def users(self, request, dandiset__pk):
        dandiset = get_object_or_404(Dandiset, pk=dandiset__pk)
        if request.method == 'PUT':
            # Verify that the user is currently an owner
            response = get_40x_or_None(request, ['owner'], dandiset, return_403=True)
            if response:
                return response

            serializer = UserSerializer(data=request.data, many=True)
            serializer.is_valid(raise_exception=True)

            def get_user_or_400(username):
                try:
                    return User.objects.get(username=username)
                except User.DoesNotExist:
                    raise ValidationError(f'User {username} not found')

            owners = [
                get_user_or_400(username=owner['username']) for owner in serializer.validated_data
            ]
            if len(owners) < 1:
                raise ValidationError('Cannot remove all draft owners')

            dandiset.set_owners(owners)
            dandiset.save()
        serializer = UserSerializer(dandiset.owners, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
