import os
import sys
from datetime import datetime
#pip install weasyprint

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(line_buffering=True)
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(line_buffering=True)

# HTML & CSS template for the Slurm Cheat Sheet
HTML_CONTENT = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>NC State HPC (Hazel) Slurm Cheat Sheet</title>
    <style>
        :root {
            --brand-red: #7a0000;
        }

        @page {
            size: letter landscape;
            margin: 30mm 10mm 12mm 10mm;
            background-color: #fcfcfc;
            @bottom-right {
                content: "Page " counter(page) " of " counter(pages);
                font-family: Arial, Helvetica, sans-serif;
                font-size: 8pt;
                color: #666666;
            }
            @bottom-left {
                content: "SEFS Lab HPC Command Cheat Sheet";
                font-family: Arial, Helvetica, sans-serif;
                font-size: 8pt;
                color: #666666;
                font-weight: bold;
            }
        }

        *, *::before, *::after {
            box-sizing: border-box;
        }

        body {
            font-family: Arial, Helvetica, sans-serif;
            font-size: 8.5pt;
            line-height: 1.25;
            color: #222222;
            margin: 0;
            padding: 0;
        }

        /* Banner / Header */
        .header-banner {
            background-color: var(--brand-red);
            color: #ffffff;
            padding: 8px 14px;
            border-radius: 4px;
            margin: 0;
            position: fixed;
            top: -21mm;
            left: 0;
            right: 0;
            z-index: 10;
        }

        .header-table {
            width: 100%;
            border-collapse: collapse;
        }

        .header-table td {
            vertical-align: middle;
            padding: 0;
            border: none;
        }

        .title-main {
            font-size: 15pt;
            font-weight: bold;
            letter-spacing: 0.5px;
            margin: 0;
            text-transform: uppercase;
        }

        .title-sub {
            font-size: 9pt;
            opacity: 0.9;
            margin-top: 3px;
        }

        .header-meta {
            text-align: right;
            font-size: 8pt;
            line-height: 1.3;
        }

        .header-meta strong {
            color: #ffcccc;
        }

        /* Wrapping card layout in reading order */
        .cards-grid {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            align-items: flex-start;
            align-content: flex-start;
        }

        .cards-grid .card {
            width: calc(50% - 4px);
            margin-bottom: 0;
        }

        /* Card / Section Box */
        .card {
            background: #ffffff;
            border: 1px solid #dcdcdc;
            border-radius: 4px;
            margin-bottom: 10px;
            page-break-inside: avoid;
            box-shadow: 0 1px 3px rgba(0,0,0,0.03);
        }

        .card-header {
            background-color: var(--brand-red);
            color: #ffffff;
            font-size: 9pt;
            font-weight: bold;
            padding: 5px 8px;
            border-top-left-radius: 3px;
            border-top-right-radius: 3px;
            letter-spacing: 0.3px;
            text-transform: uppercase;
        }

        .card-header.red-accent {
            background-color: var(--brand-red);
        }

        .card-body {
            padding: 6px;
        }

        /* Tables inside cards */
        table.data-table {
            width: 100%;
            border-collapse: collapse;
            font-size: 8pt;
        }

        table.data-table th {
            background-color: #f0f0f0;
            color: #333333;
            text-align: left;
            padding: 4px 5px;
            font-weight: bold;
            border-bottom: 1px solid #ccc;
        }

        table.data-table td {
            padding: 3.5px 5px;
            border-bottom: 1px solid #eef0f2;
            vertical-align: top;
        }

        table.data-table tr:nth-child(even) td {
            background-color: #f9fbfd;
        }

        table.data-table tr:last-child td {
            border-bottom: none;
        }

        code {
            font-family: "Consolas", "Courier New", monospace;
            font-size: 8pt;
            background-color: #f1f3f5;
            color: #990000;
            padding: 1px 4px;
            border-radius: 2px;
            font-weight: bold;
            word-break: break-word;
        }

        .code-block {
            font-family: "Consolas", "Courier New", monospace;
            font-size: 7.5pt;
            background-color: #1e1e1e;
            color: #d4d4d4;
            padding: 6px 8px;
            border-radius: 3px;
            line-height: 1.3;
            white-space: pre;
            margin: 4px 0;
            overflow-x: hidden;
        }

        .code-block .keyword { color: #569cd6; font-weight: bold; }
        .code-block .comment { color: #6a9955; font-style: italic; }
        .code-block .string { color: #ce9178; }
        .code-block .var { color: #9cdcfe; }

        .badge {
            display: inline-block;
            padding: 1px 4px;
            font-size: 7pt;
            font-weight: bold;
            color: #fff;
            background-color: #6c757d;
            border-radius: 2px;
            text-transform: uppercase;
        }
        .badge-red { background-color: #cc0000; }
        .badge-dark { background-color: #343a40; }

        .desc-note {
            font-size: 7.5pt;
            color: #555555;
            margin-top: 1px;
        }
    </style>
</head>
<body>

    <!-- Header Banner -->
    <div class="header-banner">
        <table class="header-table">
            <tr>
                <td>
                    <div class="title-main">SEFS lab HPC Command Cheat Sheet</div>
                    <div class="title-sub">General command guide for NC State HPC (Hazel) using Slurm scheduler</div>
                </td>
                <td class="header-meta">
                    <strong>Cluster Access:</strong> <code>ssh &lt;unityid&gt;@login.hpc.ncsu.edu</code><br>
                    <strong>OS / Scheduler:</strong> RHEL 9.2 / Slurm Workload Manager<br>
                    <strong>Author:</strong> Michelle Pretorius | <strong>Updated:</strong> Aug 2026
                </td>
            </tr>
        </table>
    </div>

    <!-- Main Content Grid -->
    <div class="cards-grid">

                <!-- Storage Directories -->
                <div class="card">
                    <div class="card-header red-accent">1. Filesystems & Storage Directories</div>
                    <div class="card-body">
                        <table class="data-table">
                            <thead>
                                <tr>
                                    <th>Location</th>
                                    <th>Path & Quota</th>
                                    <th>Purpose / Policy</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr>
                                    <td><strong>Home</strong></td>
                                    <td><code>~/</code> or <code>/home/&lt;unityid&gt;</code><br><span class="badge badge-red">1 GB Quota</span></td>
                                    <td>Scripts, small apps, dotfiles. Backed up daily.</td>
                                </tr>
                                <tr>
                                    <td><strong>Scratch</strong></td>
                                    <td><code>/share/doserlab/&lt;unityid&gt;</code><br><span class="badge badge-dark">20 TB Quota</span></td>
                                    <td>Job execution & raw results. <strong>Not backed up!</strong> Purged after 30 days inactive.</td>
                                </tr>
                                <tr>
                                    <td><strong>App Dir</strong></td>
                                    <td><code>/usr/local/usrapps/doserlab/jwdoser</code></td>
                                    <td>SEFS Lab shared software & R packages repository.</td>
                                </tr>
                                <tr>
                                    <td><strong>Research</strong></td>
                                    <td><code>/rs1</code> or <code>/rsstu</code><br><span class="badge badge-dark">2TB - 30TB</span></td>
                                    <td>Long-term project data storage across nodes.</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>

                <!-- Connection & File Transfer -->
                <div class="card">
                    <div class="card-header">2. Connection & Interactive SFTP</div>
                    <div class="card-body">
                        <table class="data-table">
                            <thead>
                                <tr>
                                    <th>Command</th>
                                    <th>Description</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr>
                                    <td><code>ssh &lt;id&gt;@login.hpc.ncsu.edu</code></td>
                                    <td>Log in to Hazel via SSH (requires Duo 2FA).</td>
                                </tr>
                                <tr>
                                    <td><code>sftp &lt;id&gt;@login.hpc.ncsu.edu</code></td>
                                    <td>Open interactive secure file transfer session.</td>
                                </tr>
                                <tr>
                                    <td><code>exit</code> / <code>Ctrl+D</code></td>
                                    <td>Safely terminate SSH or SFTP connection.</td>
                                </tr>
                                <tr>
                                    <td><code>hostname</code></td>
                                    <td>Identify current node (<code>loginXX</code> vs compute node).</td>
                                </tr>
                                <tr>
                                    <td><code>whoami</code> / <code>clear</code></td>
                                    <td>Print active UnityID / Clear terminal screen.</td>
                                </tr>
                            </tbody>
                        </table>
                        <div style="margin-top: 5px; font-weight: bold; font-size: 7.5pt; color: #7a0000;">Interactive SFTP Sub-commands (inside <code>sftp&gt;</code> prompt):</div>
                        <table class="data-table">
                            <tbody>
                                <tr>
                                    <td style="width: 42%;"><code>put &lt;local&gt; &lt;remote&gt;</code></td>
                                    <td>Upload file to HPC (add <code>-r</code> for folders).</td>
                                </tr>
                                <tr>
                                    <td><code>get &lt;remote&gt; &lt;local&gt;</code></td>
                                    <td>Download file from HPC (add <code>-r</code> for folders).</td>
                                </tr>
                                <tr>
                                    <td><code>lcd &lt;path&gt;</code> / <code>lpwd</code></td>
                                    <td>Change / print working directory on <strong>local machine</strong>.</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>

                <!-- Directory Navigation & File Management -->
                <div class="card">
                    <div class="card-header">3. Directory & File Operations</div>
                    <div class="card-body">
                        <table class="data-table">
                            <thead>
                                <tr>
                                    <th>Command</th>
                                    <th>Description / Key Options</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr>
                                    <td><code>pwd</code></td>
                                    <td>Print current full working directory path.</td>
                                </tr>
                                <tr>
                                    <td><code>cd &lt;path&gt;</code></td>
                                    <td>Change directory (<code>cd ~</code> home, <code>cd ..</code> parent).</td>
                                </tr>
                                <tr>
                                    <td><code>ls -ltr</code></td>
                                    <td>List files in long format sorted by modification time.</td>
                                </tr>
                                <tr>
                                    <td><code>mkdir &lt;folder&gt;</code></td>
                                    <td>Create a new directory (<code>rmdir</code> removes empty dir).</td>
                                </tr>
                                <tr>
                                    <td><code>nano &lt;file&gt;</code></td>
                                    <td>Command-line text editor (<code>Ctrl+X</code> to exit/save).</td>
                                </tr>
                                <tr>
                                    <td><code>cat &lt;file&gt;</code></td>
                                    <td>Print entire file contents to terminal screen.</td>
                                </tr>
                                <tr>
                                    <td><code>head -n 20 &lt;f&gt;</code></td>
                                    <td>Print first 20 lines of a file.</td>
                                </tr>
                                <tr>
                                    <td><code>tail -f &lt;f&gt;</code></td>
                                    <td>Print last 10 lines of a file (<code>-f</code> monitors live).</td>
                                </tr>
                                <tr>
                                    <td><code>less &lt;file&gt;</code></td>
                                    <td>Page through file line-by-line (press <code>q</code> to exit).</td>
                                </tr>
                                <tr>
                                    <td><code>grep "str" &lt;f&gt;</code></td>
                                    <td>Search pattern inside file (e.g. <code>ls | grep txt</code>).</td>
                                </tr>
                                <tr>
                                    <td><code>cp -r &lt;s&gt; &lt;d&gt;</code></td>
                                    <td>Copy file or directory (<code>-r</code> recursive).</td>
                                </tr>
                                <tr>
                                    <td><code>mv &lt;s&gt; &lt;d&gt;</code></td>
                                    <td>Move or rename a file or directory.</td>
                                </tr>
                                <tr>
                                    <td><code>rm &lt;file&gt;</code></td>
                                    <td>Permanently delete file (<strong>Warning: cannot undo!</strong>).</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>

                <!-- Storage Quotas & Environment Modules -->
                <div class="card">
                    <div class="card-header">4. Quota & Module Management</div>
                    <div class="card-body">
                        <table class="data-table">
                            <thead>
                                <tr>
                                    <th>Command</th>
                                    <th>Description</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr>
                                    <td><code>quota -s</code></td>
                                    <td>Display home directory quota and space used.</td>
                                </tr>
                                <tr>
                                    <td><code>quota_display</code></td>
                                    <td>NC State utility to check group scratch quota on <code>/share</code>.</td>
                                </tr>
                                <tr>
                                    <td><code>du -sh .</code></td>
                                    <td>Summarize total space used by current directory.</td>
                                </tr>
                                <tr>
                                    <td><code>module avail</code></td>
                                    <td>List all software modules available on Hazel.</td>
                                </tr>
                                <tr>
                                    <td><code>module load R</code></td>
                                    <td>Load specific module into active session (e.g. R, gcc).</td>
                                </tr>
                                <tr>
                                    <td><code>module list</code></td>
                                    <td>Show software modules currently loaded.</td>
                                </tr>
                                <tr>
                                    <td><code>module purge</code></td>
                                    <td>Unload <strong>all</strong> modules (best practice at start of scripts).</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>


                <!-- Slurm Directives -->
                <div class="card">
                    <div class="card-header red-accent">5. Slurm Batch Script Directives (#SBATCH)</div>
                    <div class="card-body">
                        <table class="data-table">
                            <thead>
                                <tr>
                                    <th>Directive Flag</th>
                                    <th>Description / Example</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr>
                                    <td><code>--job-name=&lt;name&gt;</code></td>
                                    <td>Name displayed in queue (e.g. <code>myjob</code>).</td>
                                </tr>
                                <tr>
                                    <td><code>--output=stdout.%j</code></td>
                                    <td>Standard output log file (<code>%j</code> = Job ID).</td>
                                </tr>
                                <tr>
                                    <td><code>--error=stderr.%j</code></td>
                                    <td>Standard error log file.</td>
                                </tr>
                                <tr>
                                    <td><code>--ntasks=1</code></td>
                                    <td>Number of tasks/processes (MPI ranks).</td>
                                </tr>
                                <tr>
                                    <td><code>--cpus-per-task=4</code></td>
                                    <td>Number of CPU cores per task (threads).</td>
                                </tr>
                                <tr>
                                    <td><code>--nodes=1</code></td>
                                    <td>Number of compute nodes requested.</td>
                                </tr>
                                <tr>
                                    <td><code>--time=04:00:00</code></td>
                                    <td>Wall clock limit (<code>HH:MM:SS</code> or <code>D-HH:MM:SS</code>).</td>
                                </tr>
                                <tr>
                                    <td><code>--mem=16G</code></td>
                                    <td>Memory per node (e.g., <code>16G</code> or <code>16000M</code>).</td>
                                </tr>
                                <tr>
                                    <td><code>--partition=compute</code></td>
                                    <td>Partition selection: <code>compute</code> (CPU) or <code>gpu</code>.</td>
                                </tr>
                                <tr>
                                    <td><code>--qos=normal</code></td>
                                    <td>QOS tier: <code>normal</code> (max 4 days) or <code>long</code> (max 10 days).</td>
                                </tr>
                                <tr>
                                    <td><code>--array=1-10</code></td>
                                    <td>Submit job array with task indices 1 through 10.</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>

                <!-- Sample Slurm Batch Script -->
                <div class="card">
                    <div class="card-header">6. Template Slurm Batch Script</div>
                    <div class="card-body">
                        <div class="code-block"><span class="comment">#!/bin/bash</span>
<span class="comment">#SBATCH --job-name=sefs_analysis</span>
<span class="comment">#SBATCH --output=stdout.%j</span>
<span class="comment">#SBATCH --error=stderr.%j</span>
<span class="comment">#SBATCH --ntasks=1</span>
<span class="comment">#SBATCH --cpus-per-task=4</span>
<span class="comment">#SBATCH --time=02:00:00</span>
<span class="comment">#SBATCH --mem=16G</span>
<span class="comment">#SBATCH --partition=compute</span>
<span class="comment">#SBATCH --qos=normal</span>

<span class="comment"># Explicitly switch to submission directory</span>
<span class="keyword">cd</span> <span class="var">$SLURM_SUBMIT_DIR</span>

<span class="comment"># Clean environment & load modules</span>
module purge
module load R

<span class="comment"># Execute R script</span>
Rscript ~/scripts/my_model.R</div>
                    </div>
                </div>

                <!-- Slurm Job Management -->
                <div class="card">
                    <div class="card-header red-accent">7. Slurm Job Management Commands</div>
                    <div class="card-body">
                        <table class="data-table">
                            <thead>
                                <tr>
                                    <th>Command</th>
                                    <th>Description</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr>
                                    <td><code>sbatch submit.sh</code></td>
                                    <td>Submit batch script to Slurm execution queue.</td>
                                </tr>
                                <tr>
                                    <td><code>salloc</code></td>
                                    <td>Start an interactive session on a compute node.</td>
                                </tr>
                                <tr>
                                    <td><code>srun &lt;exec&gt;</code></td>
                                    <td>Launch parallel job step (MPI) or command.</td>
                                </tr>
                                <tr>
                                    <td><code>squeue -u $USER</code></td>
                                    <td>View status (<code>ST</code>) of your queued/running jobs.</td>
                                </tr>
                                <tr>
                                    <td><code>sjs &lt;JOBID&gt;</code></td>
                                    <td>View live CPU %, RAM, and disk I/O for running job.</td>
                                </tr>
                                <tr>
                                    <td><code>scancel &lt;JOBID&gt;</code></td>
                                    <td>Cancel running job (<code>scancel -u $USER</code> cancels all).</td>
                                </tr>
                                <tr>
                                    <td><code>sacct -j &lt;JOBID&gt;</code></td>
                                    <td>View accounting details/exit state for completed job.</td>
                                </tr>
                                <tr>
                                    <td><code>seff &lt;JOBID&gt;</code></td>
                                    <td>Display CPU and memory efficiency utilization report.</td>
                                </tr>
                                <tr>
                                    <td><code>sa</code></td>
                                    <td>Show user account allocations and allowed QOS.</td>
                                </tr>
                                <tr>
                                    <td><code>sqos</code></td>
                                    <td>View QOS policies, priorities, and max wall time.</td>
                                </tr>
                                <tr>
                                    <td><code>si</code></td>
                                    <td>Show compute node availability across partitions.</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>

                <!-- Job States & Slurm Env Variables -->
                <div class="card">
                    <div class="card-header">8. Slurm States & Environment Variables</div>
                    <div class="card-body">
                        <table class="data-table">
                            <thead>
                                <tr>
                                    <th>Code</th>
                                    <th>State</th>
                                    <th>Meaning / Explanation</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr>
                                    <td><code>PD</code></td>
                                    <td>PENDING</td>
                                    <td>Waiting for requested cluster resources or QOS slot.</td>
                                </tr>
                                <tr>
                                    <td><code>R</code></td>
                                    <td>RUNNING</td>
                                    <td>Job is actively executing on allocated compute node(s).</td>
                                </tr>
                                <tr>
                                    <td><code>CD</code></td>
                                    <td>COMPLETED</td>
                                    <td>Job finished successfully with exit code 0.</td>
                                </tr>
                                <tr>
                                    <td><code>F</code> / <code>TO</code></td>
                                    <td>FAILED / TIMEOUT</td>
                                    <td>Non-zero exit code or exceeded requested <code>--time</code> limit.</td>
                                </tr>
                                <tr>
                                    <td><code>OOM</code></td>
                                    <td>OUT_OF_MEMORY</td>
                                    <td>Job process was killed for exceeding <code>--mem</code> limit.</td>
                                </tr>
                            </tbody>
                        </table>
                        <div style="margin-top: 5px; font-weight: bold; font-size: 7.5pt; color: #333;">Slurm Environment Variables (used inside scripts):</div>
                        <table class="data-table">
                            <tbody>
                                <tr>
                                    <td style="width: 45%;"><code>$SLURM_SUBMIT_DIR</code></td>
                                    <td>Directory path where <code>sbatch</code> was executed.</td>
                                </tr>
                                <tr>
                                    <td><code>$SLURM_ARRAY_TASK_ID</code></td>
                                    <td>Current task index for Job Array (e.g. 1, 2, 3...).</td>
                                </tr>
                                <tr>
                                    <td><code>$SLURM_JOB_ID</code></td>
                                    <td>Unique numeric ID assigned to the job.</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>

    </div>

</body>
</html>
"""


def create_slurm_cheatsheet_pdf(
    pdf_filename="ncsu_hpc_slurm_cheatsheet.pdf",
):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    if not os.path.isabs(pdf_filename):
        pdf_filename = os.path.join(script_dir, pdf_filename)

    # On Windows, make common MSYS2 runtime folders visible to the DLL loader.
    if os.name == "nt":
        candidate_dirs = [
            r"C:\msys64\mingw64\bin",
            r"C:\msys64\ucrt64\bin",
        ]
        for dll_dir in candidate_dirs:
            if os.path.isdir(dll_dir):
                if hasattr(os, "add_dll_directory"):
                    os.add_dll_directory(dll_dir)
                if dll_dir.lower() not in os.environ.get("PATH", "").lower():
                    os.environ["PATH"] = dll_dir + os.pathsep + os.environ.get("PATH", "")

    # Import WeasyPrint at runtime so missing native dependencies can be
    # reported with a clear action plan instead of failing at module import.
    try:
        from weasyprint import HTML
    except OSError as exc:
        raise RuntimeError(
            "WeasyPrint is installed, but required native GTK/Pango libraries are "
            "missing (e.g., libgobject-2.0-0).\n\n"
            "Windows fix:\n"
            "1) Install MSYS2 from https://www.msys2.org/\n"
            "2) Open MSYS2 UCRT64 shell and run:\n"
            "   pacman -S --needed mingw-w64-ucrt-x86_64-pango "
            "mingw-w64-ucrt-x86_64-gdk-pixbuf2 "
            "mingw-w64-ucrt-x86_64-cairo\n"
            "3) Add C:\\msys64\\ucrt64\\bin to your Windows PATH\n"
            "4) Restart VS Code/terminal and rerun this script\n\n"
            f"Original error: {exc}"
        ) from exc
    except ImportError as exc:
        raise RuntimeError(
            "WeasyPrint is not installed in this environment. Run: pip install weasyprint"
        ) from exc

    # Render HTML string directly into PDF (no intermediate .html output file).
    print(f"Generating PDF: {pdf_filename}", flush=True)
    try:
        HTML(string=HTML_CONTENT, base_url=os.getcwd()).write_pdf(pdf_filename)
    except PermissionError:
        stem, ext = os.path.splitext(pdf_filename)
        fallback_filename = f"{stem}_{datetime.now().strftime('%Y%m%d_%H%M%S')}{ext}"
        HTML(string=HTML_CONTENT, base_url=os.getcwd()).write_pdf(fallback_filename)
        pdf_filename = fallback_filename
        print(
            f"Main output was locked, so a new PDF was created instead: {pdf_filename}",
            flush=True,
        )

    file_size = os.path.getsize(pdf_filename)
    print(f"Successfully generated PDF: {pdf_filename} ({file_size:,} bytes)", flush=True)
    print("PDF compilation complete.", flush=True)


if __name__ == "__main__":
    try:
        create_slurm_cheatsheet_pdf()
    except RuntimeError as exc:
        print(exc, file=sys.stderr)
        raise SystemExit(1)