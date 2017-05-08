# Day-in interview prep

### Project - Example of an Elasticsearch QueryBuilder API

Thanks for coming in for the day at GrowthIntel. To make sure that we can use our time best in the day, we'd like to have you do some setup in advance. For the majority of the day you'll be working in this repo, on a Elasticsearch query building API.

### Setup - Installing Python, Virtualenv

First, clone this repository to your computer via the links on the right (creating a fork of the repository is not necessary). Next, ensure that you have virtualenv installed. If you're using Debian or Ubuntu, you likely want to run `sudo apt-get install python-virtualenv python-dev build-essential`. Otherwise, you can find installation instructions for `virtualenv` [here](https://virtualenv.pypa.io/en/latest/installation.html), and more general help with `pip` and Python package management [here](https://docs.python.org/2.7/installing/index.html). Note, we will be working with Python 2.7.

### Setup - Installing Project Requirements

When you have virtualenv installed, create a new Python environment and activate it by running:
```
virtualenv interview_env
source interview_env/bin/activate
```
Next, install some requirements by running: `pip install -r requirements.txt`, where requirements.txt is the path to the accompanying file. This may take a minute or two. When you're able to install the packages in requirements.txt, you're all done!

### Checking you're done

First, make sure your PYTHONPATH environment variable is set correctly. This can be done by running the following command:
```bash
export PYTHONPATH=/path/to/this/repo:$PYTHONPATH
```
When you have the dependencies installed, try the following command:

```bash
python main.py "/v1/company_query_builder?revenue=20150101-20160101"
```
You should see the following output:
```json
{
  "query": {
    "filtered": {
      "filter": {
        "and": [
          {
            "term": {
              "status": 1
            }
          },
          {
            "nested": {
              "filter": {
                "bool": {
                  "must": [
                    {
                      "range": {
                        "financial_filters.revenue": {
                          "gte": 20150101,
                          "lte": 20160101
                        }
                      }
                    }
                  ]
                }
              },
              "path": "financial_filters"
            }
          }
        ]
      }
    }
  },
  "from": 0,
  "size": 50
}
```
