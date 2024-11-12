import json
import lxml.etree as ET
import os


def get_json_version(file_path):
    """Retrieve version in package.json file."""
    with open(file_path, "r") as json_file:
        data = json.load(json_file)
        return data.get("version", None)


def get_xml_version(file_path):
    """Retrieve version in pom.xml file."""
    tree = ET.parse(file_path)
    root = tree.getroot()
    namespace = {"maven": "http://maven.apache.org/POM/4.0.0"}
    version_element = root.find("maven:version", namespace)

    if version_element is not None:
        return version_element.text

    return None


def get_version(file_path):
    file_extension = os.path.splitext(file_path)[1]

    if file_extension == ".json":
        return get_json_version(file_path)
    elif file_extension == ".xml":
        return get_xml_version(file_path)
    else:
        print(f"Unsupported file type for {file_path} - {file_extension}")
        return None


if __name__ == "__main__":
    file_path = os.getenv("INPUT_FILE_PATH")

    if file_path and os.path.isfile(file_path):
        version = get_version(file_path)

        if version:
            print(f"Version in {file_path}: {version}")
            with open(os.getenv("GITHUB_OUTPUT"), "a") as output:
                print(f"version={version}", file=output)
        else:
            print(f"No version found in {file_path}")
            exit(1)
    else:
        print(f"{file_path} does not exist.")
        exit(1)
