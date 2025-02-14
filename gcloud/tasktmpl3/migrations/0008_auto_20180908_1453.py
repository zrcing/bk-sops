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



from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tasktmpl3', '0006_auto_20180908_1447'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tasktemplate',
            name='pipeline_template',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to_field='template_id', blank=True, to='pipeline.PipelineTemplate', null=True),
        ),
    ]
