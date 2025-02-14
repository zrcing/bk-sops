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

import logging
import traceback

from django.db.models.signals import post_save
from django.dispatch import receiver

from gcloud.core.models import EngineConfig
from gcloud.constants import PROJECT
from gcloud.taskflow3.models import TaskFlowInstance, TimeoutNodeConfig
from gcloud.taskflow3.domains.auto_retry import AutoRetryNodeStrategyCreator
from gcloud.periodictask.models import PeriodicTaskHistory
from gcloud.shortcuts.message import send_periodic_task_message
from pipeline.contrib.periodic_task.models import PeriodicTaskHistory as PipelinePeriodicTaskHistory
from pipeline.contrib.periodic_task.models import PeriodicTask as PipelinePeriodicTask
from pipeline.contrib.periodic_task.signals import pre_periodic_task_start, periodic_task_start_failed

logger = logging.getLogger("celery")


@receiver(pre_periodic_task_start, sender=PipelinePeriodicTask)
def pre_periodic_task_start_handler(sender, periodic_task, pipeline_instance, **kwargs):
    task = TaskFlowInstance.objects.create(
        project_id=periodic_task.extra_info["project_id"],
        pipeline_instance=pipeline_instance,
        category=periodic_task.extra_info["category"],
        template_id=periodic_task.extra_info["template_num_id"],
        template_source=periodic_task.extra_info.get("template_source", PROJECT),
        create_method="periodic",
        create_info=periodic_task.id,
        flow_type="common",
        current_flow="execute_task",
        engine_ver=periodic_task.extra_info.get("engine_ver", EngineConfig.ENGINE_VER_V1),
    )

    # crete auto retry strategy
    arn_creator = AutoRetryNodeStrategyCreator(taskflow_id=task.id, root_pipeline_id=pipeline_instance.instance_id)
    arn_creator.batch_create_strategy(pipeline_instance.execution_data)

    # create timeout config
    TimeoutNodeConfig.objects.batch_create_node_timeout_config(
        taskflow_id=task.id,
        root_pipeline_id=task.pipeline_instance.instance_id,
        pipeline_tree=task.pipeline_instance.execution_data,
    )


@receiver(post_save, sender=PipelinePeriodicTaskHistory)
def periodic_task_history_post_save_handler(sender, instance, created, **kwargs):
    if created:
        PeriodicTaskHistory.objects.record_history(instance)


@receiver(periodic_task_start_failed, sender=PipelinePeriodicTask)
def periodic_task_start_failed_handler(sender, periodic_task, history, **kwargs):
    try:
        send_periodic_task_message(periodic_task, history)
    except Exception:
        logger.error(
            "periodic_task_start_failed_handler[template_id=%s] send message error: %s"
            % (periodic_task.extra_info["template_num_id"], traceback.format_exc())
        )
