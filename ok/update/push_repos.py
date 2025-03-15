import sys

import os
import shutil
import stat
import subprocess

from ok.update.GitUpdater import remove_ok_requirements


def run_command(command):
    print(f'Running command: {command}')
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
                            encoding='utf-8')
    try:
        if result.returncode != 0:
            print(f"Warning: Command '{command}' failed with error:\n{result.stderr.strip()} \n{result.stdout.strip()}")
            raise Exception(f"Command '{command}' failed with error:\n{result.stderr.strip()}")
        return result.stdout.strip()
    except Exception as e:
        print(f"Warning: Command '{command}' failed with error:\n{e}")
        return ""


def on_rm_error(func, path, exc_info):
    os.chmod(path, stat.S_IWRITE)
    func(path)


def get_current_branch():
    return run_command("git rev-parse --abbrev-ref HEAD")


def get_latest_commit_message():
    return run_command("git log -1 --pretty=%B").strip()


def tag_exists(tag_name):
    tags = run_command("git tag").split('\n')
    return tag_name in tags


def remove_history_before_tag(tag_name):
    print(f"remove_history_before_tag {tag_name}")
    if tag_exists(tag_name):
        print(f"remove_history_before_tag tag_exists {tag_name}")
        run_command(f"git checkout {tag_name}")
        run_command(f"git checkout -b new-master")
        run_command(f"git checkout master")
        run_command(f"git reset --hard lts")
        run_command("git push --force origin master")


# def run_command(command):
#     result = subprocess.run(command, shell=True, check=True, text=True, capture_output=True)
#     print(result.stdout)
#     return result.stdout
#
# def remove_history_before_tag(tag_name):
#     print(f"Attempting to remove history before tag: {tag_name}")
#     if tag_exists(tag_name):
#         print(f"Tag {tag_name} exists")
#
#         # Reset to the tag
#         run_command(f"git reset --hard {tag_name}")
#
#         # Create a temporary rebase script file
#         with open('rebase-script.txt', 'w') as file:
#             file.write('pick' * (len(run_command('git rev-list --count --reverse HEAD..{tag_name}').strip().split(
#                 '\n')) - 1) + "\n")
#
#         # Run the rebase using the script
#         run_command(f"git rebase --root --autosquash -i --rebase-merges -s 'rebase-script.txt'")
#
#         # Clean up the temporary script file
#         os.remove('rebase-script.txt')
#
#         print("Finished rebase")
#         run_command("git filter-branch -- --all")
#         print("Finished filter-branch")
#         run_command(f"git push --force origin master")
#         print("Finished push")
#     else:
#         print(f"Tag {tag_name} does not exist")


def main():
    import sys

    if '--repos' not in sys.argv or '--files' not in sys.argv:
        print("Usage: python update_repos.py --repos repo1 repo2 ... --files file1 file2 ...")
        sys.exit(1)

    if '--tag' not in sys.argv:
        print("Usage: python update_repos.py --repos repo1 repo2 ... --files file1 file2 ... --tag tag_name")
        sys.exit(1)

    repos_index = sys.argv.index('--repos') + 1
    files_index = sys.argv.index('--files') + 1
    tag_index = sys.argv.index('--tag') + 1

    repo_urls = sys.argv[repos_index:files_index - 1]
    files_filename = sys.argv[files_index:tag_index - 1]
    tag_name = sys.argv[tag_index]

    print(f"Repositories: {repo_urls}")
    print(f"Files: {files_filename}")
    print(f"Tag: {tag_name}")

    # Read the list of files from the file
    try:
        with open(files_filename[0], 'r') as file:
            files_to_copy = [line.strip() for line in file.readlines()]
    except FileNotFoundError:
        print(f"Error: File '{files_filename}' not found.")
        sys.exit(1)

    # Now you have repo_urls and files_to_copy lists
    print("Repositories:", repo_urls)
    print("Files to copy:", files_to_copy)

    print(repo_urls, files_to_copy)

    if not repo_urls or not files_to_copy:
        print("Both repository URLs and files must be specified.")
        sys.exit(1)

    # Verify if all specified files and folders exist in the current directory
    for item in files_to_copy:
        if not os.path.exists(os.path.join(os.getcwd(), item)):
            print(f"Error: {item} does not exist in the current directory.")
            sys.exit(1)

    # Get the parent directory
    parent_dir = os.path.abspath(os.path.join(os.getcwd(), os.pardir))

    # Get tags from the current HEAD in the working directory
    current_tags = run_command("git tag --points-at HEAD").split('\n')
    cwd = os.getcwd()
    latest_commit_message = get_latest_commit_message()

    for index, repo_url in enumerate(repo_urls):
        print(f"Processing {repo_url}")
        repo_name = f"repo_{index}"
        target_repo_path = os.path.join(parent_dir, repo_name)

        # Clone the repository into the parent directory
        if os.path.exists(target_repo_path):
            shutil.rmtree(target_repo_path, onerror=on_rm_error)
            print(f'delete folder: {target_repo_path}')
        run_command(f"git clone {repo_url} {target_repo_path}")
        print(f'clone folder: {target_repo_path}')
        os.chdir(target_repo_path)

        # Get the current branch name of the target repo
        current_branch = get_current_branch()

        # Delete files and folders in the target repo if they don't exist in the source
        for item in os.listdir(target_repo_path):
            if item != '.git' and item != '.gitignore':
                target_item_path = os.path.join(target_repo_path, item)
                src_item_path = os.path.join(cwd, item)
                if not os.path.exists(src_item_path):
                    run_command(f"git rm -rf {item}")
                else:
                    if os.path.isdir(target_item_path):
                        shutil.rmtree(target_item_path, onerror=on_rm_error)
                    else:
                        os.remove(target_item_path)

        # Copy specified files and folders to the cloned repository
        os.chdir(cwd)
        for item in files_to_copy:
            src = os.path.join(os.getcwd(), item)
            dest = os.path.join(target_repo_path, item)
            try:
                print(f'copy {src} to {dest}')
                if os.path.isdir(src):
                    shutil.copytree(src, dest)
                else:
                    shutil.copy2(src, dest)
            except Exception as e:
                print(f"Error: {src} to {dest} could not be copied.")
                raise e

        os.chdir(target_repo_path)

        remove_ok_requirements(os.getcwd(), tag_name)

        # Add the copied files and folders to the git index
        try:
            run_command("git rm -r --cached .")
        except:
            print(f"git rm -r --cached error")
        run_command("git add .")
        try:
            run_command(f'git commit -m "{latest_commit_message}"')
            # Push the changes and tags to the remote repository
            run_command(f"git push origin {current_branch} --force")
        except:
            print(f"nothing to commit next")

        for tag in current_tags:
            if tag:
                try:
                    if tag_exists(tag):
                        run_command(f"git tag -d {tag}")
                except Exception as e:
                    print(f"Error: {tag} could not be deleted.")
                run_command(f'git tag {tag} -m "add {tag}"')
                run_command(f"git push origin {tag} --force")
                print(f'pushed tag {tag}')

        run_command(f"git push origin --tags --force")

        # Check and remove history before 'lts' tag if it exists
        # remove_history_before_tag('lts')

    print("Operation completed successfully for all repositories.")


if __name__ == "__main__":
    main()
