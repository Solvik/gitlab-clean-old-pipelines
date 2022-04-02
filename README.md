# Gitlab clean old pipelines

This project aim is to clean old pipelines from your Gitlab self-hosted instance.

## Usage

```
usage: main.py [-h] -u GITLAB_URL -t GITLAB_TOKEN [--user-agent USER_AGENT] [--dry-run] -d DAYS
main.py: error: the following arguments are required: -h/--gitlab-url, -t/--gitlab-token, -d/--days
```

## Example

Will delete pipelines older than 365 days

```
$ ./main.py -u https://gitlab.foo.bar -t mysupertoken -d 365
```

## Using Docker

```
$ docker build -t gitlab-clean-old-pipeline .
$ docker run -ti -e GITLAB_URL=https://gitlab.foo.bar \
  -e GITLAB_TOKEN=mysupertoken \
  -e OLDER_THAN=365
  gitlab-clean-old-pipeline
```
