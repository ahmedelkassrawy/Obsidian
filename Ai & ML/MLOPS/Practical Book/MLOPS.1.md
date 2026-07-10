Continuous integration (CI)
CI is the process of continuously testing a software project and improving the
quality based on these tests’ results. It is automated testing using open source and
SaaS build servers such as GitHub Actions, Jenkins, Gitlab, CircleCI, or cloud
native build systems like AWS Code Build.
Continuous delivery (CD)
This method delivers code to a new environment without human intervention.
CD is the process of deploying code automatically,
Microservices
A microservice is a software service with a distinct function that had little to no
dependencies. One of the most popular Python-based microservice frameworks
is Flask.
Infrastructure as Code
Infrastructure as Code (IaC) is the process of checking the infrastructure into a
source code repository and “deploying” it to push changes to that repository. IaC
allows for idempotent behavior and ensures the infrastructure doesn’t require
humans to build it out.
Monitoring and instrumentation
Monitoring and instrumentation are the processes and techniques used that
allow an organization to make decisions about a software system’s performance
and reliability.
![[Pasted image 20250627010113.png]]![[Pasted image 20250627010400.png]]
Makefile
A Makefile runs “recipes” via the make system,
Make install
This step installs software via the make install command
Make lint
This step checks for syntax errors via the make lint command
Make test
This step runs tests via the make test command:
install:
pip install --upgrade pip &&\
pip install -r requirements.txt
lint:
pylint --disable=R,C hello.py
test:
python -m pytest -vv --cov=hello test_hello.py

Source code and tests
The Python scaffolding’s final portion is to add a source code file and a test file,
as shown here. This script exists in a file called hello.py:

Why create and use a Python virtual environment?
A Python virtual environment isolates third-party
packages to a specific directory. There are other solutions to
this problem and many developing tools. They effectively
solve the same problem: the Python library and interpreter are
isolated to a particular project.