## **Setup Requirements**

This project is built using `docker` and `docker-compose`.  You will need those up and running.  You can test with `sudo docker -v` and `sudo docker-compose -v`.

## **Overview**

This project has two separate (but overlapping) `docker-compose` configurations and two separate `Dockerfiles`, one each for the test and dev environments.  The main differences are a couple of additional test `python`modules and a couple of differing arguments on production for (in theory) more persistent `postgres` storage and `tty` availability.  I used `docker-compose` to bundle the `python` and `postgres` containers together and enable their easy communication.  Manual setup for a one-off like this is not ideal.  I ran into a significant issue here with the `python` container attempting to talk to `postgres` before the service is available.  There is a fix available (and I went headfirst down this [road](https://github.com/peter-evans/docker-compose-healthcheck)) before realizing that the `depends_on` is deprecated in `docker-compose v3`.  I got around it by just running things twice after initial setup and that works fine.  **Please remember to run the `up` command twice in production.  I have silenced the `postgres` logs so it will not be clear why the script failed the first time**.  

## **Running**

To run tests:
```
sudo docker-compose -f docker-compose.test.yml up --build --force-recreate --exit-code-from 
chatty_test
```
There is a little concern of idempotency here, as I have one test that hackily adds and deletes a new "QuestionText".  There are better ways of doing this, but I'm out of time.  Also note that you may need to run the above if `postgres` is slow to come up.  The error is very obvious and running the build a second time works just fine because the `postgres` container stays cached.  The test db is persisted (I think via an anonymous volume, but wasn't 100% sure here).  To clear it out:
```
sudo docker-compose -f docker-compose.test.yml down
```

To run the `dev` script, the commands are very similar:
```
sudo docker-compose -f docker-compose.yml up --build --force-recreate -d
```
and
```
sudo docker-compose -f docker-compose.yml down
```
The `dev` script opens a `TTY` as a background container and you have to attach to it with
```
sudo docker attach chatty_chatty_1
```
A few arrow keypresses will enable the full CLI.  This is unfortunate but `docker-compose` will catch up at some point.  The CLI asks you to choose a topic, then displays all the questions and question texts belonging to that topic, then lets you choose one to edit.


# **Model**

 Everything is in `model.py`, including schema setup.
- Nothing too surprising here.
- Big regret was not having anything more concrete to identify a `Question` .  It's effectively just a bridge id between `Topic` and `QuestionText`and having a string identifier would make the CLI a bit cleaner.
- One thing I'm missing that would be useful down the line is topic specificity.  A hierarchy of topics (parent-child relationship) would be ideal here.

 # **Moving fowards**
 - CLI is super bare-bones.  I spent most of my time on the model, wrestling with docker & SQLAlchemy, and getting my tests working.  I think a foundation is the most important part even if the final result isn't all the way there.  We can now add features and change things with more confidence.  
	 - Next time i'd keep the `cli` in a separate container and use compose for services (which is more what it's meant for).  
 - I gave limited consideration to query performance and docker build times.
 - My dev-env is a little lacking right now, so I didn't finish getting `flake8` working.  
 - Idempotency with the tests and a clean `postgres` proved difficult without manually running the cleanup command.
	 - I've seen this done several ways (usually wiping the db in the test cleanup) and it's always tricky.  
