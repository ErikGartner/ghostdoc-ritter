# ghostdoc-ritter

[ ![Codeship Status for ErikGartner/ghostdoc-ritter](https://codeship.com/projects/cb42cc20-c549-0133-1964-4e8753dd3f97/status?branch=master)](https://codeship.com/projects/138525) [![Build Status](https://travis-ci.org/ErikGartner/ghostdoc-ritter.svg?branch=master)](https://travis-ci.org/ErikGartner/ghostdoc-ritter)

*Ritter is the data processing engine for ghostdoc.*

[Ghostdoc](https://github.com/ErikGartner/ghostdoc) is a semi-automatic self-generating wiki written in Meteor. To allow for more advanced data processing and NLP it is powered by this module, *Ritter*.

## Features

**Sources:**
- Table of content
- Language detection
- Linkifying artifacts

**Artifacts:**
- Table of content
- Gender detection (from artifact name)
- Extraction of relevant paragraphs
- Extraction of user defined  gems (facts about artifact)

## Installation
This project is optimmized for running on Dokku but can run elsewhere as well. *Ritter* requires Python >= 3.4, a Mongo database and a RabbitMQ broker. Running multiple instances for the same *Ghostdoc* instance is possible and preferred.

Dependencies can be installed using pip or setuptools.

The following enviorment variables should be set and should be same as the ones set for *Ghostdoc*.
```
MONGO_URL
RABBITMQ_URL
```
