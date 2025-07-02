#!/usr/bin/env python3
"""
Niya Auto Lead Generator
Automatically generates leads from startup websites and uploads to Airtable
"""

import os
import csv
import time
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# Configuration
AIRTABLE_TOKEN = os.getenv("AIRTABLE_TOKEN")
LEADS_BASE_ID = os.getenv("LEADS_BASE_ID")

class AutoLeadGenerator:
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
    
    def scrape_startup_lists(self):
        """Scrape startup data from various sources"""
        print("🔍 Scraping startup data...")
        
        companies = []
        
        # Source 1: Inc42 startups
        try:
            print("📄 Scraping Inc42...")
            inc42_companies = self.scrape_inc42()
            companies.extend(inc42_companies)
            print(f"✅ Found {len(inc42_companies)} companies from Inc42")
        except Exception as e:
            print(f"❌ Inc42 scraping failed: {e}")
        
        # Source 2: Add more sources here
        # You can add more startup directories, tech blogs, etc.
        
        return companies
    
    def scrape_inc42(self):
        """Scrape Inc42 startup directory"""
        companies = []
        
        try:
            url = "https://inc42.com/startups/"
            response = requests.get(url, headers=self.headers, timeout=10)
            soup = BeautifulSoup(response.content, "html.parser")
            
            # Look for startup listings
            articles = soup.find_all("article") or soup.find_all("div", class_="post")
            
            for article in articles[:20]:  # Limit to 20
                try:
                    # Find company name
                    title_elem = (
                        article.find("h2") or 
                        article.find("h3") or 
                        article.find("a", class_="post-title")
                    )
                    
                    if title_elem:
                        company_name = title_elem.get_text(strip=True)
                        
                        # Get link
                        link_elem = article.find("a")
                        link = link_elem.get("href") if link_elem else ""
                        
                        companies.append({
                            "Company Name": company_name,
                            "Source URL": link,
                            "Source": "Inc42"
                        })
                        
                except Exception as e:
                    continue
            
        except Exception as e:
            print(f"❌ Error scraping Inc42: {e}")
        
        return companies
    
    def generate_sample_leads(self):
        """Generate sample leads for testing"""
        print("🎯 Generating sample leads...")
        
        sample_companies = [
            {
                "Company Name": "TechFlow Solutions",
                "Source URL": "https://techflow.com",
                "Source": "Sample",
                "Industry": "SaaS",
                "Company Size": "11-50 employees",
                "Target Role": "VP of Engineering"
            },
            {
                "Company Name": "DataSync Inc",
                "Source URL": "https://datasync.com",
                "Source": "Sample",
                "Industry": "Technology",
                "Company Size": "51-200 employees",
                "Target Role": "CTO"
            },
            {
                "Company Name": "CloudScale Systems",
                "Source URL": "https://cloudscale.com",
                "Source": "Sample",
                "Industry": "Cloud Computing",
                "Company Size": "201-500 employees",
                "Target Role": "VP of Operations"
            },
            {
                "Company Name": "GrowthTech Labs",
                "Source URL": "https://growthtech.com",
                "Source": "Sample",
                "Industry": "Technology",
                "Company Size": "11-50 employees",
                "Target Role": "Head of People"
            },
            {
                "Company Name": "InnovateCorp",
                "Source URL": "https://innovatecorp.com",
                "Source": "Sample",
                "Industry": "SaaS",
                "Company Size": "51-200 employees",
                "Target Role": "VP of Sales"
            }
        ]
        
        print(f"✅ Generated {len(sample_companies)} sample leads")
        return sample_companies
    
    def upload_to_airtable(self, companies):
        """Upload leads to Airtable"""
        print("📤 Uploading leads to Airtable...")
        
        if not AIRTABLE_TOKEN or not LEADS_BASE_ID:
            print("❌ Airtable credentials not configured")
            return 0
        
        headers = {
            "Authorization": f"Bearer {AIRTABLE_TOKEN}",
            "Content-Type": "application/json"
        }
        
        url = f"https://api.airtable.com/v0/{LEADS_BASE_ID}/Imported table"
        
        uploaded_count = 0
        
        for company in companies:
            try:
                # Prepare lead data
                lead_data = {
                    "records": [{
                        "fields": {
                            "Company Name": company.get("Company Name", ""),
                            "Website/LinkedIn": company.get("Source URL", ""),
                            "Industry": company.get("Industry", "Technology"),
                            "Company Size": company.get("Company Size", "11-50 employees"),
                            "Role": company.get("Target Role", "CEO"),
                            "Email": "",  # Will be filled later
                            "Email Sent?": "FALSE",
                            "Status": "New Lead",
                            "Notes/Objections": f"Auto-generated from {company.get('Source', 'Unknown')} on {datetime.now().strftime('%Y-%m-%d')}"
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
        
        return uploaded_count
    
    def save_to_csv(self, companies, filename=None):
        """Save leads to CSV file"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"leads_{timestamp}.csv"
        
        print(f"💾 Saving {len(companies)} leads to {filename}...")
        
        fieldnames = ["Company Name", "Source URL", "Source", "Industry", "Company Size", "Target Role"]
        
        with open(filename, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(companies)
        
        print(f"✅ Saved leads to {filename}")
        return filename
    
    def run_generation(self, use_samples=True, scrape_websites=False):
        """Run the lead generation process"""
        print("🚀 Starting Niya Auto Lead Generation")
        print("=" * 50)
        
        companies = []
        
        if use_samples:
            # Generate sample leads for testing
            companies.extend(self.generate_sample_leads())
        
        if scrape_websites:
            # Scrape real startup data
            scraped_companies = self.scrape_startup_lists()
            companies.extend(scraped_companies)
        
        if not companies:
            print("❌ No companies found. Exiting.")
            return
        
        print(f"📊 Total companies to process: {len(companies)}")
        
        # Save to CSV
        csv_filename = self.save_to_csv(companies)
        
        # Upload to Airtable
        uploaded_count = self.upload_to_airtable(companies)
        
        # Summary
        print("\n" + "=" * 50)
        print("📊 Lead Generation Summary")
        print("=" * 50)
        print(f"📄 Companies generated: {len(companies)}")
        print(f"📤 Uploaded to Airtable: {uploaded_count}")
        print(f"💾 CSV saved as: {csv_filename}")
        
        if uploaded_count > 0:
            print(f"\n🎉 Successfully added {uploaded_count} new leads!")
            print("   Run 'python niya_agent.py' to start sending emails.")
        else:
            print("\n⚠️ No leads were uploaded. Check Airtable configuration.")
        
        return companies

def main():
    """Main function"""
    generator = AutoLeadGenerator()
    
    # For testing, use sample leads
    # For production, set use_samples=False and scrape_websites=True
    leads = generator.run_generation(
        use_samples=True,  # Set to False for real scraping
        scrape_websites=False  # Set to True to scrape real websites
    )
    
    if leads:
        print("\n✅ Lead generation completed!")
    else:
        print("\n❌ Lead generation failed.")

if __name__ == "__main__":
    main() 