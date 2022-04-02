#!/usr/bin/env python3
import argparse
from datetime import datetime, timedelta
import gitlab
import os
import sys


class EnvDefault(argparse.Action):
    def __init__(self, envvar, required=True, default=None, **kwargs):
        if not default and envvar:
            if envvar in os.environ:
                default = os.environ[envvar]
        if required and default:
            required = False
        super(EnvDefault, self).__init__(default=default, required=required, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, values)


def clean(args):
    d = datetime.today() - timedelta(days=args.days)
    gl = gitlab.Gitlab(
        args.gitlab_url, private_token=args.gitlab_token, user_agent=args.user_agent
    )
    projects = gl.projects.list(as_list=False)
    for project in projects:
        print("[x] Handling {}...".format(project.name))
        pipelines = project.pipelines.list(as_list=False, updated_before=d)
        if len(pipelines) == 0:
            print(" [-] Skipping project because no pipeline found")
            continue
        print(
            " [-] Found {} pipelines older than {} days to delete".format(
                len(pipelines), args.days
            )
        )
        if args.dry_run:
            print("  [!] dry run mode enabled won't delete")
            continue
        for pipeline in pipelines:
            pipeline.delete()
    return True


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-u",
        "--gitlab-url",
        action=EnvDefault,
        envvar="GITLAB_URL",
        help="Gitlab URL to call",
    )
    parser.add_argument(
        "-t",
        "--gitlab-token",
        action=EnvDefault,
        envvar="GITLAB_TOKEN",
        help="Gitlab token to use",
    )
    parser.add_argument(
        "--user-agent",
        action=EnvDefault,
        envvar="USER_AGENT",
        default="gitlab-pipeline-cleaner",
        help="Gitlab user-agent to be used",
    )
    parser.add_argument(
        "--dry-run", action="store_true", default=False, help="Enable dry run mode"
    )
    parser.add_argument(
        "-d",
        "--days",
        type=int,
        action=EnvDefault,
        envvar="OLDER_THAN",
        help="Pipelines older than this variable in days will be deleted",
    )
    args = parser.parse_args()
    sys.exit(clean(args))


if __name__ == "__main__":
    main()
