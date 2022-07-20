# APIS RDF DEVOPS (working but still experimental)

## how to set up locally

### pre-requisites

* Have a local mysql server installed, ideally version 5.7, since this is what production uses (a persistence image might be integrated here in the future)

* Create a database and a user for your project, e.g. 

```
CREATE DATABASE apis_rdf_test_db;
CREATE USER 'apis_rdf_test_user'@'localhost' IDENTIFIED BY 'apis_rdf_test_password';
GRANT ALL PRIVILEGES ON apis_rdf_test_db.* TO 'apis_rdf_test_user'@'localhost';
FLUSH PRIVILEGES;
```

### setup

clone repo and recursively all its submodules, go into it:

```
git clone --recurse-submodules git@gitlab.com:acdh-oeaw/apis/apis-rdf-devops.git
cd apis-rdf-devops/
```

the ontology to be used must be symlinked into the repo root, for example like this:
```
rm apis_ontology # delete hard-wired placeholder
ln -s apis-ontologies/jelinek/ apis_ontology
```

Append at the end of file `apis_ontology/settings/server_settings.py` your db credentials (WARNING: Take care to not commit them), 
for example:
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'apis_rdf_test_db',
        'USER': 'apis_rdf_test_user',
        'PASSWORD': 'apis_rdf_test_password',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

From here onwards, there are two ways to set up the python environment:
* **a.) with a docker dev container in VS Code**
* **b.) with a python virtual environment via `pipenv`  (and arbitrary IDE utilizing this environment)**

## a.) dev container in VS Code
For developing in vscode you can use the [Remote Container Plugin](https://code.visualstudio.com/docs/remote/containers).
The plugin basically needs three settings files, all of which need to placed in a `.devcontainer` folder in the root directory:
- a Dockerfile holding the definition of the container for the app
- a `docker-compose.yml` file for orchestrating the app container in conjunction with the other containers needed (e.g. a database for local development)
- and a `devcontainer.json` holding the settings for the devcontainer: that includes things like forwarded ports, post-create and post-start commands and environment variables

If a `.devcontainer` folder with the needed files is checked in the repository and you have installed the remote container plugin in your vscode installation vscode will ask you on opening of the repository if you want to reopen it in the container. If you click on "reopen in container" vscode will pull the needed images and start the containers.
Big advantage of using remote containers is that all developers have exactly the same setup and via docker containers you can achieve a real separation of environments (something that is not possible with virtual environments only).

#### the docker-compose.yml in apis-rdf-devops
The `docker-compose.yml` file in apis-rdf-devops includes a service called tunnel:

```dockerfile
  tunnel:
    image: cagataygurturk/docker-ssh-tunnel:0.0.1
    volumes:
      - $HOME/.ssh:/root/ssh:ro
    environment:
      TUNNEL_HOST: apis-tunnel
      REMOTE_HOST: helios.arz.oeaw.ac.at
      LOCAL_PORT: 3308
      REMOTE_PORT: 3306
    network_mode: service:db
```
It uses a cofiguration stored in a file called `config` in the directory `$HOME/.ssh:/root/ssh:ro` (you need to change the path to wherever your config is stored). 
The config file basically sets the options for the ssh tunnel:
```
Host apis-tunnel # You can use any name
        HostName sisyphos.arz.oeaw.ac.at 
        IdentityFile ~/.ssh/id_rsa
        User apis
        ForwardAgent yes
        TCPKeepAlive yes
        ConnectTimeout 5
        ServerAliveCountMax 10
        ServerAliveInterval 15
```
The tunnel host set in the above config needs to be the name set in the environment variables in the docker-compose service. Additionally you can set with environment variables in the docker-compose-service:
- `REMOTE_HOST`: this is the remote host we tunnel to. In our case its `helios.arz.oeaw.ac.at` to make the remote (production) db accessible in the local container
- `LOCAL_PORT`: the local port to use for the tunnel. As we are using the same network as the db service we cant use 3306 as that port is already used by the local db. We therefore use 3308

With these settings in place you can access dbs on helios under host `db` and port `3308`. Therefore something like `mysql://jelinek:PASSWORD@db:3308/jelinek` should work.


## b.) pipenv

At the repo's root, set up your environment, and activate it:
```
pipenv install
pipenv shell
```

## django setup (after setup a. or b.)

Either within your dev container or virtual python environment, run the `manage.py` at the project's root with the corresponding settings from the ontology module, like so:
```
python manage.py version --settings=apis_ontology.settings.server_settings
```

If a fresh DB was set up, then it needs to be migrated:
```
python manage.py migrate --settings=apis_ontology.settings.server_settings
```

Start a django shell:
```
python manage.py shell --settings=apis_ontology.settings.server_settings
```
Create test admin user within shell:
```
from django.contrib.auth.models import User
User.objects.create_superuser('test_admin', None, 'test_password')
```

Relationships between entities, along with their labels, are defined in
`construct_properties()` in an individual ontology's `models.py` file.
To initially create them in the database and to update/replace them later on,
the function has to be called explicitly.

The following management command does this for you and, on success,
prints out the relationship labels (or "properties") which were created:

```shell
$ python manage.py create_relationships --settings=apis_ontology.settings.server_settings
```
Note: the above workflow for handling relationships is a workaround
since properties are currently not defined as separate classes but instances
as a result of a complicated trade-off.


Run server:
```
python manage.py runserver --settings=apis_ontology.settings.server_settings
```

## ontology specific scripts

Projects occasionally need some processing logic only within the project scope. In order to avoid cluttering the main code base, project specific scripts can be run, by placing them in a subfolder `ontology_specific_scripts` in the respective ontology folder. For example the jelinek project has a script under path `apis_ontology/ontology_specific_scripts/import_tei.py`, this can be run like so:
```
python manage.py run_ontology_script import_tei --settings=apis_ontology.settings.server_settings
```
