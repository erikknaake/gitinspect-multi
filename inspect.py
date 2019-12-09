import json
import os
import subprocess

def gitInDir(dir, *args):
	arguments = list(args)
	arguments.insert(0, "-C")
	arguments.insert(1, dir)
	git(arguments)

def git(args):
	args.insert(0, 'git')
	print(args)
	return subprocess.check_call(args)

def readConfig():
	with open('config.json', 'r') as file:
		return json.load(file)

def updateBranch(repo, didPull):
	gitInDir(repo["dir"], "checkout", repo["branch"])
	if not didPull:
		gitInDir(repo["dir"], "fetch")
		gitInDir(repo["dir"], "pull")

def updateRepos(repos):
	for repo in repos:
		print("updating repo: " + repo["url"])
		doPull = not os.path.exists(repo["dir"])
		if doPull:
			git(["clone", repo["url"]])
		updateBranch(repo, doPull)

def runGitInspect(format, extensions, folder, outputLocation):
	command = ["python", "./gitinspector/gitinspector.py", "-F", format, "-f", extensions, folder]
	print (command)
	with open(outputLocation, "w") as outfile:
		subprocess.call(command, stdout = outfile)

def listToCommaSeperatedString(list):
	return ','.join(list)

def runInspectForRepo(config, repo):
	runGitInspect(config["format"], listToCommaSeperatedString(config["extensions"]), repo["dir"], "./out_" + repo["name"] + ".html")

def runInspect(config):
	for repo in config["repos"]:
		runInspectForRepo(config, repo)

def main():
	config = readConfig()
	updateRepos(config["repos"])
	runInspect(config)

if __name__== "__main__":
  main()