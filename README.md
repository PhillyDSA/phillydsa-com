[![Requirements Status](https://requires.io/github/PhillyDSA/phillydsa-com/requirements.svg?branch=develop)](https://requires.io/github/PhillyDSA/phillydsa-com/requirements/?branch=develop)
[![CircleCI](https://circleci.com/gh/PhillyDSA/phillydsa-com.svg?style=svg)](https://circleci.com/gh/PhillyDSA/phillydsa-com) [![codecov](https://codecov.io/gh/PhillyDSA/phillydsa-com/branch/develop/graph/badge.svg)](https://codecov.io/gh/PhillyDSA/phillydsa-com)
# Philly DSA Website

Django site for Philly DSA

## Contributing

####  Code of Conduct
All contributors agree to abide by the Philly DSA Code of Conduct, which can be found at: [TKTK](github.com/TKTK).

#### Environment

Clone the repository with:

    git clone
    git checkout develop
    git submodule init
    git submodule update

That should be it.

##### Backend

Install requirements. If you're using [pyenv](https://github.com/pyenv/pyenv):

    make dev

Or by running:

    pip install -r requirements/dev.txt

This will install all the required dependencies for the project. We use [pre-commit](http://pre-commit.com/) hooks, so if you didn't install by `make dev`, run `pre-commit install` in the root directory.

Development occurs on the `develop` branch and `master` is reserved for releases. See [A Successful Git Branching Model](http://nvie.com/posts/a-successful-git-branching-model/) for rationale. [Git Flow AVH](https://github.com/petervanderdoes/gitflow-avh) is one tool to help manage this workflow. YMMV so use whatever you're comfortable with and it'll work out in the end.

##### Frontend

Install gulp globally with:

    npm install gulp -g

Install local dependencies with:

    npm install

This is just for livereload at the moment, so feel free to ignore if it's annoying.

##### Putting it all together

Run:

    make dev
    python manage.py migrate
    python manage.py createsuperuser  # follow prompts
    make gulp  # open another terminal and:
    make server

and you should be good to go.

#### Testing

Please ensure that all contributions have corresponding test coverage. Running `make test` will run all the tests for the project and output a coverage report.

#### Pull Requests

We use the following naming conventions, which help to keep things organized:

* Branch name for production releases: `master`
* Branch name for "next release" development: `develop`
* Feature branch prefix: `feature/`
* Bugfix branch prefix: `bugfix/`
* Release branch prefix: `release/`
* Hotfix branch prefix: `hotfix/`

To submit a pull request, start new branch, commit your changes, and then submit the PR. We're all volunteers, so review may not be immediate (it doesn't mean you're being ignored!), but if it's been a while, ping a collaborator.

#### Issues

Feel free to submit any issues you come across, whether they're technical or something about installation or usage is unclear - both are important and welcome.

We use issue templates, which may not be appropriate for all issues, so take the template with a grain of salt.
