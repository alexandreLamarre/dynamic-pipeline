# dynamic-pipeline

<img src="https://app.travis-ci.com/alexandreLamarre/dynamic-pipeline.svg?branch=main"/>

## What is this project?

The project is a python-native and python-oriented automation pipeline implementation.
This means it requires only python to set up some sort of CICD/build/workload pipeline - the caveat being is that it requires the rest of the automation code to be integrated into the pipeline to:

- Have python wrappers, or
- Be written in python

It aims to make modern standards of automation possible in older environments that have large and difficult to manage infrastructure and cannot integrate Jenkins or Tracis CI. For example, it integrates nicely with large monolithic architectures who have many different teams managing different aspects of the automation - over which you have no control over the intermediary script/technology usage - but want to seamlessly integrate with.

In addition, it aims to provide readable declaration of what the pipeline does in the form of its <pipeline>.YAML config files. It also aims to abstract away the pain of designing background subprocesses and concurrency via multi-threading in automation

It is primarily meant to be a useful tool for managing python OOP designed automation, loosely following some of these design principles:

- Python objects that perform pipeline workloads store what they need to continue their workload and only what they need to continue their workload.
- Each object represents a separate, mostly independent workload from the other objects. (For example you could have one object have a workload write to a file or upload a result, and have a second object depend on the name, existence or content of this file)

