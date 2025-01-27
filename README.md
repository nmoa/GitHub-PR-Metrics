# GitHub-PR-Metrics

Collect merged Pull Request data and non-assignee comments from GitHub repositories via GitHub REST API and store them in a PostgreSQL database.

## Installation

1. Clone this repository:

```bash
git clone https://github.com/nmoa/GitHub-PR-Metrics.git
cd GitHub-PR-Metrics
```

2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Environment Variables

Before running the script, you need to set up the following environment variables in a `.env` file:

### Database Configuration

- `DB_USER`: PostgreSQL database username
- `DB_PASSWORD`: PostgreSQL database password
- `DB_HOST`: Database host address
- `DB_PORT`: Database port number

### GitHub Configuration

- `GITHUB_TOKEN`: Your GitHub Personal Access Token

Example `.env` file:

```
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=your_db_host
DB_PORT=5432
GITHUB_TOKEN=your_github_token
```

### Getting GitHub Token

1. Go to GitHub Settings > Developer settings > Personal access tokens
2. Generate a new token with `repo` scope access
3. Copy the token and add it to your `.env` file

## Usage

The script allows you to collect Pull Request and comment data from specified GitHub repositories and store them in a database.

### Basic Usage

Run the script with one or more repository names as arguments:

```bash
python main.py repository-name [repository-name ...]
```

### Example

To collect data from a single repository:

```bash
python main.py owner/repository
```

To collect data from multiple repositories:

```bash
python main.py owner/repo1 owner/repo2 owner/repo3
```

Note: Make sure you have properly configured your database connection and GitHub credentials before running the script.
