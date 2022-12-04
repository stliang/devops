
# As a Build and Release engineer, I want to find out which nodes a git repo uses for
# building so that I can move the build job and nodes to newer Jenkins server without
# breakig other jobs.

# First findout the agent labels used in Jenkinsfile of gitrepo

# Of the labels being used, which Jenkins agent / node has that label

# Of the nodes' other labels, which other build jobs use them

# Once we have those infomation, we can determine the impact of moving a node as a
# node can have multiple labels and thus used by multiple jobs



