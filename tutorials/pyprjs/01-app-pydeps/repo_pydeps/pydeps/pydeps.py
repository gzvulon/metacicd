import sys
import getpass
import subprocess


def analize():
    report = {}
    report.update(analize_loaded())
    report.update(analize_pip_list())
    report.update(analize_pip_freeze())
    return report

def _get_v(it):
    import pkg_resources
    return pkg_resources.get_distribution(it).version
    # try:
    #     print (it)
    #     return pkg_resources.get_distribution(it).version
    # except:
    #     return "NA"

def analize_loaded():
    loaded = {
        (k, '')
        for k, v in list(sys.modules.items())
        if not k.startswith('_') and k not in sys.builtin_module_names}
    return {'modules.loaded.list': loaded}


def analize_pip_list():
    import re
    out = subprocess.check_output(
        f'{sys.executable} -m pip list', 
        shell=True).decode()
    l = [tuple(x.strip().split()) for x in out.splitlines() if re.match('.*[0-9].*', x)]
    return {'modules.pip-list.list': l}


def analize_pip_freeze():
    out = subprocess.check_output(
        f'{sys.executable} -m pip freeze', 
        shell=True).decode()
    l = [tuple(x.strip().split('==')) for x in out.splitlines()]
    return {'modules.pip-freeze.list': l}

# def analize_pkg_resources():
#     import pkg_resources
#     pkg_resources.
#     out = subprocess.check_output(
#         f'{sys.executable} -m pip freeze', 
#         shell=True).decode()
#     l = [tuple(x.strip().split('==')) for x in out.splitlines()]
#     return {'modules.pkg_resources.list': l}

def main():
    print("Analizing Interpreter and Virtual Environment")
    import pprint
    report = analize()
    print(pprint.pformat(report))
    print(f"Loaded Modules Count: {len(report['modules.loaded.list'])}")
    print(f"Hello from pydeps to {getpass.getuser()}")


if __name__ == "__main__":
    import sys
    if '--test' in sys.argv:
        print("--test depricated use pytest pydeps instead")
    else:
        main()
        
