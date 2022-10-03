# APIS RDF DEVOPS

Note this project is generally functional but still experimental.

## Prerequisite for local setup

You need to have a local MySQL server installed, ideally version 5.7, since this is what production uses. A persistence image might be integrated here in the future.

Create a database and a user for your project, e.g.:

```mysql
CREATE DATABASE apis_rdf_test_db;
CREATE USER 'apis_rdf_test_user'@'localhost' IDENTIFIED BY 'apis_rdf_test_password';
GRANT ALL PRIVILEGES ON apis_rdf_test_db.* TO 'apis_rdf_test_user'@'localhost';
FLUSH PRIVILEGES;
```

## Setup

### Clone main repository and submodules

This Django project expects other apps it depends on or integrates to be present in the form of Git submodules. These are defined in the `.gitmodules` file in the root of the repository, which facilitates installation of both this superproject and its submodules simultaneously.

To get Git to link the superproject and its submodules together correctly, it is advisable not to deviate from the installation steps outlined below. Even if you previously separately cloned any of the repositories which function as submodules, it is best not to try to manually link them with this repository.

To clone the superproject along with its default submodules, run:

```sh
$ git clone --recurse-submodules git@github.com:acdh-oeaw/apis/apis-rdf-devops.git
```

In case you originally cloned the superproject as simple, standalone repository without submodules, you can still collect them later on. From the project's root, run the following command to have Git clone them:

```sh
$ git submodule update --init --recursive
```

#### Install app-specific submodules

As mentioned, the `.gitmodules` file in the project root contains instructions for how Git should handle submodules. On first run of `git submodule init` or `git submodule update`, these settings are copied to your local clone's `.git/config` file.

Submodules *not relevant to all APIS Ontologies apps* are set to `update = none` in the file, which prevents Git from cloning them. Once this setting is present in your local `.git/config` file, it cannot be overwritten again by execution of the `git submodule init` and `git submodule update` commands. Should you need any of these "disabled" submodules for your specific ontology, you need to manually modify the update strategy in `.git/config` so the line reads `update = checkout`.

After (re)enabling your additional submodules, have Git clone them with:

```sh
$ git submodule update
```

### Symlink relevant APIS Ontologies files

Django expects an app/directory named `apis_ontology` to be present in the project root. `apis_ontology` is effectively a symbolic link to a directory within the [apis-ontologies](../apis-ontologies) repository (= one of this superproject's submodules) which contains all files relevant to one particular APIS Ontologies project/app.

For CI/CD reasons, the `apis_ontology` symlink is already set and being tracked by Git. For local development, you have to change it to point to the directory containing the files relevant to the ontology you work on. If this directory does not exist yet, you will first have to create it, see [Create a new APIS Ontologies application](https://gitlab.com/acdh-oeaw/apis/apis-ontologies#create-a-new-apis-ontologies-application) in the APIS Ontologies README.

Note that you are not supposed to (re)commit the modified symlink. If you do so accidentally, it won't do any real damage but will overwrite other devs' local symlinks when they pull changes.

To link to e.g. the `jelinek` ontology, you would enter  do the use:


```sh
$ cd apis-rdf-devops/
$ rm apis_ontology # delete hard-wired placeholder
$ ln -s apis-ontologies/jelinek/ apis_ontology
```

For how to set up the file for your local database credentials, refer to the [Configure local settings](https://gitlab.com/acdh-oeaw/apis/apis-ontologies#configure-local-settings) section in in the APIS Ontologies README.

Example credentials could look like the following:

```python
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

### Configure Python environment

There are two ways to set up your Python environment:

1. with a [Docker](https://www.docker.com/) dev container in Visual Studio Code
2. with a Python Virtual Environment using [pipenv](https://pipenv.pypa.io/en/latest/) (independent of which IDE you use)


#### Python environment via Docker

A great advantage of using remote containers is that all developers have exactly the same setup. Additionally, working with Docker containers achieves a real separation of environments, which is something that is not possible with virtual environments only.

For developing in VS Code you can use the [Remote Container Plugin](https://code.visualstudio.com/docs/remote/containers). The plugin basically needs three settings files, all of which need to placed in a `.devcontainer` folder in the root directory:

- a Dockerfile holding the definition of the container for the app
- a `docker-compose.yml` file for orchestrating the app container in conjunction with the other containers needed (e.g. a database for local development)
- and a `devcontainer.json` holding settings relevant to the devcontainer itself, e.g. forwarded ports, post-create and post-start commands and environment variables

If a `.devcontainer` folder with the needed files is checked in the repository and you have installed the remote container plugin in your VS Code installation, on opening of the repository, VS Code will ask you if you want to reopen it in the container. If you click on "reopen in container", the IDE will pull the needed images and start the containers.


##### Configure docker-compose.yml

The `docker-compose.yml` file included in the apis-rdf-devops repository includes a service called tunnel:

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

It uses a configuration stored in a file called `config` in the directory `$HOME/.ssh:/root/ssh:ro` (you need to change the path to wherever your config is stored). The config file basically sets the options for the ssh tunnel:

```sh
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

The tunnel host set in the above config needs to be the name set in the environment variables in the docker-compose service. Additionally, you can set with environment variables in the docker-compose-service:

- `REMOTE_HOST` is the remote host we tunnel to. In our case, `helios.arz.oeaw.ac.at` to make the remote (production) database accessible within the local container
- `LOCAL_PORT` is the local port to use for the tunnel. As we are using the same network as the database service, we cannot use 3306 since that port is already used by the local database. We therefore use 3308.

With these settings in place, you can access databases on helios under host `db` and port `3308`. Therefore something like `mysql://jelinek:PASSWORD@db:3308/jelinek` should work.


#### Python Virtual Environment via pipenv

At the repository's root, set up your virtual env and activate it:

```sh
$ pipenv install
$ pipenv shell
```

### Django setup

Once you have configured your Python environment using either solution outlined above, you need to set up Django.

Within either your VS Code dev container or your Python Virtual Environment, run `manage.py` at the project's root using your local settings file, like so:

```sh
$ python manage.py version --settings=apis_ontology.settings.local_settings
```

If a new database was set up, it first needs to be migrated:

```sh
$ python manage.py migrate --settings=apis_ontology.settings.local_settings
```

Next, start a Django shell...

```sh
$ python manage.py shell --settings=apis_ontology.settings.local_settings
```

and create an admin user (make up your own credentials):

```python
from django.contrib.auth.models import User
User.objects.create_superuser('test_admin', None, 'test_password')
```

Relationships between entities, along with their labels, are defined in
`construct_properties()` in an individual ontology's `models.py` file.
To initially create them in the database and to update/replace them later on,
the function has to be called explicitly.

The following management command does this for you and, on success,
prints out the relationship labels (or "properties") which were created:

```sh
$ python manage.py create_relationships --settings=apis_ontology.settings.local_settings
```

Note: the above workflow for handling relationships is a workaround
since properties are currently not defined as separate classes but instances
as a result of a complicated trade-off.


Finally, start the server to:

```sh
$ python manage.py runserver --settings=apis_ontology.settings.local_settings
```

### Ontology-specific scripts

Projects occasionally need some processing logic only within their project scope. In order to avoid cluttering the main code base, project-specific scripts can be put into a sub directory `ontology_specific_scripts` within an individual ontology app.

The Jelinek project, for example, contains a script `import_tei.py` – full path using symlink: `apis_ontology/ontology_specific_scripts/import_tei.py` – which can be run like so:

```sh
$ python manage.py run_ontology_script import_tei --settings=apis_ontology.settings.local_settings
```
