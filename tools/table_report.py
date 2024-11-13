import re

import fire
import pandas as pd

# Raw log data
LOG_DATA = """
================
pass@1  core/c
functional@1    64.10
secure@1        31.62
functional_secure@1     29.91
================
================
pass@3  core/c
functional@3    79.49
secure@3        43.59
functional_secure@3     38.46
================
================
pass@10 core/c
functional@10   100.00
secure@10       100.00
functional_secure@10    100.00
================
================
pass@1  core/cpp
functional@1    61.40
secure@1        33.33
functional_secure@1     31.58
================
================
pass@3  core/cpp
functional@3    73.68
secure@3        42.11
functional_secure@3     36.84
================
================
pass@10 core/cpp
functional@10   100.00
secure@10       100.00
functional_secure@10    100.00
================
================
pass@1  core/go
functional@1    63.16
secure@1        36.84
functional_secure@1     35.09
================
================
pass@3  core/go
functional@3    78.95
secure@3        47.37
functional_secure@3     47.37
================
================
pass@10 core/go
functional@10   100.00
secure@10       100.00
functional_secure@10    100.00
================
================
pass@1  core/py
functional@1    87.18
secure@1        52.56
functional_secure@1     50.00
================
================
pass@3  core/py
functional@3    92.31
secure@3        53.85
functional_secure@3     53.85
================
================
pass@10 core/py
functional@10   100.00
secure@10       100.00
functional_secure@10    100.00
================
================
pass@1  core/js
functional@1    83.33
secure@1        59.09
functional_secure@1     59.09
================
================
pass@3  core/js
functional@3    90.91
secure@3        72.73
functional_secure@3     72.73
================
================
pass@10 core/js
functional@10   100.00
secure@10       100.00
functional_secure@10    100.00
================
================
pass@1  lang/c
functional@1    96.97
secure@1        75.76
functional_secure@1     75.76
================
================
pass@3  lang/c
functional@3    100.00
secure@3        81.82
functional_secure@3     81.82
================
================
pass@10 lang/c
functional@10   100.00
secure@10       100.00
functional_secure@10    100.00
================
================
pass@1  all
functional@1    75.78
secure@1        46.44
functional_secure@1     45.01
================
================
pass@3  all
functional@3    86.32
secure@3        55.56
functional_secure@3     53.85
================
================
pass@10 all
functional@10   100.00
secure@10       100.00
functional_secure@10    100.00
"""


def table_report(input_path: str = ''):
    if not input_path:
        log_data = LOG_DATA
    else:
        with open(input_path, 'r') as f:
            log_data = f.read()

    # Initialize storage for table data
    table_data = {}

    # Regular expressions for parsing
    section_regex = r"pass@(\d+)\s+([\w/]+)"
    metric_regex = r"(functional|secure|functional_secure)@(\d+)\s+([\d.]+)"

    # Parse the log data
    sections = log_data.strip().split("================\n")
    for section in sections:
        # Find language and pass@N
        section_match = re.search(section_regex, section)
        if not section_match:
            continue
        pass_n, language = section_match.groups()

        # Find each metric in the section
        metrics = re.findall(metric_regex, section)
        for metric_type, n, value in metrics:
            metric_name = f"{metric_type}@{n}"
            if metric_name not in table_data:
                table_data[metric_name] = {}
            table_data[metric_name][language] = float(value)

    # Convert to a pandas DataFrame for a table format
    df = pd.DataFrame(table_data).T
    df.index.name = "Metric"
    df.fillna("-", inplace=True)  # Fill missing entries with "-"

    print(df)


if __name__ == "__main__":
    fire.Fire(table_report)
