import aiohttp
import json
from typing import Dict, List
from backend.config import settings

class LLMExtractor:
    def __init__(self):
        self.base_url = settings.ollama_base_url
        self.model = settings.ollama_model
    
    async def enhance_extraction(self, scraped_data: Dict) -> Dict:
        text_content = scraped_data.get("text_content", "")
        
        if not text_content or len(text_content) < 50:
            return scraped_data
        
        prompt = f"""Extract marketing-relevant information from the following website content. Return ONLY a JSON object with these fields:
- company_name: Primary company/business name
- emails: List of email addresses
- phones: List of phone numbers
- addresses: List of physical addresses
- key_services: Brief list of main services/products

Content:
{text_content[:3000]}

Return valid JSON only, no other text."""

        try:
            async with aiohttp.ClientSession() as session:
                payload = {
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False,
                    "format": "json"
                }
                
                async with session.post(
                    f"{self.base_url}/api/generate",
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=30)
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        llm_response = result.get("response", "{}")
                        
                        try:
                            enhanced_data = json.loads(llm_response)
                            
                            if enhanced_data.get("company_name"):
                                current_companies = scraped_data.get("company_names", [])
                                if isinstance(current_companies, list):
                                    current_companies.insert(0, enhanced_data["company_name"])
                                    scraped_data["company_names"] = current_companies
                            
                            if enhanced_data.get("emails"):
                                scraped_data["emails"] = list(set(
                                    scraped_data.get("emails", []) + enhanced_data["emails"]
                                ))
                            
                            if enhanced_data.get("phones"):
                                scraped_data["phones"] = list(set(
                                    scraped_data.get("phones", []) + enhanced_data["phones"]
                                ))
                            
                            if enhanced_data.get("addresses"):
                                scraped_data["addresses"] = list(set(
                                    scraped_data.get("addresses", []) + enhanced_data["addresses"]
                                ))
                            
                        except json.JSONDecodeError:
                            print("Failed to parse LLM response as JSON")
        
        except Exception as e:
            print(f"LLM extraction error: {e}")
        
        return scraped_data
