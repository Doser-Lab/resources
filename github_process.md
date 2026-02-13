# Process for Collaborative Coding on GitHub and Git

**Author**: Jeff Doser (last edited 13 February 2026)

In this document, I will go over my suggested approach for using GitHub as a permanent archive for your research projects. Regardless of whether you are working on a project that does involve collaborative coding or not, using Git and GitHub as a version control system is very good practice. This will help you if you ever lose access to your work locally on your machine, and also provides an easy way for you to keep different versions of code for you to return to at a later date. I've adapted a good chunk of this from the [Zipkin Lab](https://github.com/zipkinlab) as well as the [Atlassian Feature Branch Workflow.](https://www.atlassian.com/git/tutorials/comparing-workflows/feature-branch-workflow).  

Note that Git and GitHub have a lot of specific terminology and I won't define all of the technology here. If you're confused about the terminology, a simple google search almost always quickly resolves the answer. 

## Lab Repository

All research projects that involve some level of data analysis performed in the SEFS Lab that result in a peer-reviewed manuscript should be publicly available in an individual respository housed in the Doser Lab GitHub organization. There are certain exceptions to this (i.e., if code is developed for a proprietary project or piece of software, a paper does not involve any code/data analysis). Providing well-documented code needed to reproduce analyses in a paper in a GitHub repository makes it easy to provide manuscript reviewers/journal editors with the opportunity to review the code.  

## Keeping an Organized Directory Structure

Staying organized on your computer is crucial for avoiding errors in data analysis and for ensuring reproducibility of your work. I have found success using a standardized directory structure for all of my research projects. I strongly suggest you to use a similar structure and maintain consistency with that structure over time. Of course, when you first begin you will likely refine the directory structure in different ways, which is certainly okay, but after a bit of tinkering you should strive to keep the same directory structure across different projects. 

For every research project I am involved with, I have an individual directory (i.e., folder) on my computer where all files for that project are stored. You should name this project something that makes clear to you what the project is about. My approach is to name all projects based on the first initial of all co-authors of a project, followed by the last two numbers of the year during which I started the project. So, for example, the folder name for a project I started in 2025 where I was the first author and Bob Smith was the second author would be called `DS25`. I like this approach for naming projects and directories, but if you have a different way you'd like to name your projects, that is totally fine by me.  

Inside of my project folder, I have the same structure of folders/files. The general structure I use (and recommend you do as well) is the following: 

+ `code`: directory to store all code associated with a project. 
+ `data`: directory to store all data files associated with a project. 
+ `documents`: directory to store all documents (e.g., relevant papers, scratch notes, meeting notes) associated with a project
+ `figures`: contains all figures produced in the manuscript. 
+ `results`: all results files associated with a manuscript. 
+ `README.md`: a markdown file that describes in detail the contents of the directory. See the `Doser_et_al_2026_AF_SAE` manuscript in this repository for an example of the README structure. 
+ `.gitignore`: a simple text file that tells Git and GitHub what files to ignore and not upload.  

Creating this folder on your computer is the first step I would suggest doing when you are beginning a new research project. You can change the name of the directories from what I use (e.g., many people use `docs` instead of `documents` or `src` instead of `code`).  

## GitHub Authentication

