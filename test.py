from langchain_openai import ChatOpenAI
from browser_use import Agent
import asyncio
from dotenv import load_dotenv
import json
import argparse
from datetime import datetime

load_dotenv()

# Direct navigation prompt that passes steps to the agent
NAVIGATION_PROMPT = """
Visit this URL: {url}

You are a web automation expert. I want you to navigate through a website by following these steps:
{steps_json}

Follow these steps precisely to reach the target page with the tender information.
After reaching the final page, extract complete tender information including:
- case_name
                        - institution
                        - institution_location
                        - fulfillment_location
                        - case_announcement_date
                        - bid_date
                        - submission_deadline
                        - bid_eligibility
                        - case_summary

Return the data in markdown format with clear headings and structured information.
"""

async def navigate_and_extract(url, steps, llm=None):
    """Navigate through website and extract tender information"""
    llm = llm or ChatOpenAI(model="gpt-4o")
    
    # Pass the navigation steps directly as JSON to the agent
    task = NAVIGATION_PROMPT.format(
        url=url,
        steps_json=json.dumps(steps, ensure_ascii=False, indent=2)
    )
    
    # Create and run the agent
    agent = Agent(task=task, llm=llm)
    
    try:
        result = await agent.run()
        return result
    except Exception as e:
        return f"Error: {str(e)}"

async def main():
    parser = argparse.ArgumentParser(description="Extract tender information with web navigation")
    parser.add_argument("--config", help="JSON config file with URL and navigation steps")
    parser.add_argument("--url", help="Direct URL to process")
    parser.add_argument("--output", help="Output file path (Markdown format)")
    parser.add_argument("--model", default="gpt-4o", help="OpenAI model to use")
    
    args = parser.parse_args()
    
    # Initialize LLM
    llm = ChatOpenAI(model=args.model)
    
    # Default output filename
    if not args.output:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        args.output = f"tender_result_{timestamp}.md"
    
    config_data = None
    
    # Load config from file if provided
    if args.config:
        try:
            with open(args.config, 'r', encoding='utf-8') as f:
                config_data = json.load(f)
            print(f"Using configuration from: {args.config}")
        except Exception as e:
            print(f"Error loading config: {str(e)}")
            return
    
    # Use direct URL if provided
    elif args.url:
        # Default steps for the provided URL
        config_data = {
            "url": args.url,
            "steps": [
                {"action": "click_text", "text": "入札公告情報"},
                {"action": "wait", "ms": 1000},
                {"action": "click_selector", "selector": "#PPUBC00400__search"},
                {"action": "wait", "ms": 1000},
                {"action": "click_text", "text": "ＪＲ奈良駅南特定土地区画整理事業土木技術補助業務委託"}
            ]
        }
        print(f"Using default navigation steps for URL: {args.url}")
    
    # Use example config if no config or URL provided
    else:
        config_data = {
            "url": "https://nara.efftis.jp/PPI/Public/PPUBC00100?kikanno=0201",
            "steps": [
                {"action": "click_text", "text": "入札公告情報"},
                {"action": "wait", "ms": 1000},
                {"action": "click_selector", "selector": "#PPUBC00400__search"},
                {"action": "wait", "ms": 1000},
                {"action": "click_text", "text": "総括的道路維持管理業務委託（総－１）"}
            ]
        }
        print(f"No config provided. Using example navigation for {config_data['url']}")
    
    # Process the tender information
    print(f"Navigating {config_data['url']} and extracting tender information...")
    result = await navigate_and_extract(config_data["url"], config_data["steps"], llm)
    
    # Save result to file
    with open(args.output, 'w', encoding='utf-8') as f:
        f.write(result)
    print(f"Results saved to {args.output}")
    
    # Also print to console
    print("\nExtracted Information:")
    print(result)

if __name__ == "__main__":
    asyncio.run(main())

if __name__ == "__main__":
    asyncio.run(main())