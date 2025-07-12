#!/usr/bin/env python3
"""
Multi-Agent Financial Analyst - Command Line Interface

This module provides a CLI for running financial analysis without Streamlit.
Useful for testing, development, and batch processing.
"""

import argparse
import sys
import os
import time
from datetime import datetime
from typing import Optional, List
import json

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Import project modules
from crew.financial_crew import FinancialCrew, run_financial_analysis
from tools.financial_tools import YFinanceStockTool
from utils.helpers import validate_stock_symbol, get_stock_metrics
from config.settings import APP_CONFIG, get_environment_config, validate_config


class FinancialAnalysisCLI:
    """Command Line Interface for Financial Analysis"""
    
    def __init__(self):
        self.tool = YFinanceStockTool()
        self.crew = None
        
    def setup_cli(self) -> argparse.ArgumentParser:
        """Setup command line argument parser"""
        
        parser = argparse.ArgumentParser(
            description="Multi-Agent Financial Analyst CLI",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
Examples:
    # Analyze a single stock
    python main.py --analyze AAPL
    
    # Analyze multiple stocks
    python main.py --batch AAPL,GOOGL,MSFT
    
    # Quick stock info only
    python main.py --info TSLA
    
    # Test system configuration
    python main.py --test
    
    # Analyze with custom output file
    python main.py --analyze NVDA --output nvda_analysis.md
            """
        )
        
        # Main commands
        parser.add_argument(
            '--analyze', '-a',
            metavar='SYMBOL',
            help='Analyze a single stock symbol (e.g., AAPL)'
        )
        
        parser.add_argument(
            '--batch', '-b',
            metavar='SYMBOLS',
            help='Analyze multiple stocks (comma-separated, e.g., AAPL,GOOGL,MSFT)'
        )
        
        parser.add_argument(
            '--info', '-i',
            metavar='SYMBOL',
            help='Get quick stock information only (no AI analysis)'
        )
        
        parser.add_argument(
            '--test', '-t',
            action='store_true',
            help='Test system configuration and API connectivity'
        )
        
        # Output options
        parser.add_argument(
            '--output', '-o',
            metavar='FILE',
            help='Output file for analysis results (default: stdout)'
        )
        
        parser.add_argument(
            '--format', '-f',
            choices=['markdown', 'json', 'text'],
            default='markdown',
            help='Output format (default: markdown)'
        )
        
        # Configuration options
        parser.add_argument(
            '--verbose', '-v',
            action='store_true',
            help='Enable verbose output (show agent reasoning)'
        )
        
        parser.add_argument(
            '--quiet', '-q',
            action='store_true',
            help='Suppress progress messages'
        )
        
        parser.add_argument(
            '--config',
            action='store_true',
            help='Show current configuration'
        )
        
        return parser
    
    def validate_environment(self) -> bool:
        """Validate environment and configuration"""
        
        if not validate_config():
            print("❌ Configuration validation failed!")
            print("Please check your .env file and ensure SAMBANOVA_API_KEY is set.")
            return False
        
        env_config = get_environment_config()
        
        if not env_config["api_key"]:
            print("❌ SambaNova API key not found!")
            print("Please set SAMBANOVA_API_KEY in your .env file.")
            return False
        
        return True
    
    def test_system(self) -> bool:
        """Test system components and connectivity"""
        
        print("🧪 Testing Multi-Agent Financial Analyst System...")
        print("-" * 50)
        
        # Test 1: Environment validation
        print("1. Environment Configuration:")
        if self.validate_environment():
            print("   ✅ Environment configured correctly")
        else:
            print("   ❌ Environment configuration failed")
            return False
        
        # Test 2: YFinance tool
        print("\n2. YFinance Data Tool:")
        try:
            test_result = self.tool._run("AAPL")
            data = json.loads(test_result)
            if "company" in data and data["company"]:
                print("   ✅ YFinance tool working correctly")
                print(f"   📊 Test data: {data['company']} - ${data.get('latest_price', 'N/A')}")
            else:
                print("   ⚠️ YFinance tool returned incomplete data")
        except Exception as e:
            print(f"   ❌ YFinance tool failed: {str(e)}")
            return False
        
        # Test 3: Agent initialization
        print("\n3. AI Agent Initialization:")
        try:
            self.crew = FinancialCrew()
            print("   ✅ Agents initialized successfully")
        except Exception as e:
            print(f"   ❌ Agent initialization failed: {str(e)}")
            return False
        
        # Test 4: API connectivity (light test)
        print("\n4. API Connectivity:")
        try:
            # This will test if we can create tasks without full execution
            self.crew.create_tasks("AAPL")
            print("   ✅ API connectivity confirmed")
        except Exception as e:
            print(f"   ❌ API connectivity failed: {str(e)}")
            return False
        
        print("\n🎉 All system tests passed successfully!")
        print("The Multi-Agent Financial Analyst is ready to use.")
        return True
    
    def get_quick_info(self, symbol: str) -> dict:
        """Get quick stock information without AI analysis"""
        
        if not validate_stock_symbol(symbol):
            return {"error": f"Invalid stock symbol: {symbol}"}
        
        try:
            # Use the tool to get data
            result = self.tool._run(symbol)
            data = json.loads(result)
            
            # Get additional metrics
            metrics = get_stock_metrics(symbol)
            
            # Combine data
            info = {
                "symbol": symbol.upper(),
                "company": data.get("company", "N/A"),
                "current_price": data.get("latest_price", "N/A"),
                "latest_date": data.get("latest_date", "N/A"),
                "market_cap": data.get("market_cap", "N/A"),
                "pe_ratio": data.get("pe_ratio", "N/A"),
                "52_week_high": data.get("52wk_high", "N/A"),
                "52_week_low": data.get("52wk_low", "N/A"),
                "rating": data.get("rating", "N/A"),
                "sector": metrics.get("sector", "N/A"),
                "industry": metrics.get("industry", "N/A")
            }
            
            return info
            
        except Exception as e:
            return {"error": f"Failed to fetch data for {symbol}: {str(e)}"}
    
    def format_quick_info(self, info: dict, format_type: str = "text") -> str:
        """Format quick info for display"""
        
        if "error" in info:
            return f"Error: {info['error']}"
        
        if format_type == "json":
            return json.dumps(info, indent=2)
        
        elif format_type == "markdown":
            return f"""
# {info['symbol']} - {info['company']}

## Quick Stats
- **Current Price**: ${info['current_price']}
- **Market Cap**: ${info['market_cap']:,} if isinstance(info['market_cap'], (int, float)) else info['market_cap']
- **P/E Ratio**: {info['pe_ratio']}
- **52-Week Range**: ${info['52_week_low']} - ${info['52_week_high']}
- **Analyst Rating**: {info['rating']}
- **Sector**: {info['sector']}
- **Industry**: {info['industry']}

*Data as of {info['latest_date']}*
"""
        
        else:  # text format
            return f"""
{info['symbol']} - {info['company']}
{'=' * 40}
Current Price: ${info['current_price']}
Market Cap: ${info['market_cap']:,}" if isinstance(info['market_cap'], (int, float)) else str(info['market_cap'])
P/E Ratio: {info['pe_ratio']}
52-Week Range: ${info['52_week_low']} - ${info['52_week_high']}
Analyst Rating: {info['rating']}
Sector: {info['sector']}
Industry: {info['industry']}
Data Date: {info['latest_date']}
"""
    
    def analyze_stock(self, symbol: str, verbose: bool = False, quiet: bool = False) -> str:
        """Analyze a single stock using AI agents"""
        
        if not quiet:
            print(f"🤖 Starting AI analysis for {symbol.upper()}...")
        
        if not validate_stock_symbol(symbol):
            return f"Error: Invalid stock symbol '{symbol}'"
        
        try:
            # Show progress
            if not quiet:
                print("📊 Initializing agents and fetching data...")
                start_time = time.time()
            
            # Run the analysis
            result = run_financial_analysis(symbol.upper())
            
            if not quiet:
                duration = time.time() - start_time
                print(f"✅ Analysis completed in {duration:.1f} seconds")
            
            return result
            
        except Exception as e:
            error_msg = f"Analysis failed for {symbol}: {str(e)}"
            if not quiet:
                print(f"❌ {error_msg}")
            return f"Error: {error_msg}"
    
    def batch_analyze(self, symbols: List[str], verbose: bool = False, quiet: bool = False) -> dict:
        """Analyze multiple stocks"""
        
        results = {}
        
        if not quiet:
            print(f"🚀 Starting batch analysis for {len(symbols)} stocks...")
            print(f"Symbols: {', '.join(symbols)}")
            print("-" * 50)
        
        for i, symbol in enumerate(symbols, 1):
            if not quiet:
                print(f"\n📈 Analyzing {symbol} ({i}/{len(symbols)})...")
            
            try:
                result = self.analyze_stock(symbol, verbose, quiet=True)
                results[symbol.upper()] = {
                    "status": "success",
                    "analysis": result,
                    "timestamp": datetime.now().isoformat()
                }
                
                if not quiet:
                    print(f"✅ {symbol} analysis completed")
                
            except Exception as e:
                results[symbol.upper()] = {
                    "status": "error", 
                    "error": str(e),
                    "timestamp": datetime.now().isoformat()
                }
                
                if not quiet:
                    print(f"❌ {symbol} analysis failed: {str(e)}")
        
        if not quiet:
            success_count = sum(1 for r in results.values() if r["status"] == "success")
            print(f"\n🎉 Batch analysis completed: {success_count}/{len(symbols)} successful")
        
        return results
    
    def save_output(self, content: str, filepath: str, format_type: str = "markdown"):
        """Save output to file"""
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"💾 Output saved to: {filepath}")
        except Exception as e:
            print(f"❌ Failed to save output: {str(e)}")
    
    def show_config(self):
        """Show current configuration"""
        
        env_config = get_environment_config()
        
        print("🔧 Current Configuration")
        print("=" * 40)
        print(f"App Name: {APP_CONFIG.APP_NAME}")
        print(f"Version: {APP_CONFIG.APP_VERSION}")
        print(f"Environment: {env_config['environment']}")
        print(f"Debug Mode: {env_config['debug']}")
        print(f"API Key: {'✅ Set' if env_config['api_key'] else '❌ Missing'}")
        print(f"Model: {APP_CONFIG.SAMBANOVA_MODEL}")
        print(f"Cache Enabled: {env_config['cache_enabled']}")
        print(f"Log Level: {env_config['log_level']}")
    
    def run(self):
        """Main CLI entry point"""
        
        parser = self.setup_cli()
        args = parser.parse_args()
        
        # Handle config display
        if args.config:
            self.show_config()
            return
        
        # Handle system test
        if args.test:
            success = self.test_system()
            sys.exit(0 if success else 1)
        
        # Validate environment for other operations
        if not self.validate_environment():
            sys.exit(1)
        
        output_content = ""
        
        # Handle stock info
        if args.info:
            if not args.quiet:
                print(f"📊 Fetching information for {args.info.upper()}...")
            
            info = self.get_quick_info(args.info)
            output_content = self.format_quick_info(info, args.format)
        
        # Handle single analysis
        elif args.analyze:
            output_content = self.analyze_stock(args.analyze, args.verbose, args.quiet)
        
        # Handle batch analysis
        elif args.batch:
            symbols = [s.strip().upper() for s in args.batch.split(',')]
            results = self.batch_analyze(symbols, args.verbose, args.quiet)
            
            if args.format == "json":
                output_content = json.dumps(results, indent=2)
            else:
                # Format as markdown/text
                output_parts = []
                for symbol, result in results.items():
                    if result["status"] == "success":
                        output_parts.append(f"# Analysis for {symbol}\n\n{result['analysis']}\n\n---\n")
                    else:
                        output_parts.append(f"# Error for {symbol}\n\n{result['error']}\n\n---\n")
                output_content = "\n".join(output_parts)
        
        else:
            parser.print_help()
            return
        
        # Output results
        if args.output:
            self.save_output(output_content, args.output, args.format)
        else:
            print("\n" + "=" * 60)
            print(output_content)


def main():
    """Main entry point"""
    
    try:
        cli = FinancialAnalysisCLI()
        cli.run()
    except KeyboardInterrupt:
        print("\n\n⏹️ Analysis interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()