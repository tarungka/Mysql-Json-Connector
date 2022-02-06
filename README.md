# **Mysql-Json-Connector**

---

## An application to perform CRUD operations on MySQL using a JSON object

### **Developers** : **[Tarun Gopalkrishna A](https://github.com/Kinngman05)**

## **Requirements and Installations**

#### **Database:**

- [**MySQL 5.7**](https://www.digitalocean.com/community/tutorials/how-to-install-mysql-on-ubuntu-18-04)
  ```bash
  sudo apt install mysql-server
  ```

#### **Interpreter:**

- **python3**

#### **Dependencies:**

- [**mysql-connector**](https://pypi.org/project/mysql-connector-python/)
  ```bash
  pip3 install mysql-connector-python
  ```
- [**Flask-SocketIO**](https://flask-socketio.readthedocs.io/en/latest/)
  ```bash
  pip3 install Flask-SocketIO
  ```

#### **Working:**

###### **To connect to the database:**

Firstly, create a separate `user` for the `mysql-connector`(recommended for security and safety purposes)

> Note: Please ensure to give correct permissions to the `user` AND DO NOT USE THE 'root' users account.

In the `.config` directory create a file called `mysql.cnf` with at least the entry of minimum details to connect to the `mysql` server.

> For more details on the same check: [Creating and Configuring the my.cnf File for Red Hat Enterprise Linux Machines](https://www.ibm.com/support/knowledgecenter/en/SSYQ72_10.0.2/com.ibm.help.suiteinstall10026.databaseconfig.doc/t_CreatingandConfiguringthemy.cnffileforRedhatEnterpriseLinuxMachines.html)
> P.S: If you're on windows refer the next page in the link.

###### **To create a database:**

In the `.config` directory create a `database.json` file in the following format:

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
          "primary_key": ["COLUMN_NAME_1"],
          "foreign_key": null,
          "initial_data": [
            {
              "COLUMN_NAME_1": "VALUE_1",
              "COLUMN_NAME_2": "VALUE_2",
              "COLUMN_NAME_N": "VALUE_N"
            }
          ]
        },
        "TABLE_NAME_2": {
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
          ],
          "initial_data": null
        }
      }
    }
  },
  "procedures": [
    {
      "procedure_name": "PROCEDURE_NAME",
      "procedure_parameters": ["IN PARAMETER_1 DATATYPE_1"],
      "procedures": ["PROCEDURE_QUERY_1", "PROCEDURE_QUERY_2", "PROCEDURE_QUERY_N"]
    },
    {
      "procedure_name": "PROCEDURE_NAME",
      "procedure_parameters": ["IN PARAMETER_1 DATATYPE_1"],
      "procedures": ["PROCEDURE_QUERY_1", "PROCEDURE_QUERY_2", "PROCEDURE_QUERY_N"]
    }
  ],
  "triggers": [
    {
      "trigger_name": "TRIGGER_NAME",
      "trigger_time": "TRIGGER_TIME",
      "database_name": "DATABASE_NAME_1",
      "table_name": "TABLE_NAME_1",
      "queries": ["QUERY_1", "QUERY_2"]
    },
    {
      "trigger_name": "TRIGGER_NAME",
      "trigger_time": "TRIGGER_TIME",
      "database_name": "DATABASE_NAME_1",
      "table_name": "TABLE_NAME_1",
      "queries": ["QUERY_1", "QUERY_2"]
    }
  ],
  "initial_data": null,
  "views": [
    {
      "name": "VIEW_NAME",
      "query": "QUERY_STRING_TO_MAKE_VIEW"
    }
  ]
}
```

##### An example database:

The following has _1 database_,_3 tables_,_2 procedures_,_2 triggers_.

```json
{
  "databases": {
    "test_db": {
      "tables": {
        "students": {
          "table_constrains": {
            "name": "VARCHAR(60) NOT NULL",
            "id": "CHAR(10) NOT NULL",
            "team_name": "VARCHAR(30) NOT NULL",
            "login_status": "ENUM('YES','NO') NOT NULL DEFAULT 'NO'"
          },
          "read_list": null,
          "index_constrains": [["id"], ["id", "name"]],
          "primary_key": ["id"],
          "foreign_key": null,
          "initial_data": [
            {
              "name": "John Maverik",
              "id": "0123456789",
              "team_name": "Cool kids",
              "login_status": "NO"
            }
          ]
        },
        "teams": {
          "table_constrains": {
            "team_hash": "CHAR(10) NOT NULL",
            "team_name": "VARCHAR(30) NOT NULL",
            "team_lead": "CHAR(10) NOT NULL"
          },
          "read_list": null,
          "index_constrains": [["team_hash"]],
          "primary_key": "team_hash",
          "foreign_key": [
            {
              "constraint_name": "foreign_key_name",
              "foreign_table_name": "students",
              "parent_attribute": ["id"],
              "child_attribute": ["team_lead"]
            }
          ],
          "initial_data": null
        },
        "attendance": {
          "table_constrains": {
            "id": "CHAR(10) NOT NULL",
            "team_hash": "CHAR(6) NOT NULL ",
            "time_in": "DATETIME NOT NULL DEFAULT NOW()",
            "time_out": "DATETIME DEFAULT NULL",
            "time_spent": "TIME DEFAULT NULL"
          },
          "read_list": null,
          "index_constrains": null,
          "primary_key": null,
          "foreign_key": [
            {
              "constraint_name": null,
              "foreign_table_name": "students",
              "parent_attribute": ["id"],
              "child_attribute": ["id"]
            },
            {
              "constraint_name": null,
              "foreign_table_name": "teams",
              "parent_attribute": ["team_hash"],
              "child_attribute": ["team_hash"]
            }
          ],
          "initial_data": null
        }
      }
    }
  },
  "procedures": [
    {
      "procedure_name": "set_login_status_to_True",
      "procedure_parameters": ["IN _id CHAR(10)"],
      "procedures": ["UPDATE students SET login_status=TRUE WHERE id=_id;"]
    },
    {
      "procedure_name": "set_login_status_to_False",
      "procedure_parameters": ["IN _id CHAR(10)"],
      "procedures": ["UPDATE students SET login_status=FALSE WHERE id=_id;"]
    }
  ],
  "triggers": [
    {
      "trigger_name": "attendance_AFTER_INSERT",
      "trigger_time": "AFTER INSERT",
      "database_name": "test_db",
      "table_name": "attendance",
      "queries": ["CALL set_login_status_to_True(NEW.id);"]
    },
    {
      "trigger_name": "attendance_BEFORE_UPDATE",
      "trigger_time": "BEFORE UPDATE",
      "database_name": "test_db",
      "table_name": "attendance",
      "queries": [
        "IF OLD.time_spent IS NULL THEN SET NEW.time_spent=TIMEDIFF(NEW.time_out,OLD.time_in); END IF;",
        "CALL set_login_status_to_False(NEW.id);"
      ]
    }
  ],
  "initial_data": null,
  "views": [
    {
      "name": "final_table",
      "query": "SELECT name,id,login_status,team_hash,student.team_name,team_lead FROM student,teams WHERE student.team_name=team.team_name"
    }
  ]
}
```

The following are the queries generated and executed by the connector when `setup.py` is run:

###### To create the database:

```sql
CREATE DATABASE `test_db`;
```

###### To create the tables:

```sql
--TABLE students
CREATE TABLE students(`name` VARCHAR(60) NOT NULL,`id` CHAR(10) NOT NULL,`team_name` VARCHAR(30) NOT NULL,`login_status` ENUM('YES','NO') NOT NULL DEFAULT 'NO',PRIMARY KEY(id),INDEX(`id`),INDEX(`id`,`name`));
--TABLE teams
CREATE TABLE teams(`team_hash` CHAR(10) NOT NULL,`team_name` VARCHAR(30) NOT NULL,`team_lead` CHAR(10) NOT NULL,PRIMARY KEY(team_hash),CONSTRAINT `foreign_key_name` FOREIGN KEY (`team_lead`) REFERENCES `students` (`id`),INDEX(`team_hash`));
--TABLE attendance
CREATE TABLE attendance(`id` CHAR(10) NOT NULL,`team_hash` CHAR(6) NOT NULL ,`time_in` DATETIME NOT NULL DEFAULT NOW(),`time_out` DATETIME DEFAULT NULL,`time_spent` TIME DEFAULT NULL,FOREIGN KEY (`id`) REFERENCES `students` (`id`),FOREIGN KEY (`team_hash`) REFERENCES `teams` (`team_hash`));
```

###### To create procedures:

```sql
CREATE PROCEDURE `set_login_status_to_True` (IN _id CHAR(10)) BEGIN UPDATE students SET login_status=TRUE WHERE id=_id;END
CREATE PROCEDURE `set_login_status_to_False` (IN _id CHAR(10)) BEGIN UPDATE students SET login_status=FALSE WHERE id=_id;END
```

###### To create triggers:

```sql
CREATE TRIGGER `events_AFTER_INSERT` AFTER INSERT ON `test_db`.`attendance` FOR EACH ROW BEGIN CALL set_login_status_to_True(NEW.id);END
CREATE TRIGGER `attendance_BEFORE_UPDATE` BEFORE UPDATE ON `test_db`.`attendance` FOR EACH ROW BEGIN IF OLD.time_spent IS NULL THEN SET NEW.time_spent=TIMEDIFF(NEW.time_out,OLD.time_in); END IF;CALL set_login_status_to_False(NEW.id);END
```

###### To create view:

```sql
CREATE VIEW final_table AS SELECT name,id,login_status,team_hash,student.team_name,team_lead FROM student,teams WHERE student.team_name=team.team_name;
```

##### To peform `CRUD` operations on the created database:

> Refer the `json_sekelton_config` for the minimum json format needed to peform any opereaion on the database. -- Need to update this!

###### To inserting records into the created database:

```bash
echo "Registering a student"
./database.py '{"HEADER":{"DATABASE":"test_db","TABLE_NAME":"students","REQUEST_TYPE":"insert"},"DATA":{"FIELDS":{"id":"TEST_ID_01","name":"Tester","team_name": "TESTING TEAM"},"SET":null,"WHERE":null},"FOOTER":{"DATA ABOUT THE REQUEST":"reg_stud","COMMENT":"","UPDATE":null,"DEP":null}}'
echo "Registering team"
./database.py '{"HEADER":{"DATABASE":"test_db","TABLE_NAME":"teams","REQUEST_TYPE":"insert"},"DATA":{"FIELDS":{"team_hash":"TST_TM","team_name":"TESTING TEAM","team_lead":"TEST_ID_01"},"SET":null,"WHERE":null},"FOOTER":{"DATA ABOUT THE REQUEST":"reg_team","COMMENT":"","UPDATE":null,"DEP":null}}'
```

When inserting into `attendace` we can set a trigger(i.e `attendance_AFTER_INSERT`) in the intial setup of the database(like we have) or we could use the following format:

```bash
echo "Student login"
./database.py '{"HEADER":{"DATABASE":"test_db","TABLE_NAME":"attendance","REQUEST_TYPE":"insert"},"DATA":{"FIELDS":{"team_hash":"TST_TM","team_name":"TESTING TEAM","id":"TEST_ID_01"},"SET":null,"WHERE":null},"FOOTER":{"DATA ABOUT THE REQUEST":"login","COMMENT":"","UPDATE":[{"HEADER":{"DATABASE":"test_db","TABLE_NAME":"students","REQUEST_TYPE":"update"},"DATA":{"FIELDS":null,"SET":{"login_status":"YES"},"WHERE":{"id":"TEST_ID_01"}},"FOOTER":{"DATA ABOUT THE REQUEST":"login","COMMENT":"","UPDATE":null,"DEP":null}}],"DEP":null}}'
```

> If you are using the trigger then set the "UPDATE" field within the "FOOTER" to null in the outer query.
