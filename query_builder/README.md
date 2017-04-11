# Growth Intelligence API
The API uses data indexed by [elasticsearch](https://www.elastic.co/) to serve results to the [frontend](https://github.com/pelucid/frontend) app.

## Repo Champion

The Repo champion is Sam

## Getting started

#### Prerequisites

* Install elasticsearch **2.4**.
  * Available on Homebrew, APT or https://www.elastic.co/guide/en/elasticsearch/reference/2.4/_installation.html
  * **NB**: be sure to enable scripting in your [elasticsearch.yaml config](https://github.com/pelucid/config/blob/1f713a9b2df50661fc37ec11ed1e4055cc7b6dc7/dev2/elasticsearch/elasticsearch.yml#L389)
* Install mysql
  * This can be done with `brew install mysql`
  * **NB**: Read [the on-boarding docs](https://pelucid.atlassian.net/wiki/display/GI/Step+1.+Getting+set+up) for required settings
* Clone the dependencies:
  * [indexer](https://github.com/pelucid/indexer)

#### Steps to get up and running

0. `cd` into the project root
0. Create a virtualenv and install requirements `make deps`
0. Once the indexer has indexed the test data into elasticsearch, you should be able to test the setup from the project root with: `make clean-test`
0. If the tests pass, run `make run_dev` to start the API.

*NB: After the fixture data has been built once, you can use `make test` to run the python tests*

## Troubleshooting

> I get an AttributeError for the API settings

The environment variable `GI_ENV=<env>` must be set (where `<env>` is `PROD`, `STAGING` or `TEST`)

> I get "service unavailable" when I ping the API :(

Make sure elasticsearch is running!

> My tests are failing.

Did you set up the api and indexer in the right order? Create test data in the API, then run the indexer, and then run the API tests!

> I am inundated with SearchParseExceptions in the elasticsearch output

You forgot to add support for dynamic scripting in the elasticsearch config. See above.

> *Import errors like* ImportError: No module named api.credential_models

Make sure that the PYTHONPATH environment variable is set to the root of all the repos. E.g. if you store the repos in ~/dev, and username is USERNAME add the following to your .bash_profile

```
export PYTHONPATH="${PYTHONPATH}:/Users/USERNAME/dev"
```

> ImportError: dlopen(.../site-packages/_mysql.so, 2): Library not loaded: libssl.1.0.0.dylib

Are you using anaconda? And homebrew? Try `brew unlink openssl && brew link openssl --force`

> sqlalchemy.exc.OperationalError: (OperationalError) ("... doesn't have a default value")

Are you using a MySQL version 5.7.X or higher? A bug was fixed making the SQL standard strict over previous versions (that the sevrers use). The quickest fix is to remove `STRICT_TRANS_TABLES` from `sql_mode=` if present or add the line `sql_mode=NO_ENGINE_SUBSTITUTION` to your `my.cnf` file otherwise. If you installed mysql with brew there is a sample file `/usr/local/Cellar/mysql/5.7.10/support-files/my-default.cnf` which you can copy to `/etc/my.cnf` before editing.

## Development

To create an auto-generated alembic migration script for the db schema: 

`GI_ENV=TEST alembic -c alembic/alembic_api_test.ini revision --autogenerate -m "msg"`

NB if you're on the live system you should be using the alembic scripts not
postfixed with "_test"

# Setting up ACL indexing on export events locally
0. run rabbitmq `rabbitmq-server`
0. run a celery worker `GI_ENV=TEST celery -A celery_tasks.celery_worker worker -Q api_acl,api_export_snapshots`
0. Run the api normally.
0. When you export, you should see the output of the celery task in the shell.