Before you do anything with GitHub, you will need to setup some form of authentication. See [here](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/about-authentication-to-github#authenticating-with-the-command-line) for how to go about doing that. I use personal access tokens and find that approach to be relatively pain free. 

## Creating a GitHub Repository

Once you have created your local project directory on your computer, you can then create a repository on GitHub. Go to GitHub and create a new repository in the Doser-Lab group. Call the repository the same thing as what you named your project directory on your computer. When you create the repository on GitHub, you will see different settings for the repository. The main one to consider is whether or not you make the repository public or private. Whether or not a repository is private or public will depend on the specific project. If there are no data privacy concerns, you should make the repository public. If there are, then you can make the repository private, or you can make the repository public and you would just need to ensure that you do not upload any data to GitHub. Making sure you don't *ever* upload the data to Git/GitHub is vital. If you do so once, then you would have to go back and delete the data from multiple locations, which can be challenging and very difficult. This is true even if the repository is private for a while and then you plan to eventually make the repository public. To avoid errors, do not initialize the repository with README, license, or gitignore files. 

Creating the repository on GitHub does not actually create the version control system for keeping track of your files, but rather initiates the location on GitHub where you eventually will put all of your code. The next step then is to initialize your local directory as a Git repository, and then you will use Git to add your repository to GitHub. This is all done via the terminal. On Windows machines, you have two options for using the terminal: (1) use the terminal through RStudio (probably the easier option); (2) download some terminal designed explicitly for Windows (I have had the most success with MobaXterm).   


## Initializing your local directory as a Git Repository

1. Open up the terminal window in the application of your choosing (e.g., RStudio or MobaXterm).  
2. Navigate to the root directory of your project. You can do this with the `cd` command. Note that if you are using RStudio and you create an RStudio Project for your project directory, you should automatically have started in the right spot. 
3. Initialize the local directory as a Git repository. By default, the initial branch is called `main`. Git uses the terms `branch` to refer to different lines of development, which allows developers to diverge from the main codebase, work on new features or bug fixes in isolation, and then experiment without affecting the stability of the main project code. As I will talk about a bit later, it is often good practice to never really directly work with the `main` branch and instead work on individual branches designed for specific parts of a project. Execute the following code in the terminal to do this: 

```
git init -b main
```

At this point, your directory is now set up as a Git repository, so it is time to start adding in files. If you have set up your repository in the way that I outlined above and all the directories are empty, then there is nothing more to do. If you already have a bunch of files in the repository, you will want to add any files that you don't want to be uploaded to Git/GitHub into your `.gitignore` file. This is very important if: (1) you cannot post data publicly; (2) you have large (>50MB) results files; or (3) you have a bunch of documents in your directory that you don't want to share publicly (e.g., a notebook).  

Assuming your directory is mostly empty (or you've added in all the appropriate file names into the .gitignore document), the next step is to 

4. Add the files in your new local repository. This stages them for the first commit to Git. 

```
git add .
```

5. Commit the files that you've staged in your local repository. The text in the quotation marks is the label on the commit. Here it is just labeled as "First commit" but for future commits, you should label this with something that is more informative. 

```
git commit -am "First commit"
```

At this point, all of your files in the directory are now commited to Git, but next we need to sync to GitHub. 

## Adding local repository to GitHub using Git

1. At the top of your repository on GitHub's Quick Setup page, click the copy symbol to copy the remote repository URL. 
2. Open the Terminal. 
3. Change the current working directory to your local project (if needed)
4. To add the URL for the remote repository where your local repository will be pushed, run the following command. Replace `REMOTE-URL` with the repository's full URL on GitHub. 

```
git remote add origin REMOTE-URL
```

5. To verify that you set the remote URL correctly, run the following command: 

```
git remote -v
```

6. To push the changes in your local repository to GitHub, run the following command. 

```
git push origin main
```

Now go back to GitHub and you should see it now contains all of the code/files from your local directory!


## Git Feature Branch Workflow

The Git Feature Branch Workflow is my suggested approach for working with code on GitHub. If you use this approach for all your repositories, regardless of whether they are collaborative or not, your life will be a whole lot easier if you do end up working on a collaborative coding project. Note that this all comes from the [Atlassian workflow documented here](https://www.atlassian.com/git/tutorials/comparing-workflows/feature-branch-workflow). I'll provide a summary of the most important things to do, but see the tutorial for more complete details. 

The first step in the workflow is to ensure that you have the latest code from a project. If you have done work locally that you have not pushed up to GitHub, then you should `add`, `commit`, and `push` that work before beginning here. Then the first step is to run the following lines of code through the terminal. 

```
git checkout main
git fetch origin
git reset --hard origin/main
```

This changes the repository to the `main` branch, pulls the latest commits, and resets the repo's local copy of `main` to match the latest version. 

The next step is to create a new branch. I would suggest using a separate branch for each feature or component of the project you work on, or you could have a separate branch each week or two, then push the work you did for those couple of weeks up to GitHub. You can create and "checkout" to a new branch as follows

```
git checkout -b new-feature
```

where `new-feature` is the name of the branch. Note that this can be used to create the `new-feature` branch, or it can be used to move to the `new-feature` branch if it already exists.  

Once you have checked out to your new branch, you can update, `add`, `commit`, and `push` changes as usual. You can use `git status` to check the status of what you have done. To push changes from your new branch, you would use the following code

```
git push -u origin new-feature
```

where `new-feature` is the name of your branch. 

When you do this, a pull request will be created on GitHub, which you should then eventually merge on GitHub itself. 

After you've merged the pull request, you would then start back at the beginning of the feature branch workflow the next time you go to do any work on the project.  








