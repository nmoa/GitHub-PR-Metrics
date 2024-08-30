import os
from pytz import timezone
from github import Github, Auth

from PR_db_connector import PullRequest, Comment

if os.path.exists(".env"):
    from dotenv import load_dotenv

    load_dotenv()


def datetime_utc_to_str_jst(datetime_utc) -> str:
    """
    UTCの日時をJSTに変換して文字列にフォーマットする関数

    :param datetime_utc: UTCの日時
    :return: JSTに変換された日時 (フォーマット: "%Y-%m-%d %H:%M:%S")
    """
    if datetime_utc is None:
        return None
    return datetime_utc.astimezone(timezone("Asia/Tokyo")).strftime("%Y-%m-%d %H:%M:%S")


def format_comment(comment, assignee, pull_id):
    """
    コメント情報をデータベースに保存する形式にフォーマットする関数

    :param comment: コメント
    :param assignee: プルリクエストの担当者
    :param pull_id: プルリクエストのID
    :return: フォーマットされたコメント情報
    """
    return Comment(
        comment_id=comment.id,
        assignee=assignee,
        commenter=comment.user.login,
        body=comment.body,
        created_at=datetime_utc_to_str_jst(comment.created_at),
        pull_id=pull_id,
    )


def format_pull_info(pull):
    """
    プルリクエスト情報をデータベースに保存する形式にフォーマットする関数

    :param pull: プルリクエスト
    :return: フォーマットされたプルリクエスト情報
    """
    print(f"Getting info for PR {pull.base.repo.name}#{pull.number}")
    commits = pull.get_commits()
    return PullRequest(
        id=pull.id,
        repository=pull.base.repo.name,
        number=pull.number,
        title=pull.title,
        assignee=pull.assignee.login if pull.assignee else None,
        target_branch=pull.base.ref,
        source_branch=pull.head.ref,
        first_commit_at=datetime_utc_to_str_jst(commits[0].commit.author.date),
        merged_at=datetime_utc_to_str_jst(pull.merged_at),
        num_commits=commits.totalCount,
    )


def fetch_comments(pull):
    """
    プルリクエストに紐づいたコメントを取得する関数

    :param pull: プルリクエスト
    :return: コメントのリスト
    """
    comments = pull.get_comments()
    assignee = pull.assignee.login if pull.assignee else None
    comments_formatted = [
        format_comment(comment, assignee, pull.id)
        for comment in comments
        if comment.user.login != assignee
    ]
    return comments_formatted


def fetch_closed_pulls(repo_name):
    """
    GitHubのリポジトリからクローズされたプルリクエストのリストを取得する関数

    :param repo_name: リポジトリ名 (例: "octocat/Hello-World")
    :return: クローズされたプルリクエストのリスト
    """
    auth = Auth.Token(os.environ["GITHUB_TOKEN"])
    g = Github(auth=auth)
    repo = g.get_repo(repo_name)
    pulls = repo.get_pulls(state="closed")
    return pulls


def store_pr_and_comments_to_db(session, repo_name):
    ids = session.query(PullRequest.id).all()
    pull_ids_stored = [id[0] for id in ids]

    pulls = fetch_closed_pulls(repo_name)

    # idがDBに保存されていないPRを取得
    pulls_merged = [pull for pull in pulls if pull.merged_at is not None]
    pulls_not_stored = [pull for pull in pulls_merged if pull.id not in pull_ids_stored]
    pulls_to_insert = [format_pull_info(pull) for pull in pulls_not_stored]

    # pulls_not_stored に紐づいたコメントを取得
    comments_to_insert = []
    for pull in pulls_not_stored:
        comments = fetch_comments(pull)
        comments_to_insert.extend(comments)

    session.add_all(pulls_to_insert)
    session.add_all(comments_to_insert)
    try:
        session.commit()
        print("Data inserted successfully")
    except Exception as e:
        print(f"Error inserting data: {e}")
        session.rollback()
    return
