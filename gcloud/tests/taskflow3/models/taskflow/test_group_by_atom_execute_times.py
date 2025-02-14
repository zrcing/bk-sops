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

from gcloud.tests.mock_settings import TASKFLOWEXECUTEDNODE_STATISTICS_FILTER
from gcloud.tests.mock import mock, MagicMock
from gcloud.taskflow3.models import TaskFlowInstance

MOCK_COMP_TOTAL = "gcloud.taskflow3.models.ComponentModel.objects.count"
MOCK_COMP_VALUES_LIST = "gcloud.taskflow3.models.ComponentModel.objects.values_list"


class MockCompoentData(MagicMock):
    def annotate(self, *args, **kwargs):
        return [
            {"component_code": "code1", "version": "1.0", "is_remote": False, "value": 1},
            {"component_code": "code2", "version": "1.0", "is_remote": True, "value": 1},
        ]

    def values(self, *args, **kwargs):
        return self


class MockTaskFlow(MagicMock):
    def values_list(self, *args, **kwargs):
        return [1, 2]


TEST_TOTAL = 2
TEST_COMP_NAME = (("code1", "group-name1"), ("code2", "name2"))

TEST_GROUPS = [
    {"code": "code1", "name": "组-name1-1.0", "value": 1},
    {"code": "code2", "name": "第三方插件-code2-1.0", "value": 1},
]


class TestAtomExecuteTimes(TestCase):
    def test_success(self):
        with mock.patch(MOCK_COMP_TOTAL, MagicMock(return_value=TEST_TOTAL)) as mock_total:
            with mock.patch(MOCK_COMP_VALUES_LIST, MagicMock(return_value=TEST_COMP_NAME)) as mock_dict:
                with mock.patch(
                    TASKFLOWEXECUTEDNODE_STATISTICS_FILTER, MagicMock(return_value=MockCompoentData())
                ) as mock_comp_data:
                    total, groups = TaskFlowInstance.objects.group_by_atom_execute_times(MockTaskFlow())
                    mock_total.assert_called_once_with()
                    mock_dict.assert_called_once_with("code", "name")
                    mock_comp_data.assert_called_once_with(task_instance_id__in=[1, 2])
                    self.assertEqual(total, TEST_TOTAL)
                    self.assertEqual(groups, TEST_GROUPS)
