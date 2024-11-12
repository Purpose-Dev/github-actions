import os
import json

import lxml.etree as ET


def get_file_type(file_path):
    file_type = os.path.splitext(file_path)[1]
    return file_type


def get_file_name(file_path):
    file_name = os.path.basename(file_path)
    return file_name


def update_json(version, file_path):
    with open(file_path, "r") as json_file:
        data = json.load(json_file)
        data["version"] = version
        try:
            data["packages"][""]["version"] = version
        except KeyError:
            pass

    with open(file_path, "w") as json_file:
        json.dump(data, json_file, indent=2)
        json_file.write("\n")


def update_xml(version, file_path):
    mytree = ET.parse(file_path)
    myroot = mytree.getroot()
    namespace = {"maven": "http://maven.apache.org/POM/4.0.0"}
    version_element = myroot.find("maven:version", namespace)

    if version_element is not None:
        version_element.text = version
    else:
        raise Exception("No <version> tag found in pom.xml")

    mytree.write(file_path, pretty_print=True, encoding="UTF-8", xml_declaration=True)


if __name__ == "__main__":
    version = os.getenv("INPUT_VERSION")
    file_path = os.getenv("INPUT_FILE_PATH")

    try:
        os.path.isfile(file_path)
    except TypeError:
        raise Exception(f"File path for {file_path} does not exist.")

    file_name = get_file_name(file_path)
    file_type = get_file_type(file_path)

    if file_type == ".json":
        update_json(version, file_path)
    elif file_type == ".xml":
        update_xml(version, file_path)
    else:
        raise Exception("No file recognized as supported format.")

    if "GITHUB_OUTPUT" in os.environ:
        with open(os.environ["GITHUB_OUTPUT"], "a") as f:
            print("{0}={1}".format("status", f"Updated {file_path}"), file=f)
