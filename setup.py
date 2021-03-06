import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="EmailMxChecker",
    version="0.1.13",
    author="Wei Zhang",
    author_email="zhangw1.2011@gmail.com",
    description="A module to verify email address by SMTP handshake",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Weizhang2017/EmailMxChecker",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=['dnspython'],
)
