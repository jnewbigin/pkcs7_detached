import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pkcs7_detached",
    version="0.0.3",
    author="John Newbigin",
    author_email="jnewbigin@chrysocome.net",
    description="Validate PKCS7 detached signatures",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jnewbigin/pkcs7_detached",
    packages=setuptools.find_packages(),
    install_requires=["cryptography>=2.3"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
