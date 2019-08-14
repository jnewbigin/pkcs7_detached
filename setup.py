import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pkcs7",
    version="0.0.1",
    author="John Newbigin",
    author_email="jnewbigin@chrysocome.net",
    description="Validate detacked PKCS7 signatures",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jnewbigin/pkcs7",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
