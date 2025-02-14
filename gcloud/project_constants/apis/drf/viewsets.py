# -*- coding: utf-8 -*-
"""
Tencent is pleased to support the open source community by making 蓝鲸智云PaaS平台社区版 (BlueKing PaaS Community
Edition) available.
Copyright (C) 2017-2021 THL A29 Limited, a Tencent company. All rights reserved.
Licensed under the MIT License (the "License"); you may not use this file except in compliance with the License.
You may obtain a copy of the License at
http://opensource.org/licenses/MIT
Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
specific language governing permissions and limitations under the License.
"""

from rest_framework import permissions, viewsets
from django_filters.rest_framework import DjangoFilterBackend

from gcloud.core.apis.drf.viewsets.utils import ApiMixin
from gcloud.project_constants.models import ProjectConstant
from gcloud.project_constants.apis.drf.serializers import ProjectConstantsSerializer
from gcloud.project_constants.apis.drf.permissions import ProjectConstantPermissions


class ProjectConstantsViewSet(ApiMixin, viewsets.ModelViewSet):
    queryset = ProjectConstant.objects.all()
    permission_classes = [permissions.IsAuthenticated, ProjectConstantPermissions]
    serializer_class = ProjectConstantsSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["project_id"]
