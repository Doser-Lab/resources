# How to use the NC State High Performance Computer (HPC)

**Author**: Michelle Pretorius (last edited 30 July 2026)

In this document, I will go over how to use Hazel, NC State's high performance computer (HPC). Note, this guide uses Slurm syntax (Hazel is *slowly* being migrated over to Slurm), whereas the previous guide used LSF syntax. Until Hazel has fully migrated, that guide may still be useful. 

## What is an HPC?

A High-Performance Computing (HPC) system is a network of powerful computers (called nodes) that work together to solve computationally intensive problems much faster, or that require more computational power, than a standard desktop or laptop computer.

### How does it work?

Think of an HPC like a factory assembly line rather than a single workbench:
+ **Login nodes**: Where you prepare your work (write scripts, organize files)
+ **Compute nodes**: Where the actual heavy computation happens (workhorse)
+ **Job scheduler**: The manager that assigns work to available compute nodes
+ **Storage systems**: Shared filesystems where all nodes can access your data

### NC State's Cluster

NC State's HPC cluster is officially called Hazel, though you'll also see it referred to as Henry2. Hazel represents the upgraded version of the cluster running modern software (RHEL 9.2 instead of the older CentOS 7.5). Both names refer to the same system, and you'll see both used in documentation (official NC State HPC tutorials) and when acknowledging the cluster in publications. The NC State HPC recently (as of mid-2026) migrated from LSF (Load Sharing Facility) to Slurm as its job scheduler. Therefore, it is important to note that some older documentation might still use LSF syntax.

