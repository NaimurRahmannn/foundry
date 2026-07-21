from typing import Type
import requests
from pydantic import BaseModel,Field
from crewai.tools import BaseTool

class PyPIPackageLookupInput(BaseModel):
    package_name:str=Field(
     ..., description="The exact PyPI package name to look up, e.g. 'fastapi' or 'sqlalchemy'."
    )
class PyPIPackageLookupTool(BaseTool):
    name: str = "pypi_package_lookup"
    description: str = (
        "Looks up a Python package on PyPI and returns its latest version, "
        "short summary, and minimum supported Python version. Use this before "
        "recommending a Python library in an architecture, so recommendations "
        "are grounded in real, currently published packages instead of assumptions."
    )
    args_schema: Type[BaseModel] = PyPIPackageLookupInput

    def _run(self, package_name: str) -> str:
        url = f"https://pypi.org/pypi/{package_name}/json"
        try:
            response = requests.get(url, timeout=10)
        except requests.RequestException as exc:
            return f"Could not reach PyPI for '{package_name}': {exc}"

        if response.status_code == 404:
            return f"No PyPI package named '{package_name}' was found. Double-check the spelling."
        if response.status_code != 200:
            return f"PyPI lookup for '{package_name}' failed with status {response.status_code}."

        data = response.json()
        info = data.get("info", {})
        latest_version = info.get("version", "unknown")
        summary = info.get("summary", "No summary available.")
        requires_python = info.get("requires_python", "not specified")

        return (
            f"Package: {package_name}\n"
            f"Latest version: {latest_version}\n"
            f"Requires Python: {requires_python}\n"
            f"Summary: {summary}"
        )
