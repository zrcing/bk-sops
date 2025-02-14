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

from django.shortcuts import render

from gcloud.contrib.appmaker.models import AppMaker
from gcloud.contrib.appmaker.decorators import check_db_object_exists
from gcloud.core.signals import user_enter


@check_db_object_exists("AppMaker")
def task_home(request, app_id, project_id):
    """
    @summary 通过appmaker创建任务
    @param request:
    @param app_id:
    @param project_id:
    @return:
    """
    app_maker = AppMaker.objects.get(pk=app_id, project_id=project_id)

    ctx = {
        "view_mode": "appmaker",
        "app_id": app_id,
        "template_id": app_maker.task_template.pk,
    }
    user_enter.send(username=request.user.username, sender=request.user.username)
    return render(request, "core/base_vue.html", ctx)


@check_db_object_exists("AppMaker")
def newtask_selectnode(request, app_id, project_id):
    """
    @summary 通过appmaker创建任务
    @param request:
    @param app_id:
    @param project_id:
    @return:
    """
    context = {
        # 等于app的时候是在标准运维打开的
        "view_mode": "appmaker",
        "app_id": app_id,
    }
    user_enter.send(username=request.user.username, sender=request.user.username)
    return render(request, "core/base_vue.html", context)


@check_db_object_exists("AppMaker")
def newtask_paramfill(request, app_id, project_id):
    """
    @summary 通过appmaker创建任务
    @param request:
    @param app_id:
    @param project_id:
    @return:
    """
    context = {
        # 等于app的时候是在标准运维打开的
        "view_mode": "appmaker",
        "app_id": app_id,
    }
    user_enter.send(username=request.user.username, sender=request.user.username)
    return render(request, "core/base_vue.html", context)


@check_db_object_exists("AppMaker")
def execute(request, app_id, project_id):
    """
    @summary: 在轻应用中查看任务详情
    @param request:
    @param app_id:
    @param project_id:
    @return:
    """
    context = {
        "view_mode": "appmaker",
        "app_id": app_id,
    }
    user_enter.send(username=request.user.username, sender=request.user.username)
    return render(request, "core/base_vue.html", context)
