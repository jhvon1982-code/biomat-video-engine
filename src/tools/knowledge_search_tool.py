"""
Knowledge search tool for retrieving material specifications from Juhe_Polymer_Specs dataset.
"""
import json
from langchain.tools import tool
from coze_coding_utils.runtime_ctx.context import new_context
import subprocess


@tool
def search_polymer_specs(material_name: str, top_k: int = 3) -> str:
    """
    Search polymer material specifications from the Juhe_Polymer_Specs knowledge base.

    Use this tool when you need to retrieve detailed technical information about
    biodegradable polymers including PCL, PLLA, PLGA, PTMC, AMPPD, APS-5, etc.

    This tool provides:
    - Material chemical properties (molecular weight, Tg, Tm)
    - Physical characteristics (crystallinity, modulus, degradation period)
    - Application scenarios and usage guidelines
    - Compatibility and processing parameters

    Args:
        material_name: Name of the material (e.g., "PCL", "PLLA", "PLGA", "PTMC")
        top_k: Number of top results to return (default: 3)

    Returns:
        Formatted search results with material specifications
    """
    try:
        # Build command
        cmd = [
            "coze-coding-ai",
            "knowledge",
            "search",
            "--query", f"{material_name} properties specifications molecular weight Tg Tm",
            "--top-k", str(top_k),
            "--dataset", "Juhe_Polymer_Specs"
        ]

        # Execute command
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=30
        )

        if result.returncode == 0:
            output = result.stdout
            # Try to parse JSON if output is in JSON format
            try:
                if output.strip().startswith('{'):
                    data = json.loads(output)
                    # Format the JSON data
                    formatted = []
                    for idx, item in enumerate(data.get('results', []), 1):
                        formatted.append(f"### Result {idx}\n")
                        formatted.append(f"**Content**: {item.get('content', 'N/A')}\n")
                        formatted.append(f"**Score**: {item.get('score', 'N/A')}\n")
                    return "\n".join(formatted)
                else:
                    return output
            except json.JSONDecodeError:
                return output
        else:
            error_msg = result.stderr if result.stderr else "Unknown error"
            return f"Knowledge search failed: {error_msg}"

    except subprocess.TimeoutExpired:
        return "Knowledge search timed out after 30 seconds"
    except Exception as e:
        return f"Knowledge search error: {str(e)}"


@tool
def import_knowledge_url(url: str, dataset: str = "Juhe_Polymer_Specs") -> str:
    """
    Import a document URL into the knowledge base.

    Use this tool when you need to add new material specification documents
    to the Juhe_Polymer_Specs dataset from a web URL.

    Args:
        url: URL of the document to import
        dataset: Target dataset name (default: "Juhe_Polymer_Specs")

    Returns:
        Import result message
    """
    try:
        cmd = [
            "coze-coding-ai",
            "knowledge",
            "add",
            "--dataset", dataset,
            "--url", url
        ]

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=60
        )

        if result.returncode == 0:
            return f"✅ Successfully imported URL to {dataset}: {url}"
        else:
            error_msg = result.stderr if result.stderr else "Unknown error"
            return f"❌ Import failed: {error_msg}"

    except subprocess.TimeoutExpired:
        return "Import timed out after 60 seconds"
    except Exception as e:
        return f"Import error: {str(e)}"
