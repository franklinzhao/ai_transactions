with open('task.txt', 'r') as file:
    file_contents = file.read()

# Now the content of the file is stored in the variable 'file_contents'
task_description=file_contents
print(task_description)