> The Office of Information Technology (OIT) at NC State has some great [YouTube tutorials](https://www.youtube.com/@OITHPC) and [general documentation](https://hpc.ncsu.edu/main-slurm.php) on using the HPC, be sure to check them out too!

### Citing the HPC

If you have used the HPC at any stage in your research, you should acknowledge these compute resources in all works (thesis, publications, etc.): "*We acknowledge the computing resources provided by North Carolina State University High Performance Computing Services Core Facility* [RRID:SCR_022168](https://scicrunch.org/resources/data/record/nlx_144509-1/SCR_022168/resolver?rrid:scr_022168)."

### Key terms to know 

| Category | Term | Definition |
| :--- | :--- | :--- |
| **Infrastructure** | Cluster | The entire HPC system consisting of many connected computers |
| | Node | A single computer within the cluster |
| | Login node | The computer you connect to when you SSH into the HPC (for preparing work only) |
| | Compute node | Nodes where your actual computations run |
| | Core/CPU | Individual processing unit within a node (modern nodes have 8–32+ cores) |
| | GPU | Graphics Processing Unit, specialized for parallel calculations |
| **Job Scheduling** | Job | Computational task you submit to run on the cluster |
| | Batch job | Job that runs without user interaction using a script |
| | Interactive job | Job where you can type commands in real-time |
| | Queue | Waiting line for jobs before they run |
| | Batch/shell script | File containing instructions for what your job should do |
| | Wall time | Maximum real-world time your job is allowed to run |

## Storage

There are several different places on Hazel that are available for keeping files. These have different amounts of space available and different intended purposes.

### Home Directory
When you initially connect to Hazel, your working directory is your home directory `/home/user_name` (or shorthand `~`). **There is a 1GB quota!** Your home directory should be used only for storing scripts, small applications, and temporary files needed by the scheduling system to run your jobs. Your home directory is backed up daily to another data center.

### Scratch Directory
There is a 20TB scratch directory quota. The scratch directory is where data for running jobs and results are stored. Your scratch directory is located at `/share/group_name/user_name`. You can find your group name with the command `echo $GROUP`. Jobs should be submitted from `/share` or written in such a way that they by default read/write to `/share`. Any important files should be moved at the end of a run. 
> Scratch space is not backed up, and files not accessed for 30 days are automatically deleted. 

### Application Directory
If you (or your group) are installing your own applications, they should be kept in the application directory (unless they are small enough to fit in your home directory). Each project may request an application directory. As part of the SEFS Lab, we have a shared directory for commonly used software/packages (`/usr/local/usrapps/doserlab/jwdoser`). This allows us to use software that other members have downloaded, which can save us a lot of time/trouble in the long run. See the `software_on_hpc` document for how to set this up. 

### Research Storage

Research storage is accessible from all Hazel nodes via `/rs1` or `/rsstu` The recommended workflow is to copy data from Research Storage to your scratch directory at the beginning of your job script. Then, at the end of your run, copy results back from your scratch directory to Research Storage. This storage must be requested, and generally starts at 2TB, but you can request up to 30TB. 

## Requesting Access

To use the HPC, a faculty member must first request a project. Students may then be added to a project by their faculty advisor. Graduate students, postdocs, and other collaborators must be added to a project by their faculty PI.

## Required software

You can connect to the HPC using a web-based interface (e.g., Open OnDemand) or through a terminal window on your computer. 

+ **Built-in IDE Terminals**: Platforms like RStudio and Visual Studio Code have built-in terminal panels and native text editors, making it easy to create, edit, and run scripts on the HPC all in one place.
+ **Windows**:
    + Windows Terminal/PowerShell: Pre-installed on Windows 10/11. Simply search for "Terminal" or "PowerShell" in your start menu and open it.
    + MobaXterm (recommended by NC State): Download and install the [MobaXterm Home Edition](https://mobaxterm.mobatek.net/download-home-edition.html) (Installer edition). Provides an SSH terminal alongside a graphical drag-and-drop file browser.
+ **macOS/Linux**: No extra software needed, just search for and open the built-in "Terminal" app.

## Connecting to Hazel

To connect to the shared HPC login nodes via a secure shell (ssh), open a terminal window and type:
```
ssh <user_name>@login.hpc.ncsu.edu          # <user_name> is your NC State UnityID
```

You will then have to supply your password (same as with all UnityID logins), and then you will be asked to complete a Duo two-factor login, which can be done either by receiving a Duo Push (usually option 1) or SMS passcode (option 2). Annoyingly, if you supplied the wrong password, you will only find out *after* the Duo verification, and you will then have to do it all again. 

Once you have successfully logged in, you will see welcome and/or warning messages at the top of the terminal. **Take note of any planned outages that might impact your work!** At the bottom-left of the screen, you should see that you are no longer logged into your computer but rather logged into a login node part of NC State's Hazel cluster: `[ user_name@loginXX ~ ]`, where XX is the reference ID of the specific login node, and ~ is shorthand for your home directory.

> Hazel can only be accessed when connected to university Wi-Fi (eduroam). If you want to access the cluster from home, then a virtual private network (VPN) is required. NC State provides a VPN connection through the [Cisco Secure Client](https://ncsu.service-now.com/sp?id=kb_article_view&sysparm_article=KB0018300) software.

## Logging out of Hazel

When you are finished working on Hazel, simply type `exit` in your terminal window and press **Enter** (or press `Ctrl` + `D`). This safely closes your SSH connection and returns you to your local computer's command prompt. The cluster will also automatically log you out after a period of inactivity to free up resources.

## Organizing and transferring files

There are a few ways to move files to or from Hazel:

1. **Terminal window**: From a terminal window the `sftp` command can be used to transfer files between your local computer and Hazel.
    + SFTP (Secure File Transfer Protocol) is a network protocol for transferring files using your terminal window. Like logging into the HPC, you also need to log in to SFTP: `sftp <user_name>@login.hpc.ncsu.edu`. Again, you will be prompted for your password and to complete a Duo verification. You will know you are in when you see `sftp >`. What's nice about SFTP is that it uses the same Linux commands we use with the HPC, such as `pwd`, `ls`, `mkdir`, `cd`, etc. See the table at the end for all basic/essential Linux commands needed to work on the HPC.
    + You can interact with your local computer by adding `l` before commands, e.g., `lpwd Desktop/` will print to your local desktop:

    ```
    sftp> lpwd Desktop/
    Local working directory: /home/user_name/Desktop
     
    sftp> pwd 
    Remote working directory: /home/user_name
    ```
    + To exit SFTP, we use the command `bye`.
    + **Local to Remote**: To move files from your local machine to the HPC, we use the command `put <local> <remote>`, i.e., command followed by your local directory and then remote directory:
        ```
        sftp> put ./data_for_hpc/data_file.txt ./
        ```
       + This will move "`data_file.txt`" from your local machine to the current working directory on the HPC (`./`), or you could specify a specific directory in the HPC.
       + You can also copy entire folders using `put -r <local> <remote>`
    + **Remote to Local**: To move files the other way, i.e., to move model outputs from the HPC to your local machine to continue analyses, we use the command `get <remote> <local>`.

2. **Web browser**: [Globus](https://app.globus.org) is the preferred tool to use for moving larger files. It can restart interrupted network sessions and compute a checksum at the end of the transfer to ensure the data was moved correctly. The location you are moving data to/from will need to be connected to a Globus Connect Server or have [Globus Personal Connect](https://www.globus.org/globus-connect-personal) installed.
    + Go to the [Globus web app](https://app.globus.org), look up your organization (e.g., North Carolina State University). You will once again be prompted to log in with your university credentials and complete a Duo verification. Once completed, you will see a Windows-style web interface.
    + In the collection, search for "NC State Hazel HPC Cluster", and continue with your university credentials or Unity ID. This will open the contents of your home directory once again, i.e., the Path should be `/home/<user_name>/`. If not, you can navigate to your home directory by clicking on select folders.
        + Rename folders/files on the cluster by right-clicking on the folder/file, or by pressing the "**Rename**" button
        + Delete folders/files on the cluster by pressing the "**Delete**" button
        + Upload files from your computer to the cluster by pressing the "**Upload**" button, and then directly selecting files on your local machine.
        + Download files from the cluster by pressing the "**Download**" button, and this will initiate a regular web download into the Downloads folder of your local machine.
        + Navigate between folders by either editing the pathname or by clicking on the different folders.
    + Globus transfers between endpoints:
        1. Under the "**File Manager**" tab, select "**Set two panes**" in the top right corner.
        2. Then, in the second pane, you can search for "NC State Google Drive Connector" in the path search bar. You may need to do some additional authentication. You should see the home directory of your university's Google Drive in the right pane.
            + You can also connect to folders on your local machine by downloading the [Globus Personal Connect](https://www.globus.org/globus-connect-personal) app which will allow Globus to connect to your computer.
            + If downloaded, you will see an icon in the menu bar at the bottom of your screen. You can right-click and select "**Web: Transfer Files**", which will take you straight to the two Globus panes for transferring files. You can then connect the second pane to the HPC by searching for "NC State Hazel HPC Cluster" again.
        3. In both panes, navigate to where the file/folder that you want to transfer is located, and the folder/path where you want the file/folder to be transferred to.
        4. Select the "**Start**" button on the pane that contains the file/folder you are transferring. E.g., if you are transferring a file from the HPC, you would press "**Start**" on the panel connected to the HPC. 
        5. This creates a "Transfer Task" which can be monitored in the "Activity" tab to the right. You will also receive an email notification when the task is complete.  

## Basic job scripts

Each time you want to run something on the HPC, you would follow very similar job submission steps:

1. Create/modify your batch script. This is a text file that contains the information necessary for the job scheduler to reserve the resources you need, as well as the actual lines of code that you are trying to run (or a command/directory for where to source your code)
2. Navigate to job submission (scratch) directory (usually `/share/$GROUP/$USER`). This is a location used for rapid reading and writing.
3. Submit job using `sbatch [name of batch script].sh`
4. Check on job progress using `squeue -u $USER`
5. Examine outputs

### Step 1. Create/modify batch script

Start by creating a batch/shell script in your desired directory: `nano ~<path>/submit.sh`. You can also create shell scripts in any text editor (just save with a ".sh" extension), and transfer this file to the HPC.

Within your batch script, you would specify the following information:

```
#!/bin/bash 

#======================================================
# Job name and output files
#======================================================
#SBATCH --job-name=myjob           # Job name
#SBATCH --output=stdout.%j         # Standard output (%j = job ID)
#SBATCH --error=stderr.%j          # Standard error

#======================================================
# Resource requests
#======================================================
#SBATCH --ntasks=4                 # Number of tasks (MPI ranks)
#SBATCH --cpus-per-task=1          # CPUs per task (OpenMP threads)
#SBATCH --nodes=1                  # Number of nodes
#SBATCH --time=02:00:00            # Time limit (HH:MM:SS)
#SBATCH --mem=4G                   # Memory per node

#======================================================
# Partition and QOS (optional - uses defaults if omitted)
#======================================================
#SBATCH --partition=cnr           # Partition name (compute = everyone)
#SBATCH --qos=normal              # Quality of Service

#======================================================
# Environment setup
#======================================================
module purge                       # Clear modules
module load R                      # Load compiler environment

#======================================================
# Change to submission directory (optional)
#======================================================
cd $SLURM_SUBMIT_DIR

#======================================================
# Run script/application
#======================================================
Rscript /path/to/script.R          # Need to include Rscript command
# OR:
./myprogram.exe

# For MPI programs, use srun:
# srun ./my_mpi_program.exe

```

The first line of the batch script, like all shell scripts, always starts with a shebang line, because it starts with a `#!`, followed by the shell, which is what you will use to run all your commands on the cluster, which is `/bin/bash`, i.e., the location of the bash shell executable.

The next few lines, starting with `SBATCH`, specify job parameters for the job scheduler Slurm. For example:
+ `--job-name` sets the job name displayed by `squeue`.
+ `--output` and `--error` specify where `stdout` and `stderr` are written. `%j` is a job ID placeholder, which will be replaced with the actual numeric job ID. This prevents different job runs from overwriting each other’s output.
+ `--ntasks` requests CPU cores. If you are running a serial job, you would specify 1 core. Parallel jobs will need more cores (>1). For example, specifying `--ntasks=4` requests 4 cores while `--nodes=1` ensures all 4 tasks run on the same node. 

    > You need to make sure that your job doesn't use more cores than what you specify, as this can lead to issues with jobs not having the necessary resources (because it is being secretly used by another node/job).

+ `--time=02:00:00` sets the time needed to complete your job. This can be in HH:MM:SS (`--time=02:00:00`) or D-HH:MM:SS (`--time=1-00:00:00`). Once the time "runs out" your job will be shut down regardless of whether it is finished or not. 
+ `--mem=4G` requests 4 GB of memory per node. Note that Slurm supports suffixes (`--mem=16G`, or `--mem=16000M`). Slurm defaults to a baseline memory allocation per core if omitted (usually 2GB per task on Hazel)
+ `cd $SLURM_SUBMIT_DIR`: This is more of a safety net. Slurm automatically runs jobs from the directory where you executed `sbatch`. If you follow the steps set out in this guide, you should always be executing `sbatch` in your scratch directory. This line *explicitly* ensures your job always executes in the scratch/submission directory, regardless of where you execute `sbatch`.

#### Environment setup
This is where you load in environmental modules or read in certain config files. Setting up your environment will commonly (but not always) involve modules that have been set up by the HPC staff. These are really helpful, and mean you don't have to maintain these modules yourself. However, sometimes these maintained modules can conflict with what you are working on. If that happens, then you can create these yourself using something like `conda`. However, using a conda environment can lead to path conflicts between modules, so be careful with that!

> You load modules to your HOME directory (NOT the job submission (shared/scratch) directory)

Some environmental module commands:
+ `module list`: Check which modules are currently loaded
+ `module avail`: Check which modules are available to be loaded
+ `module load <module_name>/<version>`: Loads in a specific module (note version is *optional*)
+ `module unload <module_name>`: Unloads a currently loaded module
+ `module purge`: Unloads ALL currently loaded modules

Loading in modules is required to add specific directories to your path, e.g., you need to load in R as a module before you can use it: 

First, try running R before the module is loaded:
```
R
-bash: R: command not found
```

Load the R module:
```
module load R
```

Run R again
```
R 

R version 4.3.2 (2025-12-05) -- "Hypothetical Example" 
Copyright (C) 2025 The R Foundation for Statistical Computing
Platform: x86_64-pc-linux-gnu (64-bit)
```
Now you are in a working R console, e.g., 

```
1 + 1

[1] 2
```

You can install any R packages you may need:
```
install.packages("spOccupancy")
```

Use `quit` to exit your R console:
```
quit

Save workspace image? [y/n/c]:
```

> As part of the SEFS Lab, we have a shared directory for commonly used software/packages (`/usr/local/usrapps/doserlab/jwdoser`). Installing R packages with a lot of dependencies can very quickly fill up your home directory space. These shared application directories help avoid this! You can check which packages have already been installed typing `ls /usr/local/usrapps/doserlab/jwdoser/R_Packages`. See the `software_on_hpc` document, also available of the SEFS lab GitHub, on how to add this directory. 

It is generally recommended that you limit the number of packages in any script run through the HPC, i.e., do your data wrangling on your local machine (using `dplyr`, `sf`, etc.), and then just load your formatted data (`.rda`) to the HPC. 

If you want to use a development package, or a package downloaded from GitHub, then you need to move the package folder onto the HPC and then install them from source. Usually, outside of the HPC, I would use `devtools` to load in my dev packages, but devtools is a pain on the HPC given all its dependencies, and so the best alternative is `remotes`. Note, the package folder or `tar.gz` file must be moved onto the HPC. 

```
# Load the R module
module load R

# Run R again
R

# If you need to install remotes:
install.packages("remotes", repos = "https://cloud.r-project.org") 

# If your package is a folder:
remotes::install_local("/path/to/folder", dependencies = TRUE) 

# If your package is a .tar.gz file: 
remotes::install_local("/path/to/tar.gz", dependencies = TRUE)
```

### Step 2. Job submission directory

Next, we must navigate to our job submission (scratch) directory: `cd /share/$GROUP/$USER`. 

> For Dr Doser's lab, we can specify: `cd /share/doserlab/<user_name>`, where `<user_name>` is your NC State UnityID. 

If you want to make a sub-directory/folder within this scratch directory (which makes it easier to keep track of jobs/outputs), use: `mkdir <folder_name>`

### Step 3. Submit a job

Now, we can submit our job using `sbatch ~<path>/submit.sh`. As our scratch directory has a limited lifespan, it's generally recommended to save your scripts in your home directory (remember, `~` is shorthand for your home directory). If you have saved your scripts in the scratch directory, then remove the ~, but remember, scratch space is not backed up, and files not accessed for 30 days are automatically deleted!

```
sbatch ~<path>/submit.sh
    
Submitted batch job XXX
```

Note that your default memory is 2GB per task, which translates to 2GB per core that you reserve. If you want to reserve more memory per task (e.g., 10GB), you can specify this in your batch/shell script with `#SBATCH --mem=10G`

> **Tip:** Once `sbatch` returns a job ID (e.g., `Submitted batch job 123456`), it is managed entirely by Slurm on the compute nodes. You do not need to keep your terminal open or stay logged in for the job to keep running.

### Step 4. Job progress

You can check on your job progress using `squeue -u $USER`, this will print general information about the job(s) currently running:

```
squeue -u $USER

 JOBID  PARTITION  NAME     USER      ST   TIME   NODES  NODELIST 
 12345  standard   my_job   unityID   R    0:45   1      c001n01 

```

| Job state (`ST`) | Code | Description |
| :--- | :--- | :--- |
| `PENDING` | `PD` | Waiting for resources or dependencies |
| `RUNNING` | `R` | Currently executing |
| `COMPLETING` | `CG` | Finishing up (epilog running) |
| `COMPLETED` | `CD` | Finished successfully (exit code 0) |
| `FAILED` | `F` | Finished with non-zero exit code |
| `TIMEOUT` | `TO` | Exceeded time limit |
| `CANCELLED` | `CA` | Canceled by user or admin |
| `NODE_FAIL` | `NF` | Node failure during execution |
| `OUT_OF_MEMORY` | `OOM` | Exceeded memory limit |

You can pair additional tags with `squeue` (after `JOBID`) to get more information about a job:
    
+ `-a` Job in all states, including jobs that finished recently.
+ `-d` Only jobs that finished recently.
+ `-r` Only running jobs.
+ `-l` Long format, i.e., multi-line format.
+ `-o` "output format"

```
squeue -u $USER -o "%.10i %.9P %.20j %.8u %.2t %.10M %.6D %R"

    JOBID PARTITION                 NAME     USER ST       TIME  NODES REASON
    123456   compute             analysis  unityID PD       0:00      4 (Priority)
    123457   compute           preprocess  unityID PD       0:00      1 (Resources)
```

The long string after `-o` tells `squeue` exactly what to display for each column and column widths (for easier visualization). 

We can see both our jobs are currently pending (`ST` = `PD`). Common pending reasons include:

| Reason |	Meaning	| What to do |
| :--- | :--- | :--- | 
| Priority |	Other jobs have higher priority	| Wait; use short QOS for jobs under 2 hours |
| Resources |	Waiting for requested resources	| Wait; consider reducing resource request |
| QOSMaxCpuPerUserLimit |	Hit your CPU limit for this QOS | Wait for running jobs to finish |
| QOSMaxJobsPerUserLimit | 	Hit your job count limit | Wait for running jobs to finish |
| AssocGrpCPURunMinutesLimit | 	Account allocation exhausted | Contact HPC support | 

`squeue` only shows that a job is running, not whether it is doing any work. Use `sjs` to see live CPU, memory, and disk usage:

```
sjs [JOBID]

    [JOBID]  unityID, RUNNING, elapsed 4:44:21
    alloc: cpu=12,mem=48000M,node=1,billing=23 

    Step             NTasks  AveCPU    %CPU   MaxRSS   %Mem   MaxDiskRead    MaxDiskWrite
    [JOBID].batch    1       04:55:28  9%     9.24G    20%   181.72G        235.09G 
```

Here `%CPU` of 9% means the job is using about 1 of its 12 requested cores. Add `-r` to resample and watch what changes, which is how you tell a busy job from a stuck one.


### Step 5. Cancel a job

+ Use `scancel JOBID` with the job ID to cancel a single job
+ Use `scancel -u $USER` to cancel ALL your jobs (associated with your UnityID)

### Step 6. Examine outputs

We can now explore the various outputs from our run:

+ Standard output and job details (`stdout.[JOBID]`), which will include information such as which directory was used, start date/time, end/terminate date/time, and some resource usage summaries (i.e., CPU time, average memory, etc.)
+ Job errors (`stderr.[JOBID]`), which will be empty if everything ran correctly, or will contain error messages which can be used to debug/fix your batch or R script. 
+ Script outputs/products such as `.rda` from a model, etc.
    + Remember, your scratch space is not backed up, and files not accessed for 30 days are automatically deleted. Therefore, it is good practice to download or move outputs to research storage after a successful run.

## More complex job scripts

When running large models, you’ll often hit a RAM ceiling. Instead of forcing one massive job to run three chains (e.g., `n.chains = 3` in R), it’s much more efficient to run three *independent* jobs. You could submit these manually, but using **Job Arrays** can do the heavy lifting for you by automating the submission and naming process. 

For example:
```
#!/bin/bash 
#SBATCH --job-name=my_array
#SBATCH --output=output_%A_%a.out           # %A = array job ID, %a = task index
#SBATCH --error=error_%A_%a.err
#SBATCH --array=1-3                         # Create 3 tasks with indices 1-3
#SBATCH --ntasks=1
#SBATCH --time=04:00:00
#SBATCH --mem=32G

module load openmpi-gcc
module load R

Rscript ~/model_script.R ${SLURM_ARRAY_TASK_ID}
```

You can see a couple of changes to this batch script compared to our basic batch script:
+ `--array=1-3` tells Slurm, "I want three versions of this job, indexed 1, 2, and 3."
+ `_%A_%a` acts as a placeholder. Slurm swaps it for the index number so your logfiles stay organized and don’t overwrite each other: `%A` = master array JOBID (e.g., `123456`), `%a` = array task index (e.g., `1`, `2`, or `3`)
+ `$SLURM_ARRAY_TASK_ID` is an environment variable that Slurm "plugs into" your R command. For the first job, it becomes 1; for the second, 2, and so on.

| Variable | Description | Example Value |
| :--- | :--- | :--- |
| `$SLURM_ARRAY_JOB_ID` | Main array job ID | `123456` |
| `$SLURM_ARRAY_TASK_ID` | Current task index | `42` |
| `$SLURM_ARRAY_TASK_COUNT` | Total number of tasks | `100` |
| `$SLURM_ARRAY_TASK_MIN` | Minimum task index | `1` |
| `$SLURM_ARRAY_TASK_MAX` | Maximum task index | `100` |


Now in your R script, you would have the following lines of code at the top of your script:
```
args <- commandArgs(trailingOnly = TRUE)

if (length(args) == 0) { 
    chain_idx <- 1
    } else {
    chain_idx <- as.numeric(args[1])
    }

set.seed(123 + chain_idx)
```

This allows the script to be "self-aware", i.e., it knows which part of the task it is performing based on what the HPC tells it.
+ `args <- commandArgs(trailingOnly = TRUE)` This captures any text you type after `Rscript model_script.R` in your batch script (i.e., the `$SLURM_ARRAY_TASK_ID` we passed from the batch script.).
+ `chain_idx <- if(length(args) > 0) as.numeric(args[1]) else 1` This is a bit of "safety" code. It grabs the index number from the HPC, but if you're just testing locally, it defaults to 1 so the script doesn't crash.
+ `set.seed(123 + chain_idx)` This is the most important part. By shifting the seed based on the chain ID, you ensure each job explores the posterior from a different starting point, maintaining statistical independence for your Bayesian model.

## Essential commands

### Slurm job management

| Command | Description |
| :--- | :--- |
| `sbatch script.sh` | Submit a batch script to the Slurm execution queue. |
| `squeue -u $USER` | View the status (`ST`) and details of all your queued/running jobs. |
| `scancel <JOBID>` | Cancel or terminate a running or pending job. |
| `si`	| Show node availability by partition and architecture |
| `si --nodes --partition compute` | Show detailed resource availability for given partition |
|  `sacct -j JOBID` | View completed job details |
| `salloc` | Start an **interactive session** on a compute node. |
| `sinfo` | Show all available partitions on the cluster or check which ones you have access to (e.g., `cnr`) |
| `srun` | Run parallel tasks |
| `seff JOBID` | Job efficiency report |


### General Linux commands

| Command | Description |
| :--- | :--- |
| `ssh` | Secure shell used to log in and communicate with remote machines. |
| `clear` | Clear your terminal screen (shortcut: `Ctrl` + `L`). |
| `whoami` | Print your username. |
| `hostname` | Print system/node name — essential for identifying if you are on a **login node** or **compute node**. |
| `pwd` | Print working directory (where you currently are). |
| `echo` | Display a line of text or variable value (e.g., `echo $GROUP` or `echo $USER`). |
| `man` | Open the command manual (e.g., `man pwd`). Press `q` to exit. |
| `exit` | Log out of the HPC (jobs will keep running). You will also be automatically logged out after a certain period of inactivity. |

### Working with directories

| Command | Description |
| :--- | :--- |
| `ls` | Show contents of a directory. Common flags:<br> `-l`: long format (shows permissions, owner, size)<br> `-h`: human-readable sizes (KB/MB/GB)<br> `-t`: sort by modification time (newest first)<br> `-r`: reverse sorting order (e.g., `-tr` shows oldest first) |
| `grep` | Search for text or regular expressions.<br> Example: `ls \| grep txt` lists files in the current directory containing "txt". |
| `mkdir` | Create a new directory. |
| `cd` | Change directory. Tab key auto-completes names.<br> `cd .` Refers to the current directory.<br> `cd ..` Move up to the parent directory. |
| `rmdir` | Remove an empty directory (will throw an error if files exist inside). |


### Working with text files
*Note: Most commands require a target file: `<command> <file_name>`*

| Command | Description |
| :--- | :--- |
| `nano` | Simple command-line text editor.<br> **Ctrl + X**: Exit (press **Y** then **Enter** to save changes) |
| `cat` | Print entire contents of a file directly to the terminal. |
| `head` | Print the first 10 lines of a file. |
| `tail` | Print the last 10 lines of a file. |
| `less` | Open a file to navigate through page by page. Press `q` to exit. |
| `mv` | Move or rename a file (e.g., `mv <old_name> <new_name>`). |
| `cp` | Copy a file. Add `-r` to recursively copy an entire directory. |
| `rm` | Permanently delete a file (**Warning:** cannot be undone!). |


### Storage management

| Command | Description |
| :--- | :--- |
| `quota` | Display available user storage limits.<br> `-s`: Human-readable format (KB/MB/GB)<br> `-g <group_name>`: Check quota for your specific research group |
| `du <path>` | Check disk usage of a directory/path to see what files are taking up space.<br> `-s`: Summarize total size<br> `-h`: Human-readable format (e.g., `du -sh .`) |