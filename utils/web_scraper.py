"""
Web scraping utilities for extracting content from URLs
"""

import requests
from bs4 import BeautifulSoup
from typing import Dict, Optional, List
import validators
import re
from urllib.parse import urljoin, urlparse

try:
    from trafilatura import fetch_url, extract
    TRAFILATURA_AVAILABLE = True
except ImportError:
    TRAFILATURA_AVAILABLE = False


class WebScraper:
    """Handles web content extraction from URLs"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })
        self.timeout = 15
    
    def is_valid_url(self, url: str) -> bool:
        """Validate URL format"""
        return validators.url(url) if validators.url(url) else False
    
    def extract_content(self, url: str) -> Dict[str, Optional[str]]:
        """
        Extract content from a URL
        
        Args:
            url: Web page URL
            
        Returns:
            Dictionary with title, content, meta_description, etc.
        """
        result = {
            "url": url,
            "title": None,
            "content": None,
            "meta_description": None,
            "headings": [],
            "word_count": 0,
            "error": None
        }
        
        if not self.is_valid_url(url):
            result["error"] = "Invalid URL format"
            return result
        
        try:
            # Try trafilatura first (better content extraction)
            if TRAFILATURA_AVAILABLE:
                content = self._extract_with_trafilatura(url)
                if content:
                    result.update(content)
                    return result
            
            # Fallback to BeautifulSoup
            content = self._extract_with_beautifulsoup(url)
            result.update(content)
            
        except requests.RequestException as e:
            result["error"] = f"Request failed: {str(e)}"
        except Exception as e:
            result["error"] = f"Extraction failed: {str(e)}"
        
        return result
    
    def _extract_with_trafilatura(self, url: str) -> Optional[Dict]:
        """Extract using trafilatura library"""
        try:
            downloaded = fetch_url(url)
            if downloaded:
                content = extract(downloaded, include_comments=False, include_tables=True)
                if content:
                    # Also get metadata with BeautifulSoup
                    response = self.session.get(url, timeout=self.timeout)
                    soup = BeautifulSoup(response.text, 'lxml')
                    
                    return {
                        "title": self._get_title(soup),
                        "content": content,
                        "meta_description": self._get_meta_description(soup),
                        "headings": self._get_headings(soup),
                        "word_count": len(content.split()) if content else 0
                    }
        except Exception:
            pass
        return None
    
    def _extract_with_beautifulsoup(self, url: str) -> Dict:
        """Extract using BeautifulSoup"""
        response = self.session.get(url, timeout=self.timeout)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'lxml')
        
        # Remove script and style elements
        for script in soup(["script", "style", "nav", "footer", "header", "aside"]):
            script.decompose()
        
        # Extract main content
        content = self._extract_main_content(soup)
        
        return {
            "title": self._get_title(soup),
            "content": content,
            "meta_description": self._get_meta_description(soup),
            "headings": self._get_headings(soup),
            "word_count": len(content.split()) if content else 0
        }
    
    def _get_title(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract page title"""
        # Try og:title first
        og_title = soup.find("meta", property="og:title")
        if og_title and og_title.get("content"):
            return og_title["content"].strip()
        
        # Then try title tag
        title_tag = soup.find("title")
        if title_tag:
            return title_tag.get_text().strip()
        
        # Then try h1
        h1 = soup.find("h1")
        if h1:
            return h1.get_text().strip()
        
        return None
    
    def _get_meta_description(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract meta description"""
        # Try standard meta description
        meta_desc = soup.find("meta", attrs={"name": "description"})
        if meta_desc and meta_desc.get("content"):
            return meta_desc["content"].strip()
        
        # Try og:description
        og_desc = soup.find("meta", property="og:description")
        if og_desc and og_desc.get("content"):
            return og_desc["content"].strip()
        
        return None
    
    def _get_headings(self, soup: BeautifulSoup) -> List[Dict[str, str]]:
        """Extract all headings"""
        headings = []
        for tag in ["h1", "h2", "h3"]:
            for heading in soup.find_all(tag):
                text = heading.get_text().strip()
                if text:
                    headings.append({"level": tag, "text": text})
        return headings
    
    def _extract_main_content(self, soup: BeautifulSoup) -> str:
        """Extract main text content"""
        # Try to find main content container
        main_selectors = [
            soup.find("article"),
            soup.find("main"),
            soup.find("div", class_=re.compile(r"(content|article|post|entry)")),
            soup.find("div", id=re.compile(r"(content|article|post|entry)"))
        ]
        
        container = None
        for selector in main_selectors:
            if selector:
                container = selector
                break
        
        if not container:
            container = soup.find("body")
        
        if container:
            # Get text from paragraphs
            paragraphs = container.find_all("p")
            text_parts = [p.get_text().strip() for p in paragraphs if p.get_text().strip()]
            return "\n\n".join(text_parts)
        
        return ""
    
    def batch_extract(self, urls: List[str]) -> List[Dict]:
        """Extract content from multiple URLs"""
        results = []
        for url in urls:
            result = self.extract_content(url)
            results.append(result)
        return results
    
    def get_page_links(self, url: str, same_domain_only: bool = True) -> List[str]:
        """Get all links from a page"""
        links = []
        
        try:
            response = self.session.get(url, timeout=self.timeout)
            soup = BeautifulSoup(response.text, 'lxml')
            
            base_domain = urlparse(url).netloc
            
            for a in soup.find_all("a", href=True):
                href = a["href"]
                full_url = urljoin(url, href)
                
                if self.is_valid_url(full_url):
                    if same_domain_only:
                        if urlparse(full_url).netloc == base_domain:
                            links.append(full_url)
                    else:
                        links.append(full_url)
                        
        except Exception as e:
            print(f"Error getting links: {e}")
        
        return list(set(links))  # Remove duplicates
