import requests
import logging
from typing import Dict, Any

logger = logging.getLogger("app.services.fact_checker")

def fact_check(query: str) -> Dict[str, Any]:
    """
    Verifies a networking topic using the Wikipedia API.
    Returns a dictionary containing Topic, Summary, Wikipedia URL, and Status.
    """
    if not query or not query.strip():
        return {
            "topic": query,
            "summary": "No query provided for fact checking.",
            "wikipedia_url": "",
            "status": "Invalid Query"
        }
        
    query_clean = query.strip()
    # Replace spaces with underscores for Wikipedia REST summary API
    api_query = query_clean.replace(" ", "_")
    
    url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{api_query}"
    headers = {
        "User-Agent": "PersonalizedNetworkingAssistant/1.0 (contact@example.com)"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=5)
        if response.status_code == 200:
            data = response.json()
            summary = data.get("extract", "No summary found.")
            wiki_url = data.get("content_urls", {}).get("desktop", {}).get("page", f"https://en.wikipedia.org/wiki/{api_query}")
            return {
                "topic": query_clean,
                "summary": summary,
                "wikipedia_url": wiki_url,
                "status": "Verified"
            }
        elif response.status_code == 404:
            # Fallback: Try a search endpoint first to find the closest match
            search_url = "https://en.wikipedia.org/w/api.php"
            search_params = {
                "action": "opensearch",
                "search": query_clean,
                "limit": 1,
                "namespace": 0,
                "format": "json"
            }
            search_resp = requests.get(search_url, params=search_params, headers=headers, timeout=5)
            if search_resp.status_code == 200:
                search_data = search_resp.json()
                # search_data format: [query, [titles], [descriptions], [urls]]
                if len(search_data) > 1 and search_data[1]:
                    matched_title = search_data[1][0]
                    matched_url = search_data[3][0] if len(search_data) > 3 and search_data[3] else f"https://en.wikipedia.org/wiki/{matched_title.replace(' ', '_')}"
                    
                    # Fetch summary for matched title
                    summary_url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{matched_title.replace(' ', '_')}"
                    sum_resp = requests.get(summary_url, headers=headers, timeout=5)
                    if sum_resp.status_code == 200:
                        sum_data = sum_resp.json()
                        return {
                            "topic": query_clean,
                            "summary": sum_data.get("extract", f"See full article on Wikipedia: {matched_title}"),
                            "wikipedia_url": matched_url,
                            "status": "Verified (Redirected)"
                        }
            
            return {
                "topic": query_clean,
                "summary": f"Wikipedia could not find a page matching '{query_clean}'.",
                "wikipedia_url": "",
                "status": "Not Found"
            }
        else:
            return {
                "topic": query_clean,
                "summary": f"Wikipedia returned status code {response.status_code}.",
                "wikipedia_url": "",
                "status": "Error"
            }
    except Exception as e:
        logger.error(f"Error during fact check for '{query_clean}': {e}")
        return {
            "topic": query_clean,
            "summary": f"Failed to connect to Wikipedia API: {str(e)}",
            "wikipedia_url": "",
            "status": "Connection Error"
        }
