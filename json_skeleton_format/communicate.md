###BARE MINIMUM FOR THE JSON FORMAT(A GENERAL FORMAT)

```json
{
    "HEADER"    :   {
        "DATABASE"          : "",
        "TABLE_NAME"        : "",
        "REQUEST_TYPE"      : ""
    },
    "DATA"    :   {
        "FIELDS"    : {}(OR)[],
        "SET"       : {},
        "WHERE"     : {}
    },
    "FOOTER"    :   {
        "DATA ABOUT THE REQUEST"  : "",
        "COMMENT"   : "",
        "UPDATE"    : null,
        "DEP"       : null
    }
}
```

###FOR A SELECT STATEMENT

```json
{
  "HEADER": {
    "DATABASE": "",
    "TABLE_NAME": "",
    "REQUEST_TYPE": ""
  },
  "DATA": {
    "FIELDS": [],
    "SET": null,
    "WHERE": {}
  },
  "FOOTER": {
    "DATA ABOUT THE REQUEST": "",
    "COMMENT": "",
    "UPDATE": null,
    "DEP": null
  }
}
```

###FOR AN INSERT STATEMENT

```json
{
  "HEADER": {
    "DATABASE": "",
    "TABLE_NAME": "",
    "REQUEST_TYPE": ""
  },
  "DATA": {
    "FIELDS": {},
    "SET": null,
    "WHERE": null
  },
  "FOOTER": {
    "DATA ABOUT THE REQUEST": "",
    "COMMENT": "",
    "UPDATE": null,
    "DEP": null
  }
}
```

###FOR AN UPDATE STATEMENT

```json
{
  "HEADER": {
    "DATABASE": "",
    "TABLE_NAME": "",
    "REQUEST_TYPE": ""
  },
  "DATA": {
    "FIELDS": null,
    "SET": {},
    "WHERE": {}
  },
  "FOOTER": {
    "DATA ABOUT THE REQUEST": "",
    "COMMENT": "",
    "UPDATE": null,
    "DEP": null
  }
}
```

###FOR A DELETE STATEMENT -- HAS NOT BEEN IMPLEMENTED YET, WILL BE IN THE LATER VERSION OF THE THE APP

```json
{
  "HEADER": {
    "DATABASE": "",
    "TABLE_NAME": "",
    "REQUEST_TYPE": ""
  },
  "DATA": {
    "FIELDS": null,
    "SET": null,
    "WHERE": {}
  },
  "FOOTER": {
    "DATA ABOUT THE REQUEST": "",
    "COMMENT": "",
    "UPDATE": null,
    "DEP": null
  }
}
```

###FOR A ALTER STATEMENT -- HAS NOT BEEN DEFINED YET(PROBABLY WILL NEVER BE DEFINED AS THERE NEVER MIGHT BE A USE FOR IT)
