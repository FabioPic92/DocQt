from setuptools import setup

package_name = "RecognizeDocumentGui"
widgets = package_name + "/widgets"
#utils = package_name + "/utils"

setup(
    name=package_name,
    version="0.0.0",
    packages=[package_name, widgets],
    data_files=[
        ("share/ament_index/resource_index/packages", ["resource/" + package_name]),
        ("share/" + package_name, ["package.xml"]),
    ],
    install_requires=["setuptools"],
    zip_safe=True,
    maintainer="Fabio Picciati",
    maintainer_email="picciati.fab@gmail.com",
    description="GUI to recognize document",
    license="TODO: License declaration",
    tests_require=["pytest"],
    entry_points={
        "console_scripts": ["main_window = RecognizeDocumentGui.RecognizeDocumentGui:main"],
    },
)