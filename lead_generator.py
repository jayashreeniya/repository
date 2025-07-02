#!/usr/bin/env python3
"""
Niya Lead Generator - Automated Lead Generation System
Scrapes startups, enriches with LinkedIn profiles, and uploads to Airtable
"""

import os
import csv
import time
import requests
import urllib.parse
from bs4 import BeautifulSoup
from datetime import datetime
from dotenv import load_dotenv
import json

load_dotenv()

# Configuration
AIRTABLE_TOKEN = os.getenv("AIRTABLE_TOKEN")
LEADS_BASE_ID = os.getenv("LEADS_BASE_ID")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

class LeadGenerator:
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        self.leads = []
        
    def scrape_inc42_startups(self, max_pages=3):
        """Scrape startup data from Inc42"""
        print("🔍 Scraping startups from Inc42...")
        
        companies = []
        
        for page in range(1, max_pages + 1):
            try:
                url = f"https://inc42.com/startups/page/{page}/"
                print(f"📄 Scraping page {page}...")
                
                response = requests.get(url, headers=self.headers, timeout=10)
                response.raise_for_status()
                soup = BeautifulSoup(response.content, "html.parser")
                
                # Look for startup articles
                articles = soup.find_all("article") or soup.find_all("div", class_="post")
                
                for article in articles:
                    try:
                        # Try different selectors for company name
                        name_elem = (
                            article.find("h2") or 
                            article.find("h3") or 
                            article.find("a", class_="post-title")
                        )
                        
                        if name_elem:
                            company_name = name_elem.get_text(strip=True)
                            
                            # Get link
                            link_elem = article.find("a")
                            link = link_elem.get("href") if link_elem else ""
                            
                            # Get description if available
                            desc_elem = article.find("p") or article.find("div", class_="excerpt")
                            description = desc_elem.get_text(strip=True) if desc_elem else ""
                            
                            companies.append({
                                "Company Name": company_name,
                                "Source URL": link,
                                "Description": description,
                                "Source": "Inc42"
                            })
                            
                    except Exception as e:
                        print(f"⚠️ Error parsing article: {e}")
                        continue
                
                # Rate limiting
                time.sleep(2)
                
            except Exception as e:
                print(f"❌ Error scraping page {page}: {e}")
                continue
        
        print(f"✅ Scraped {len(companies)} companies from Inc42")
        return companies
    
    def scrape_techcrunch_startups(self, max_pages=2):
        """Scrape startup data from TechCrunch"""
        print("🔍 Scraping startups from TechCrunch...")
        
        companies = []
        
        try:
            url = "https://techcrunch.com/tag/startups/"
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, "html.parser")
            
            articles = soup.find_all("article") or soup.find_all("div", class_="post-block")
            
            for article in articles[:20]:  # Limit to 20 articles
                try:
                    title_elem = article.find("h2") or article.find("a", class_="post-block__title")
                    if title_elem:
                        company_name = title_elem.get_text(strip=True)
                        
                        link_elem = article.find("a")
                        link = link_elem.get("href") if link_elem else ""
                        
                        companies.append({
                            "Company Name": company_name,
                            "Source URL": link,
                            "Description": "",
                            "Source": "TechCrunch"
                        })
                        
                except Exception as e:
                    continue
            
            print(f"✅ Scraped {len(companies)} companies from TechCrunch")
            
        except Exception as e:
            print(f"❌ Error scraping TechCrunch: {e}")
        
        return companies
    
    def find_linkedin_profiles(self, companies, roles=None):
        """Find LinkedIn profiles for company decision makers"""
        if roles is None:
            roles = ["CEO", "CTO", "VP Engineering", "Head of People", "VP Sales"]
        
        print("🔍 Finding LinkedIn profiles...")
        
        enriched_companies = []
        
        for i, company in enumerate(companies):
            print(f"🔗 Searching for {company['Company Name']} ({i+1}/{len(companies)})")
            
            best_profile = ""
            best_role = ""
            
            for role in roles:
                try:
                    profile = self.google_search_linkedin(company['Company Name'], role)
                    if profile:
                        best_profile = profile
                        best_role = role
                        break
                    
                    # Rate limiting
                    time.sleep(1)
                    
                except Exception as e:
                    print(f"⚠️ Error searching for {role}: {e}")
                    continue
            
            company['LinkedIn Profile'] = best_profile
            company['Target Role'] = best_role
            enriched_companies.append(company)
            
            # Rate limiting between companies
            time.sleep(2)
        
        print(f"✅ Enriched {len(enriched_companies)} companies with LinkedIn profiles")
        return enriched_companies
    
    def google_search_linkedin(self, company, role):
        """Search Google for LinkedIn profiles"""
        try:
            query = f"site:linkedin.com/in {role} {company}"
            url = f"https://www.google.com/search?q={urllib.parse.quote_plus(query)}"
            
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            
            # Look for LinkedIn profile links
            for link in soup.find_all("a", href=True):
                href = link.get("href")
                if "linkedin.com/in/" in href:
                    # Extract the actual LinkedIn URL
                    if "/url?q=" in href:
                        linkedin_url = href.split("/url?q=")[1].split("&")[0]
                        return urllib.parse.unquote(linkedin_url)
                    else:
                        return href
            
            return ""
            
        except Exception as e:
            print(f"⚠️ Error in Google search: {e}")
            return ""
    
    def generate_email_addresses(self, companies):
        """Generate potential email addresses for leads"""
        print("📧 Generating email addresses...")
        
        for company in companies:
            company_name = company['Company Name']
            target_role = company.get('Target Role', 'CEO')
            
            # Generate common email patterns
            email_patterns = []
            
            # Extract first word of company name
            company_words = company_name.split()
            if company_words:
                first_word = company_words[0].lower()
                
                # Common email patterns
                patterns = [
                    f"info@{first_word}.com",
                    f"hello@{first_word}.com",
                    f"contact@{first_word}.com",
                    f"team@{first_word}.com"
                ]
                
                email_patterns.extend(patterns)
            
            company['Email Patterns'] = email_patterns
            company['Primary Email'] = email_patterns[0] if email_patterns else ""
        
        print(f"✅ Generated email patterns for {len(companies)} companies")
        return companies
    
    def save_to_csv(self, companies, filename="generated_leads.csv"):
        """Save leads to CSV file"""
        print(f"💾 Saving {len(companies)} leads to {filename}...")
        
        fieldnames = [
            "Company Name", "Source URL", "Description", "Source", 
            "LinkedIn Profile", "Target Role", "Primary Email", "Email Patterns"
        ]
        
        with open(filename, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(companies)
        
        print(f"✅ Saved leads to {filename}")
    
    def upload_to_airtable(self, companies):
        """Upload leads to Airtable"""
        print("📤 Uploading leads to Airtable...")
        
        if not AIRTABLE_TOKEN or not LEADS_BASE_ID:
            print("❌ Airtable credentials not configured")
            return False
        
        headers = {
            "Authorization": f"Bearer {AIRTABLE_TOKEN}",
            "Content-Type": "application/json"
        }
        
        url = f"https://api.airtable.com/v0/{LEADS_BASE_ID}/Imported table"
        
        uploaded_count = 0
        
        for company in companies:
            try:
                # Prepare lead data for Airtable
                lead_data = {
                    "records": [{
                        "fields": {
                            "Company Name": company.get("Company Name", ""),
                            "Website/LinkedIn": company.get("LinkedIn Profile", ""),
                            "Industry": "Technology",  # Default for startups
                            "Company Size": "1-50 employees",  # Default for startups
                            "Role": company.get("Target Role", "CEO"),
                            "Email": company.get("Primary Email", ""),
                            "Email Sent?": "FALSE",
                            "Status": "New Lead",
                            "Notes/Objections": f"Source: {company.get('Source', 'Unknown')}. {company.get('Description', '')}"
                        }
                    }]
                }
                
                response = requests.post(url, headers=headers, json=lead_data)
                
                if response.status_code == 200:
                    uploaded_count += 1
                    print(f"✅ Uploaded: {company['Company Name']}")
                else:
                    print(f"❌ Failed to upload {company['Company Name']}: {response.status_code}")
                
                # Rate limiting
                time.sleep(1)
                
            except Exception as e:
                print(f"❌ Error uploading {company['Company Name']}: {e}")
                continue
        
        print(f"✅ Successfully uploaded {uploaded_count}/{len(companies)} leads to Airtable")
        return uploaded_count
    
    def run_full_pipeline(self, max_pages=2):
        """Run the complete lead generation pipeline"""
        print("🚀 Starting Niya Lead Generation Pipeline")
        print("=" * 50)
        
        # Step 1: Scrape startups
        inc42_companies = self.scrape_inc42_startups(max_pages)
        techcrunch_companies = self.scrape_techcrunch_startups(max_pages)
        
        all_companies = inc42_companies + techcrunch_companies
        print(f"📊 Total companies found: {len(all_companies)}")
        
        if not all_companies:
            print("❌ No companies found. Exiting.")
            return
        
        # Step 2: Enrich with LinkedIn profiles
        enriched_companies = self.find_linkedin_profiles(all_companies)
        
        # Step 3: Generate email addresses
        final_companies = self.generate_email_addresses(enriched_companies)
        
        # Step 4: Save to CSV
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        csv_filename = f"leads_{timestamp}.csv"
        self.save_to_csv(final_companies, csv_filename)
        
        # Step 5: Upload to Airtable
        uploaded_count = self.upload_to_airtable(final_companies)
        
        # Summary
        print("\n" + "=" * 50)
        print("📊 Lead Generation Summary")
        print("=" * 50)
        print(f"📄 Companies scraped: {len(all_companies)}")
        print(f"🔗 LinkedIn profiles found: {sum(1 for c in enriched_companies if c.get('LinkedIn Profile'))}")
        print(f"📧 Email patterns generated: {len(final_companies)}")
        print(f"📤 Uploaded to Airtable: {uploaded_count}")
        print(f"💾 CSV saved as: {csv_filename}")
        
        return final_companies

def main():
    """Main function to run lead generation"""
    generator = LeadGenerator()
    leads = generator.run_full_pipeline(max_pages=2)
    
    if leads:
        print("\n🎉 Lead generation completed successfully!")
        print("   Your Niya agent can now process these new leads.")
    else:
        print("\n❌ Lead generation failed. Please check the errors above.")

if __name__ == "__main__":
    main() 