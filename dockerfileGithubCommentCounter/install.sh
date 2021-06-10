#! /bin/bash

# Link to github-comment-counter version
version=https://github.com/tzachz/github-comment-counter/releases/download/V0.1.61/leaderboard-server-0.1.62.zip

# Download the release
mkdir -p /tmp/release
cd /tmp/release
wget -O githubCommentCounterRelease.zip https://github.com/tzachz/github-comment-counter/releases/download/V0.1.61/leaderboard-server-0.1.62.zip
unzip githubCommentCounterRelease.zip
rm -f githubCommentCounterRelease.zip
mv leaderboard-server* leaderboard-server

# Move to the /application folder
mkdir /application
mv /tmp/release/leaderboard-server/* /application
mkdir /application/config

# Remove release
rm -rf /tmp/release