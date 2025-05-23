### Helper script to automatically grab the first couple lines of each script
### with the description of what it does, and update the README accordingly. 

import os
import argparse, sys

def get_script_description(file_path, num_lines=4):
    descriptions = []
    for file in os.listdir(file_path):
        if file.endswith(".py"):
            with open(os.path.join(file_path, file), 'r', encoding='utf-8') as f:
                lines = []
                try:
                    for _ in range(num_lines):
                        line = next(f).strip()
                        if line.startswith("###"):
                            lines.append(line.lstrip("###").strip())
                except StopIteration:
                    pass
                descriptions.append((file, ' '.join(lines)))
    return descriptions

def update_readme(readme_path, scripts_dir):
    with open(readme_path, 'r', encoding='utf-8') as readme_file:
        readme_content = readme_file.readlines()

    new_content = []
    scripts_section_started = False
    scripts_content = []
    for line in readme_content:
        if line.strip() == "# Scripts":
            scripts_section_started = True
            new_content.append(line)
            new_content.append("\n")
            descriptions = get_script_description(scripts_dir)
            for file, description in descriptions:
                script_line = f"- `scripts/{file}`: {description}\n"
                new_content.append(script_line)
                scripts_content.append(script_line)
        elif line.strip().startswith("#") and scripts_section_started:
            scripts_section_started = False
            new_content.append(line)
        elif not scripts_section_started:
            new_content.append(line)

    with open(readme_path, 'w', encoding='utf-8') as readme_file:
        readme_file.writelines(new_content)
    
    ### output to txt, for debugging
    # with open('new_scripts_content.txt', 'w', encoding='utf-8') as new_file:
    #     new_file.writelines(scripts_content)

# ### Local paths
# if __name__ == "__main__":
#     readme_path = '../README.md'
#     scripts_dir = '.'
#     update_readme(readme_path, scripts_dir)

### Argument parsing
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Update README with script descriptions")
    parser.add_argument('--readme', type=str, required=True, help="Path to README.md file")
    parser.add_argument('--scripts_dir', type=str, required=True, help="Path to directory containing scripts")
    args = parser.parse_args()
    
    sys.exit(update_readme(args.readme, args.scripts_dir))
