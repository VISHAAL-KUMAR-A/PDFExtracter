from openai import OpenAI
from typing import List, Dict, Any
import os
from dotenv import load_dotenv
import json

load_dotenv()


class LLMService:
    """Service for processing text with OpenAI LLM"""

    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError(
                "OPENAI_API_KEY not found in environment variables")

        self.client = OpenAI(api_key=api_key)
        self.model = "gpt-4o-mini"  # Fast and cost-effective model

    def extract_data(self, extracted_texts: List[Dict[str, str]], template_id: str) -> Dict[str, Any]:
        """
        Extract structured data from text using LLM

        Args:
            extracted_texts: List of dictionaries with filename and text
            template_id: Template to use for extraction

        Returns:
            Structured data dictionary
        """
        template_prompt = self._get_template_prompt(template_id)

        # Combine all texts
        combined_text = "\n\n=== NEW DOCUMENT ===\n\n".join(
            [f"Filename: {item['filename']}\n\n{item['text']}" for item in extracted_texts]
        )

        prompt = f"""You are an expert data extraction assistant specializing in Private Equity Fund documents.

{template_prompt}

EXTRACTED TEXT FROM PDF(S):
{combined_text}

INSTRUCTIONS:
1. Carefully analyze the provided PDF text(s)
2. Extract ALL relevant information according to the template structure
3. Return the data as a valid JSON object with the exact structure specified
4. If a field is not found in the document, use null or an empty string
5. For numerical values, extract as numbers (not strings)
6. For dates, use ISO format (YYYY-MM-DD) if possible
7. Ensure all extracted data is accurate and matches the source document

Return ONLY the JSON object, no additional text or explanation.
"""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert data extraction assistant specializing in Private Equity Fund documents. Always return valid JSON only."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1,
                response_format={"type": "json_object"}
            )

            result_text = response.choices[0].message.content.strip()

            # Extract JSON from response (in case there's markdown formatting)
            if result_text.startswith("```json"):
                result_text = result_text[7:]
            if result_text.startswith("```"):
                result_text = result_text[3:]
            if result_text.endswith("```"):
                result_text = result_text[:-3]

            result_text = result_text.strip()

            # Parse JSON
            structured_data = json.loads(result_text)
            return structured_data

        except json.JSONDecodeError as e:
            # If JSON parsing fails, return a structured error response
            return {
                "error": "Failed to parse LLM response",
                "raw_response": result_text[:1000] if 'result_text' in locals() else "No response",
                "template_id": template_id
            }
        except Exception as e:
            raise Exception(f"Error processing with LLM: {str(e)}")

    def _get_template_prompt(self, template_id: str) -> str:
        """Get the extraction prompt for the specified template"""

        if template_id == "template1":
            return """
TEMPLATE 1: Private Equity Funds - Detailed Extraction

Extract data according to the following structure (return as JSON):

{
  "fund_information": {
    "fund_name": "",
    "fund_partnership": "",
    "investment_vehicle": "",
    "fund_term": "",
    "vintage_year": "",
    "fund_size": "",
    "currency": "",
    "fund_status": ""
  },
  "fund_manager": {
    "manager_name": "",
    "gp_name": "",
    "contact_person": "",
    "email": "",
    "phone": "",
    "address": "",
    "founded_date": ""
  },
  "financial_position": {
    "reporting_date": "",
    "total_commitments": null,
    "paid_in_capital": null,
    "unfunded_commitments": null,
    "nav_before_carry": null,
    "nav_after_carry": null,
    "total_distributions": null,
    "irr": null,
    "moic": null
  },
  "lp_investors": [
    {
      "investor_name": "",
      "commitment_amount": null,
      "paid_in_capital": null,
      "distributions": null,
      "nav": null,
      "ownership_percentage": null
    }
  ],
  "fund_companies": [
    {
      "company_name": "",
      "sector": "",
      "industry": "",
      "country": "",
      "investment_date": "",
      "initial_investment": null,
      "current_value": null,
      "ownership_percentage": null,
      "status": ""
    }
  ],
  "company_valuations": [
    {
      "company_name": "",
      "valuation_date": "",
      "valuation_method": "",
      "enterprise_value": null,
      "equity_value": null
    }
  ],
  "company_financials": [
    {
      "company_name": "",
      "financial_date": "",
      "revenue": null,
      "ebitda": null,
      "net_income": null,
      "total_assets": null,
      "total_debt": null,
      "total_equity": null
    }
  ],
  "investment_history": [
    {
      "company_name": "",
      "transaction_date": "",
      "transaction_type": "",
      "amount": null,
      "valuation": null
    }
  ]
}
"""
        elif template_id == "template2":
            return """
TEMPLATE 2: Private Equity Funds - Executive Summary Extraction

Extract data according to the following structure (return as JSON):

{
  "executive_summary": {
    "fund_name": "",
    "reporting_period": "",
    "total_commitments": null,
    "total_invested": null,
    "total_realized": null,
    "total_unrealized": null,
    "nav": null,
    "irr": null,
    "moic": null,
    "dpi": null,
    "rvpi": null,
    "tvpi": null
  },
  "schedule_of_investments": [
    {
      "company_name": "",
      "investment_date": "",
      "cost_basis": null,
      "fair_value": null,
      "unrealized_gain_loss": null,
      "ownership_percentage": null,
      "sector": "",
      "geography": ""
    }
  ],
  "operations_statement": {
    "reporting_period": "",
    "investment_income": null,
    "interest_income": null,
    "dividend_income": null,
    "realized_gains": null,
    "unrealized_gains": null,
    "management_fees": null,
    "operating_expenses": null,
    "net_investment_income": null
  },
  "cashflow_statement": {
    "reporting_period": "",
    "capital_calls": null,
    "investment_purchases": null,
    "operating_expenses_paid": null,
    "distributions_to_lps": null,
    "proceeds_from_sales": null,
    "dividend_received": null,
    "net_cash_flow": null
  },
  "pcap_statement": {
    "reporting_period": "",
    "beginning_capital": null,
    "capital_contributions": null,
    "capital_distributions": null,
    "net_income_loss": null,
    "ending_capital": null
  },
  "portfolio_companies": [
    {
      "company_name": "",
      "description": "",
      "headquarters": "",
      "sector": "",
      "investment_date": "",
      "investment_amount": null,
      "ownership_percentage": null,
      "key_management": [],
      "website": ""
    }
  ],
  "portfolio_financials": [
    {
      "company_name": "",
      "fiscal_year": "",
      "revenue": null,
      "ebitda": null,
      "ebitda_margin": null,
      "net_income": null,
      "capex": null,
      "employees": null
    }
  ],
  "footnotes": [
    {
      "reference": "",
      "description": ""
    }
  ]
}
"""
        else:
            raise ValueError(f"Unknown template_id: {template_id}")
