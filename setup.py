"""
À CHANGER
"""
import pathlib

from setuptools import find_packages, setup
import alimata

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

if __name__ == "__main__":
    setup(name='aliot-py',
          author='Nils',
          author_email="alivecode.developers@gmail.com",
          version=alimata.__version__,
          description='Aliot-py is the python implementation of the Aliot library, an'
                      ' IOT library made to work with the ALIVEIoT ecosystem (see https://alivecode.ca/iot)',
          long_description=README,
          long_description_content_type="text/markdown",
          classifiers=[
              "Programming Language :: Python :: 3",
              "Programming Language :: Python :: 3.7",
          ],
          url="https://github.com/ALIVEcode/aliot/tree/aliot2",
          packages=find_packages(
              include=['aliot', 'aliot.*']),
          include_package_data=True,
          python_requires=">=3.7",
          install_requires=["websocket-client~=1.3.2",
                            "rich~=12.3.0",
                            "click~=8.1.3",
                            "requests~=2.27.1",
                            "setuptools==62.1.0"
                            ],
          setup_requires="setuptools",
          entry_points={
              "console_scripts": ["aliot = aliot.core._cli.aliot_cli:main"]
          },
          )
