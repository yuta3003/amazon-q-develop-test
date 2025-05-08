import setuptools

with open("README.md") as fp:
    long_description = fp.read()

setuptools.setup(
    name="api_gateway_lambda",
    version="0.0.1",
    description="API Gateway and Lambda CDK Python project",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="author",
    package_dir={"": "api_gateway_lambda"},
    packages=setuptools.find_packages(where="api_gateway_lambda"),
    install_requires=[
        "aws-cdk-lib>=2.0.0",
        "constructs>=10.0.0",
    ],
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Software Development :: Code Generators",
        "Topic :: Utilities",
        "Typing :: Typed",
    ],
)