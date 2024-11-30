from setuptools import setup, find_packages

setup(
    name="tarjan_travel_plan",
    version="1.0.0",
    description="TSP Solver for Tarjan's travel planning problem",
    author="Shubham Singh",
    author_email="shsin5910@oslomet.no",
    packages=find_packages(),  # Finds 'tarjanplanner' package
    install_requires=[
        "networkx",
        "geopy",
        "matplotlib",
        "pytest",

    ],
    entry_points={
        "console_scripts": [
            "tarjan-planner=tarjan_travel_plan.tarjanplanner.main:main", 
            "tarjan-planner-gui=tarjan_travel_plan.gui_interface:open_gui"# Updated path to main()
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
