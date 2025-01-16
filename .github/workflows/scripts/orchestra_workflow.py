import os
import time
import requests

# ------------------------------------------------------------------------------
# Get environment variables
# ------------------------------------------------------------------------------
api_base = os.getenv(
    "ORCHESTRA_URL", "https://app.getorchestra.io"
)  # Default to Orchestra URL
job_cause = os.getenv(
    "ORCHESTRA_JOB_CAUSE", "API-triggered job"
)  # Default to generic message
git_branch = os.getenv("ORCHESTRA_JOB_BRANCH", None)  # Default to None
schema_override = os.getenv("ORCHESTRA_JOB_SCHEMA_OVERRIDE", None)  # Default to None
api_key = os.environ[
    "ORCHESTRA_API_KEY"
]  # No default, throw an error if key not provided
account_id = os.environ[
    "ORCHESTRA_ACCOUNT_ID"
]  # No default, throw an error if ID not provided
project_id = os.environ[
    "ORCHESTRA_PROJECT_ID"
]  # No default, throw an error if ID not provided
job_id = os.environ[
    "ORCHESTRA_JOB_ID"
]  # No default, throw an error if ID not provided

print(f"""
Configuration:
api_base: {api_base}
job_cause: {job_cause}
git_branch: {git_branch}
schema_override: {schema_override}
account_id: {account_id}
project_id: {project_id}
job_id: {job_id}
""")

req_auth_header = {"Authorization": f"Token {api_key}"}
req_job_url = f"{api_base}/api/v2/accounts/{account_id}/jobs/{job_id}/run/"
run_status_map = {
    1: "Queued",
    2: "Starting",
    3: "Running",
    10: "Success",
    20: "Error",
    30: "Cancelled",
}

type AuthHeader = dict[str, str]

def run_job(
    url: str,
    headers: AuthHeader,
    cause: str,
    branch: str | None = None,
    schema_override: str | None = None,
) -> int:
    """
    Runs an Orchestra job
    """
    req_payload = {"cause": cause}
    if branch and not branch.startswith("$( "):  # Check for valid branch name
        req_payload["git_branch"] = branch.replace("refs/heads/", "")
    if schema_override:
        req_payload["schema_override"] = schema_override.replace("-", "_").replace("/", "_")

    print(f"Triggering job:\n\turl: {url}\n\tpayload: {req_payload}")
    response = requests.post(url, headers=headers, json=req_payload)
    run_id: int = response.json()["data"]["id"]
    return run_id

def get_run_status(url: str, headers: AuthHeader) -> str:
    """
    Gets the status of a running Orchestra job
    """
    response = requests.get(url, headers=headers)
    run_status_code: int = response.json()["data"]["status"]
    run_status = run_status_map[run_status_code]
    return run_status

def main():
    print("Beginning request for job run...")

    run_id: int = 0
    try:
        run_id = run_job(
            req_job_url, req_auth_header, job_cause, git_branch, schema_override
        )
    except Exception as e:
        print(f"ERROR! - Could not trigger job:\n {e}")
        raise

    req_status_url = f"{api_base}/api/v2/accounts/{account_id}/runs/{run_id}/"
    run_status_link = f"{api_base}/deploy/{account_id}/projects/{project_id}/runs/{run_id}/"

    print(f"Job running! See job status at {run_status_link}")

    time.sleep(30)
    while True:
        status = get_run_status(req_status_url, req_auth_header)
        print(f"Run status -> {status}")

        if status in ["Error", "Cancelled"]:
            raise Exception(f"Run failed or canceled. See why at {run_status_link}")

        if status == "Success":
            print(f"Job completed successfully! See details at {run_status_link}")
            return

        time.sleep(10)

if __name__ == "__main__":
    main()
