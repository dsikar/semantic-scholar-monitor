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

