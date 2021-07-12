# gsuite-scripts
Administrative script to perform some tasks using google API. I created this script to do the following tasks.
1. Suspend a google workspace user.
2. Move the suspended user to a Terminated OU.
3. Remove the user from all the groups it was part of.

#Usage
To use this script, following steps are required to complete. 

1. you need download your seceret client file and rename it to client_secrets.json

2. Install all the required libraries to run the script \
   `pip install requirements.txt`

3. Run the script \
  `python admin.py`

4. Enter the user email address you want to perform functions to.
