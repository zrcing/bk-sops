### Request Address

/v2/sops/get_common_template_list/

### Request Method

GET

### Functional description

Query common flow templates list

### Request Parameters

#### General Parameters

|   Field         |  Type       | Required |  Description    |
|-----------------|-------------|---------|------------------|
|   bk_app_code   |   string    |   YES    |  APP ID |
|   bk_app_secret |   string    |   YES    |  APP Secret(APP TOKEN), which can be got via BlueKing Developer Center -> Click APP ID -> Basic Info |
|   bk_token      |   string    |   NO     |  Current user login token, bk_token or bk_username must be valid, bk_token can be got by Cookie      |
|   bk_username   |   string    |   NO     |  Current user username, APP in the white list, can use this field to specify the current user        |

#### Interface Parameters

None

### Request Parameters Example

```
{
    "bk_app_code": "esb_test",
    "bk_app_secret": "xxx",
    "bk_token": "xxx",
    "bk_username": "xxx",
}
```

### Return Result Example

```
{
    "data": [
        {
            "category": "Other",
            "name": "flow2",
            "creator": "admin",
            "edit_time": "2019-07-15 15:13:22 +0800",
            "create_time": "2019-07-15 15:13:22 +0800",
            "editor": "admin",
            "id": 10014,
            "auth_actions": [
                "common_flow_create_task",
                "common_flow_edit",
                "common_flow_delete",
                "common_flow_view",
                "common_flow_create",
                "common_flow_create_periodic_task"
            ]
        },
        {
            "category": "Other",
            "name": "flow1",
            "creator": "admin",
            "edit_time": "2019-07-15 15:13:22 +0800",
            "create_time": "2019-07-15 15:13:22 +0800",
            "editor": "admin",
            "id": 10013,
            "auth_actions": [
                "common_flow_create_task",
                "common_flow_edit",
                "common_flow_delete",
                "common_flow_view",
                "common_flow_create",
                "common_flow_create_periodic_task"
            ]
        },
    ],
    "result": true,
    "request_id": "xxx",
    "trace_id": "xxx"
}
```

### Return Result Description

| Field      | Type      | Description      |
|-----------|----------|-----------|
|  result   |    bool    |      true or false, indicate success or failure                      |
|  data     |    dict    |      data returned when result is true, details are described below  |
|  message  |    string  |      error message returned when result is false                     |
|  request_id     |    string  | esb request id             |
|  trace_id     |    string  | open telemetry trace_id        |
|  auth_actions      |    array   |      actions with permissions for the current user   |

#### data

| Field      | Type      | Description      |
|-----------|----------|-----------|
|  id            |    int       |      flow template ID             |
|  name          |    string    |      flow template name            |
|  category      |    string    |      flow template type，the value is described below    |
|  creator       |    string    |      person who created this flow template      |
|  create_time   |    string    |      datetime when this flow template created   |
|  editor        |    string or null | person who edited this flow template last |
|  edit_time     |    string    |      datetime when this flow template edited          |

#### data.category

| Value        | Description     |
|--------------|----------|
| OpsTools     | operation tools  |
| MonitorAlarm | monitor alarm  |
| ConfManage   | configuration management  |
| DevTools     | development tools  |
| EnterpriseIT | enterprise IT   |
| OfficeApp    | official APPs  |
| Other        | other     |
