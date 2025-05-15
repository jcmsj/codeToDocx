import os
import pypandoc

# key: language name
# value: file extension
LANGUAGE:dict[str,str] = {
    'python': '.py',
    'java': '.java',
    'c': '.c',
    'cpp': '.cpp',
    'javascript': '.js',
    'typescript': '.ts',
    'html': '.html',
    'css': '.css',
    'scss': '.scss',
    'less': '.less',
    'java': '.java',
    'kotlin': '.kt',
    'swift': '.swift',
    'dart': '.dart',
    'vue': '.vue',
    'react': '.jsx',
    'react-ts': '.tsx',
    'php': '.php',
    'go': '.go',
    'rust': '.rs',
    'ruby': '.rb',
    'perl': '.pl',
    'shell': '.sh',
    'powershell': '.ps1',
    'yaml': '.yaml',
    'json': '.json',
    'xml': '.xml',
    'sql': '.sql',
    'markdown': '.md',
    'plaintext': '.txt'
}

def convert_to_docx(directory:str, output_file:str, languages:list[str], gitignore:bool=False, keep_md:bool=False):
    # add .docx extension if not present
    final_output_name = output_file if output_file.endswith('.docx') else output_file + '.docx'

    sorted_languages = sorted(languages, key=lambda x: LANGUAGE[x])
    print(f"Languages: {sorted_languages}")

    processed_files: dict[str,list[dict[str,str]]] = {language: [] for language in sorted_languages}

    # read the gitignore file residing in directory
    ignore = [x.strip('\n')for x in open(f"{directory}/.gitignore", 'r', encoding='utf-8', errors='ignore') .readlines() if not x.startswith('#')]
    ignore = [x for x in ignore if x]
    print(f"Ignore: {ignore}")
    
    for root, dirs, files in os.walk(directory):
        for file in files:
            for language in sorted_languages:
                if file.endswith(LANGUAGE[language]):
                    fullpath = os.path.join(root, file)
                    relativepath = fullpath[len(directory)+1:] # +1 to remove leading slash
                    filename = os.path.basename(fullpath)
                    # skip file if in .gitignore file
                    if not any([relativepath.startswith(p) for p in ignore]):
                        processed_files[language].append({
                            'fullpath':fullpath,
                            'relativepath':relativepath,
                            'filename':filename,
                        })
                    break
                
    for language in sorted_languages:
        print(f"Found {len(processed_files[language])} {language} files")
    ''' Create a markdown file with the following structure
    ## <relative file path>.<extension>
    ```<language>
    <code>
    ```
    '''
    temp_md = final_output_name.replace('.docx', '.md')
    with open(temp_md, 'w',encoding='utf-8') as f:
        for language, items in processed_files.items():
            for item in items:
                with open(item['fullpath'], 'r', encoding='utf-8', errors='ignore') as file:
                    code = file.read()
                    # Header
                    try:
                        f.write(f"## {item['filename']}\n")
                        # codeblock
                        f.write(f"```{language}\n{code}\n```\n")
                    except:
                        continue

        pypandoc.convert_file(temp_md, 'docx', outputfile=final_output_name)

    if os.path.exists(temp_md) and not keep_md:
        os.remove(temp_md)
    print(f"Generated {final_output_name}")
    if keep_md:
        print(f"Generated {temp_md}")

def cli():
    import argparse

    parser = argparse.ArgumentParser(description='Generate a docx file from source code')
    parser.add_argument('-d','--directory', help='path for searching source files', required=True)
    # parser.add_argument('--url', help='github repo url', required=False)
    parser.add_argument('-o','--output', help='output file name ( with .docx extension)', required=True)
    parser.add_argument('-l','--languages', help='list of languages to search for', required=True, choices=LANGUAGE.keys(), nargs='+' )

    parser.add_argument('--gitignore', help='whether to use .gitignore to exclude files', required=False, default=False, action='store_true')
    # keep the markdown file
    parser.add_argument('--keep_md', help='keep the markdown file', required=False, default=False, action='store_true')
    return parser.parse_args()


def main():
    '''Run if main module'''
    args = cli()
    # if args.url:
    #     print("TODO")
        # pass 
        # # shallow clone the repo to a temporary directory
        # # clone the repo to a temporary directory, check OS for the exact path
        # # generate a random temp name
        # # extract the repo name from the url
        # repoName = args.url.split('/')[-1]
        # tempName = 'temp-repo'
        # if os.name == 'posix':
        #     tempName = tempfile.mkdtemp()
        # else:
        #     tempName = os.path.join(tempfile.gettempdir(), 'temp-repo')

        # os.system(f"git clone --depth 1 {args.url} {tempName}")
    
    if args.directory:
        convert_to_docx(args.directory, args.output, args.languages, gitignore=args.gitignore, keep_md=args.keep_md)

if __name__ == '__main__':
    main()
