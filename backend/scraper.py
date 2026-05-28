from playwright.async_api import async_playwright, Page
from bs4 import BeautifulSoup
import re
from typing import Dict, List, Optional
from urllib.parse import urljoin, urlparse

class WebScraper:
    def __init__(self):
        self.playwright = None
        self.browser = None
        
    async def __aenter__(self):
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(headless=True)
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()
    
    async def scrape_page(self, url: str) -> Dict[str, any]:
        page = await self.browser.new_page()
        
        try:
            await page.goto(url, timeout=30000, wait_until="domcontentloaded")
            await page.wait_for_timeout(2000)
            
            content = await page.content()
            title = await page.title()
            
            soup = BeautifulSoup(content, 'html.parser')
            
            text_content = soup.get_text(separator=' ', strip=True)
            
            emails = self._extract_emails(text_content)
            phones = self._extract_phones(text_content)
            addresses = self._extract_addresses(text_content)
            company_names = self._extract_company_names(soup)
            social_links = self._extract_social_links(soup, url)
            contact_forms = self._extract_contact_forms(soup, url)
            meta_description = self._extract_meta_description(soup)
            
            return {
                "url": url,
                "title": title,
                "emails": emails,
                "phones": phones,
                "addresses": addresses,
                "company_names": company_names,
                "social_links": social_links,
                "contact_forms": contact_forms,
                "meta_description": meta_description,
                "text_content": text_content[:5000]
            }
        
        except Exception as e:
            print(f"Error scraping {url}: {e}")
            return {"url": url, "error": str(e)}
        
        finally:
            await page.close()
    
    def _extract_emails(self, text: str) -> List[str]:
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = list(set(re.findall(email_pattern, text)))
        return [e for e in emails if not e.endswith(('.png', '.jpg', '.gif'))]
    
    def _extract_phones(self, text: str) -> List[str]:
        phone_patterns = [
            r'\+?\d{1,3}[-.\s]?\(?\d{1,4}\)?[-.\s]?\d{1,4}[-.\s]?\d{1,9}',
            r'\(\d{3}\)\s*\d{3}-\d{4}',
            r'\d{3}-\d{3}-\d{4}'
        ]
        phones = []
        for pattern in phone_patterns:
            phones.extend(re.findall(pattern, text))
        return list(set(phones))
    
    def _extract_addresses(self, text: str) -> List[str]:
        address_pattern = r'\d+\s+[\w\s,]+(?:Street|St|Avenue|Ave|Road|Rd|Boulevard|Blvd|Lane|Ln|Drive|Dr|Court|Ct|Circle|Cir|Way|Plaza|Square|Trail|Parkway|Pkwy|Place|Pl)[,\s]+[\w\s]+,\s*[A-Z]{2}\s*\d{5}'
        addresses = re.findall(address_pattern, text, re.IGNORECASE)
        return list(set(addresses))
    
    def _extract_company_names(self, soup: BeautifulSoup) -> List[str]:
        company_names = []
        
        og_site = soup.find('meta', property='og:site_name')
        if og_site and og_site.get('content'):
            company_names.append(og_site['content'])
        
        h1_tags = soup.find_all('h1', limit=3)
        for h1 in h1_tags:
            text = h1.get_text(strip=True)
            if len(text) < 50:
                company_names.append(text)
        
        return list(set(company_names))
    
    def _extract_social_links(self, soup: BeautifulSoup, base_url: str) -> Dict[str, str]:
        social_patterns = {
            'facebook': r'facebook\.com',
            'twitter': r'twitter\.com|x\.com',
            'linkedin': r'linkedin\.com',
            'instagram': r'instagram\.com',
            'youtube': r'youtube\.com',
            'tiktok': r'tiktok\.com'
        }
        
        social_links = {}
        links = soup.find_all('a', href=True)
        
        for link in links:
            href = link['href']
            absolute_url = urljoin(base_url, href)
            
            for platform, pattern in social_patterns.items():
                if re.search(pattern, absolute_url, re.IGNORECASE):
                    social_links[platform] = absolute_url
        
        return social_links
    
    def _extract_contact_forms(self, soup: BeautifulSoup, base_url: str) -> List[str]:
        contact_urls = []
        links = soup.find_all('a', href=True)
        
        contact_keywords = ['contact', 'get-in-touch', 'reach-us', 'support', 'help']
        
        for link in links:
            href = link['href'].lower()
            text = link.get_text(strip=True).lower()
            
            if any(keyword in href or keyword in text for keyword in contact_keywords):
                absolute_url = urljoin(base_url, link['href'])
                contact_urls.append(absolute_url)
        
        return list(set(contact_urls))
    
    def _extract_meta_description(self, soup: BeautifulSoup) -> Optional[str]:
        meta = soup.find('meta', attrs={'name': 'description'})
        if meta and meta.get('content'):
            return meta['content']
        
        og_desc = soup.find('meta', property='og:description')
        if og_desc and og_desc.get('content'):
            return og_desc['content']
        
        return None
