import argparse
from PR_db_connector import connect_db
import GitHub_connector


def main(args):
    session = connect_db()
    for repo_name in args.repo_name:
        GitHub_connector.store_pr_and_comments_to_db(session, repo_name)
    session.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("repo_name", nargs="+", type=str)
    args = parser.parse_args()
    main(args)
