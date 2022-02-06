Look at this xD

```json
{
  "databases": {
    "DATABASE_NAME_1": {
      "tables": {
        "TABLE_NAME_1": {
          "table_constrains": {
            "COLUMN_NAME_1": "DATATYPE_1",
            "COLUMN_NAME_2": "DATATYPE_2",
            "COLUMN_NAME_N": "DATATYPE_N"
          },
          "read_list": null,
          "index_constrains": [["COLUMN_NAME_1"], ["COLUMN_NAME_1", "COLUMN_NAME_2"]],
          "primary_key": "COLUMN_NAME_1",
          "foreign_key": null
        },
        "TABLE_NAME_1": {
          "table_constrains": {
            "COLUMN_NAME_1": "DATATYPE_1",
            "COLUMN_NAME_2": "DATATYPE_2",
            "COLUMN_NAME_N": "DATATYPE_N"
          },
          "read_list": null,
          "index_constrains": [["COLUMN_NAME_2"]],
          "primary_key": "COLUMN_NAME_1",
          "foreign_key": [
            {
              "constraint_name": "FOREIGN_KEY_NAME",
              "foreign_table_name": "TABLE_NAME_1",
              "parent_attribute": ["COLUMN_NAME_1"],
              "child_attribute": ["COLUMN_NAME_1"]
            }
          ]
        }
      }
    }
  },
  "procedures": [
    {
      "procedure_name": "PROCEDURE_NAME",
      "procedure_parameters": ["IN PARAMETER_1 DATATYPE_1"],
      "procedures": "PROCEDURE_QUERY"
    },
    {
      "procedure_name": "PROCEDURE_NAME",
      "procedure_parameters": ["IN PARAMETER_1 DATATYPE_1"],
      "procedures": "PROCEDURE_QUERY"
    }
  ],
  "triggers": [
    {
      "trigger_name": "TRIGGER_NAME",
      "trigger_time": "TRIGGER TIME",
      "database_name": "DATABASE_NAME_1",
      "table_name": "TABLE_NAME_1",
      "queries": ["QUERY_1", "QUERY_2"]
    },
    {
      "trigger_name": "TRIGGER_NAME",
      "trigger_time": "TRIGGER TIME",
      "database_name": "DATABASE_NAME_1",
      "table_name": "TABLE_NAME_1",
      "queries": ["QUERY_1", "QUERY_2"]
    }
  ]
}
```
