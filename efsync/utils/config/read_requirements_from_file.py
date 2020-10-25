def read_requirements_from_file(file_path):
    try:
        # read all requirements from file and remove \n
        install_list = open(file_path, 'r').read().splitlines()
        # removes empty lines and comments
        install_requires = [
            str(requirement)
            for requirement
            in install_list if not requirement.startswith('#') and len(requirement) > 0]
        return ' '.join(install_requires)
    except Exception as e:
        print(e)
        raise(e)
