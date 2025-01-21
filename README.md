# Semantic Scholar Monitor

**Semantic Scholar Monitor** is a Python-based tool for monitoring the availability and responsiveness of the [Semantic Scholar API](https://www.semanticscholar.org/product/api). This repository includes scripts to:
- Periodically send requests to the Semantic Scholar API.
- Compare the success rates of requests using Python's `requests` library and `curl`.
- Log request outcomes (e.g., success, failure, error) for further analysis.

---

## Features

- **Dynamic Paper ID Selection**: Selects a random paper ID from a preloaded list for each request.
- **Dual Mode Requests**: Monitors API availability using both Python and `curl` for redundancy and comparison.
- **Detailed Logging**: Captures results, timestamps, selected paper IDs, and request modes in a CSV file.
- **Customizable Scheduling**: Configurable request intervals using the `schedule` library.
- **Workflow Visualization**: ASCII workflow diagram to outline the request-monitoring process.

---

## Workflow

Below is the ASCII representation of the monitoring workflow:

```
+----------------------+
|   Start Script       |
+----------+-----------+
           |
           v
+----------------------+      +-------------------------+
| Load paper IDs       |----->| paper_ids.txt available?|
+----------+-----------+      +-----------+-------------+
           |                                |
           v                                v
+-----------------------+          +----------------------+
| Paper IDs loaded into |          | Exit script with    |
| a list                |          | "No paper IDs" error|
+-----------+-----------+          +----------------------+
            |
            v
+-------------------------------+
| Randomly select a paper ID    |
| for each scheduled request    |
+---------------+---------------+
                |
                v
+-------------------------------+      +----------------------+
| Make Python HTTP request      |----->| Successful request?  |
| using `requests` library      |      +-----------+----------+
+---------------+---------------+                  |
                |                                  |
                |                                  v
                |                          +-------------------+
                |                          | Log "Failure" or  |
                |                          | "Error" in CSV    |
                v                          +-------------------+
+-------------------------------+      
| Make cURL HTTP request        |-----> Same "Success" or "Failure"
| using subprocess module       |       logic as Python requests
+---------------+---------------+
                |
                v
+-------------------------------+
| Log request details           |
| (Python/cURL mode, result,    |
| timestamp, selected paper ID) |
+---------------+---------------+
                |
                v
+-------------------------------+
| Scheduler waits for next      |
| interval (e.g., 30 minutes)   |
+---------------+---------------+
                |
                v
+-------------------------------+
|     Continue indefinitely     |
+-------------------------------+
```

---

### Dependencies

This project requires a Python environment with specific dependencies to monitor and analyze Semantic Scholar API requests. For consistency and ease of setup, we provide an `environment.yml` file for managing dependencies using Conda.

#### Required Dependencies
The following Python packages are needed:
- **`requests`**: For making HTTP requests to the Semantic Scholar API.
- **`schedule`**: For scheduling periodic tasks.
- **`pandas`**: For logging and analyzing request data.

#### Using the `environment.yml` File
To ensure a consistent environment, follow these steps:

1. **Install Conda** (if not already installed):
   - You can download and install Miniconda or Anaconda from [here](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html).

2. **Create the Environment**:
   - Run the following command in the repository's root directory (where `environment.yml` is located):
     ```bash
     conda env create -f environment.yml
     ```

3. **Activate the Environment**:
   - Once the environment is created, activate it using:
     ```bash
     conda activate semantic-scholar-monitor
     ```

4. **Verify the Installation**:
   - Check if the dependencies were installed correctly:
     ```bash
     conda list
     ```

#### Manually Installing Dependencies
If you prefer not to use Conda, you can manually install the required dependencies using `pip`:
```bash
pip install requests schedule pandas
```

---

#### `environment.yml` File

Below is the content of the `environment.yml` file provided in this repository:

```yaml
name: semantic-scholar-monitor
channels:
  - conda-forge
dependencies:
  - python=3.9
  - requests
  - schedule
  - pandas
```
---

5. Run the script from scripts directory
```bash
nohup python ss-scholar-monitor.py > output.log 2>&1 &
```

6. Alternatively, schedule with cron
```bash

$crontab -e

0 2 * * * /usr/bin/python /home/daniel/git/semantic-scholar-monitor/scripts/ss-scholar-monitor.py > /home/daniel/git/semantic-scholar-monitor/scripts/output.log 2>&1

```
### TODO: Future Sprints

Wish list features for the project:

1. **Organize Project Structure:**
   - Separate existing scripts, data, and reports into dedicated sub-directories for better organization:
     - `scripts/` for Python scripts.
     - `data/` for `paper_ids.txt`, logs, and other input files.
     - `reports/` for generated plots and analysis outputs.

2. **Automate Script Execution: DONE**
   - Replace the current `nohup` method with cron jobs or other task schedulers for improved automation and manageability.
   - Define cron schedules for:
     - Running `monitor_requests.py` periodically (e.g., every 30 minutes).
     - Running `analyze_logs.py` and `update_repo.py` once a day.

3. **Expand Paper IDs:**
   - Add more paper IDs to `paper_ids.txt` to improve monitoring robustness and test API performance across a wider dataset.

4. **Add Reporting Capabilities:**
   - Automatically generate and archive a daily report summarizing API performance (e.g., success rates, error analysis).
   - Include visualizations in the report (e.g., success rate by hour and day).

5. **Improve Logging and Error Handling:**
   - Add detailed logging for easier debugging (e.g., timestamped logs, categorized error messages).
   - Include retry logic for failed API requests with exponential backoff.

6. **Deploy on Hosted Service:**
   - Migrate the script to run on a hosted service (e.g., AWS EC2, Azure, or a Raspberry Pi) for 24/7 monitoring.
   - Configure service-level monitoring for uptime and error alerts.

7. **Optimize GitHub Updates:**
   - Schedule GitHub updates only when there are changes to push.
   - Compress and archive old log files to save space in the repository.

8. **Add Documentation and Configuration:**
   - Enhance the `README.md` with examples of cron job configuration and running the project on hosted services.
   - Include a configuration file (e.g., `config.yaml`) to make intervals, file paths, and other settings customizable.

9. **API Rate Limit Handling:**
   - Implement logic to detect and respond to API rate-limiting errors (e.g., reduce request frequency temporarily).

10. **Add Docker Support:**
    - Create a `Dockerfile` and instructions for containerizing the application, ensuring a consistent runtime environment.

---

Here’s a **Contributing** sub-section you can append to the `README.md` file:

---

### Contributing

We welcome contributions to improve the **Semantic Scholar Monitor** project! Whether it's fixing bugs, adding new features, or enhancing documentation, your help is greatly appreciated. Here's how you can get started:

#### How to Contribute
1. **Fork the Repository:**
   - Click the "Fork" button on the top right of the GitHub repository page.

2. **Clone Your Fork:**
   - Clone your forked repository to your local machine:
     ```bash
     git clone git@github.com:<your-username>/semantic-scholar-monitor.git
     cd semantic-scholar-monitor
     ```

3. **Create a New Branch:**
   - Create a branch for your feature or bugfix:
     ```bash
     git checkout -b feature-or-bugfix-name
     ```

4. **Make Your Changes:**
   - Add or update code, data, or documentation.
   - Follow best practices for Python development, including:
     - Using meaningful commit messages.
     - Testing your changes locally.

5. **Push Your Changes:**
   - Push your changes to your fork:
     ```bash
     git add .
     git commit -m "Description of your changes"
     git push origin feature-or-bugfix-name
     ```

6. **Submit a Pull Request:**
   - Go to the original repository on GitHub.
   - Click "New Pull Request" and select your branch for comparison.
   - Describe your changes and link to any related issues.

#### Guidelines for Contributions
- **Code Quality:**
  - Follow Python best practices (e.g., PEP 8 style guide).
  - Include comments and docstrings for clarity.
- **Testing:**
  - Ensure your changes are thoroughly tested before submitting.
- **Commit Messages:**
  - Write clear, concise commit messages summarizing your changes.
- **Documentation:**
  - Update the `README.md` file or other relevant documentation if necessary.
- **Collaboration:**
  - Engage with reviewers during the pull request process to address feedback.

#### Reporting Issues
If you encounter any bugs or have suggestions, please open an issue on the GitHub repository:
- Include a clear description of the problem or feature request.
- Provide steps to reproduce the issue (if applicable).

#### Contact
Feel free to reach out via GitHub issues if you have any questions about contributing!

---

