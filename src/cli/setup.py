from setuptools import setup


setup(
    name="mojee",
    version="0.1",
    py_modules=["images"],
    install_requires=["Click", "texttable", "requests", "google-cloud-vision"],
    entry_points="""
        [console_scripts]
        mojee=images:cli
    """,
)
