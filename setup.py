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
    setup(name='alimata',
          author='Nils Lahaye and Francis M-G researchers at LRIMa',
          author_email="alivecode.developers@gmail.com",
          version=alimata.__version__,
          description='Alimata is a Python library to simplify the use of the pymata-express library.',
          long_description=README,
          long_description_content_type="text/markdown",
          classifiers=[
              "Programming Language :: Python :: 3",
              "Programming Language :: Python :: 3.7",
          ],
          url="https://github.com/ALIVEcode/alimata",
          packages=find_packages(
              include=['alimata', 'alimata.*']),
          include_package_data=True,
          python_requires=">=3.7",
          install_requires=["firmetix>=7.1.1"],
          setup_requires="setuptools",
          )
