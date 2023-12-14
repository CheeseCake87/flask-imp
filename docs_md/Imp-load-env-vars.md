```
Menu = Imp/Load Env Variables
Title = Load Enviroment Variables into the Config File
```

`<>` markers can be used to find variables set in the environment. For example:

**File: `default.config.toml`**
```toml
[FLASK]
# ...

ERROR_404_HELP = true
SERVER_NAME = "<FLASK_SERVER_NAME>"
APPLICATION_ROOT = "/"

# ...
```

`<FLASK_SERVER_NAME>` will be replaced by the value of `FLASK_SERVER_NAME`

**Development `.env`**
```text
FLASK_SERVER_NAME=localhost:5000
```

**Production `.env`**
```text
FLASK_SERVER_NAME=mysite.com
```
