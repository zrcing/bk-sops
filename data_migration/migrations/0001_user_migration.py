# -*- coding: utf-8 -*-
"""
Tencent is pleased to support the open source community by making 蓝鲸智云PaaS平台社区版 (BlueKing PaaS Community
Edition) available.
Copyright (C) 2017-2019 THL A29 Limited, a Tencent company. All rights reserved.
Licensed under the MIT License (the "License"); you may not use this file except in compliance with the License.
You may obtain a copy of the License at
http://opensource.org/licenses/MIT
Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
specific language governing permissions and limitations under the License.
"""
# Generated by Django 1.11.2 on 2018-10-16 09:55


from django.db import migrations, connection, transaction
from data_migration.conf import settings

from data_migration.utils import dictfetchall, old_uer_table_exist

additional_key = settings.USER_ADDITIONAL_PROPERTY
fields_map = settings.USER_FIELDS_MAP


def reverse_func(apps, schema_editor):
    if not old_uer_table_exist():
        return

    User = apps.get_model('account', 'User')
    UserProperty = apps.get_model('account', 'UserProperty')

    db_alias = schema_editor.connection.alias
    with transaction.atomic():
        UserProperty.objects.using(db_alias).all().delete()
        User.objects.using(db_alias).all().delete()


def forward_func(apps, schema_editor):
    if not old_uer_table_exist():
        return

    User = apps.get_model('account', 'User')
    UserProperty = apps.get_model('account', 'UserProperty')

    db_alias = schema_editor.connection.alias
    with connection.cursor() as cursor:
        cursor.execute('select * from %s'
                       % getattr(settings, 'USER_TABLE', 'account_bkuser'))
        bk_users = dictfetchall(cursor)
        cursor.execute('select * from %s'
                       % getattr(settings, 'USER_GROUP_TABLE', 'account_bkuser_groups'))
        groups = dictfetchall(cursor)
        cursor.execute('select * from %s'
                       % getattr(settings, 'USER_PERMISSION_TABLE', 'account_bkuser_user_permissions'))
        permissions = dictfetchall(cursor)

    users = []
    user_properties = []

    for row in bk_users:

        try:
            user = User.objects.using(db_alias).get(username=row['username'])
        except Exception:
            user = User(
                id=row[fields_map['id']],
                username=row[fields_map['username']],
                nickname=row[fields_map['nickname']],
                is_staff=row[fields_map['is_staff']],
                is_active=True,
                is_superuser=row[fields_map['is_superuser']],
                date_joined=row[fields_map['date_joined']]
            )
            users.append(user)

        for key in additional_key:
            user_properties.append(
                UserProperty(
                    user=user,
                    key=key,
                    value=row[key] or ''
                )
            )

    group_values = []
    for row in groups:
        group_values.append('(%s, %s, %s)' % (row['id'], row['bkuser_id'], row['group_id']))

    permission_values = []
    for row in permissions:
        permission_values.append('(%s, %s, %s)' % (row['id'], row['bkuser_id'], row['permission_id']))

    with transaction.atomic():
        User.objects.bulk_create(users)
        UserProperty.objects.bulk_create(user_properties)
        with connection.cursor() as cursor:
            if group_values:
                cursor.execute('insert into `account_user_groups` (id, user_id, group_id) values %s;' %
                               ','.join(group_values))
            if permission_values:
                cursor.execute('insert into `account_user_permissions` (id, user_id, permission_id) values %s;' %
                               ','.join(permission_values))


class Migration(migrations.Migration):
    operations = [
        migrations.RunPython(forward_func, reverse_func)
    ]
