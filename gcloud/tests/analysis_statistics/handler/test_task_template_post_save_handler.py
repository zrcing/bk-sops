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

from django.test import TestCase

from gcloud.tests.mock import *  # noqa
from gcloud.tests.mock_settings import *  # noqa
from gcloud.tests.analysis_statistics.mock_settings import *  # noqa
from gcloud.tasktmpl3.models import TaskTemplate


class TestTaskTemplatePostSaveHandler(TestCase):
    def test_task_call_success(self):
        with patch(TASKTEMPLATE_POST_SAVE_STATISTICS_TASK, MagicMock()) as mocked_handler:
            self.tasktemplate = TaskTemplate.objects.create(
                default_flow_type="default_flow_type", executor_proxy="executor_proxy"
            )
            mocked_handler.assert_called_once_with(self.tasktemplate.id)
