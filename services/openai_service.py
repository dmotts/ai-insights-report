import openai
import logging
from typing import List
from cachetools import cached, TTLCache
from config import Config

class OpenAIService:
    def __init__(self, api_key: str, model: str):
        if not Config.ENABLE_OPENAI_SERVICE:
            logging.info('OpenAI service is disabled.')
            return

        openai.api_key = api_key
        self.client = openai
        self.model = model
        self.logger = logging.getLogger(__name__)
        self.cache = TTLCache(maxsize=100, ttl=300)  # Cache results for 5 minutes

    def generate_report_content(self, industry: str, answers: List[str]) -> dict:
        if not Config.ENABLE_OPENAI_SERVICE:
            logging.info('OpenAI service is disabled. Skipping report content generation.')
            return {}

        try:
            # Construct the prompt
            prompt = self.build_prompt(industry, answers)

            self.logger.debug('Generating report content with OpenAI')
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1500
            )
            report_content = response.choices[0].message.content
            self.logger.info('Report content generated successfully')

            self.logger.info(f'Your AI Insights Report:  {report_content}')

            # Parse and return the content
            return {
                                'introduction': self.extract_section(report_content, "Introduction") if report_content else "",
                                'industry_trends': self.extract_section(report_content, "Industry Trends") if report_content else "",
                'ai_solutions': self.extract_section(report_content, "AI Solutions") if report_content else "",
                'analysis': self.extract_section(report_content, "Analysis") if report_content else "",
                'conclusion': self.extract_section(report_content, "Conclusion") if report_content else ""
            }
        except Exception as e:
            self.logger.error(f'Error generating report content: {e}')
            return {}

    def build_prompt(self, industry: str, answers: List[str]) -> str:
        return f"""
        You are an AI consultant preparing a comprehensive report for a business owner in the {industry} industry. The report must be detailed, insightful, and structured into the following sections:

        1. **Introduction**: Provide a brief overview of the business's context based on the industry.
        2. **Industry Trends**: Provide the latest AI trends in the {industry} industry.
        3. **AI Solutions**: Offer AI-driven solutions for the following business needs:
            - Current data management and utilization challenges: {answers[0]}
            - Areas of technology integration and inefficiency: {answers[1]}
            - Long-term business goals and AI's role in achieving them: {answers[2]}
        4. **Analysis and Recommendations**:
            - Include a detailed analysis of how AI can address the specific challenges mentioned.
            - Offer actionable recommendations for AI implementation.
        5. **Conclusion**: Summarize the key insights and recommend next steps.

        Ensure the report is structured professionally, with clear headings and well-organized content. Also, include a call-to-action encouraging the business owner to engage with Daley Mottley AI Consulting for further AI consulting services.

        The report should be in the following format embedded in HTML code with the brackets filled in with the appropraite content:

        ## Format
        ```
        <body>
            <header>
                <img src="{{ url_for('static', filename='images/logo.png') }}" alt="Daley Mottley AI Consulting">
                <h1>AI Insights Report</h1>
            </header>

            <div class="container">
                <section>
                    <h2>Introduction</h2>
                    <p>{{ introduction }}</p>
                </section>

                <section>
                    <h2>Industry Trends</h2>
                    <p>{{ industry_trends }}</p>
                </section>

                <section>
                    <h2>AI Solutions</h2>
                    <p>{{ ai_solutions }}</p>
                </section>

                <section>
                    <h2>Analysis</h2>
                    <p>{{ analysis }}</p>
                </section>

                <section>
                    <h2>Conclusion</h2>
                    <p>{{ conclusion }}</p>
                </section>

                <section class="cta">
                    <h2>Ready to Implement AI in Your Business?</h2>
                    <p>Contact Daley Mottley AI Consulting for expert guidance on how AI can transform your business. Let us help you stay ahead of the competition with cutting-edge AI solutions.</p>
                    <a href="mailto:daley.mottley@hotmail.com">Contact Us Today</a>
                </section>
            </div>

            <footer>
                <p>Daley Mottley AI Consulting | All Rights Reserved &copy; {{ current_year }}</p>
            </footer>
        </body>
        ```
        """

    def extract_section(self, content: str, section_title: str) -> str:
        # Simple method to extract sections from the generated content
        start = content.find(f"**{section_title}**")
        if start == -1:
            return ""
        end = content.find("**", start + len(section_title) + 4)
        return content[start + len(section_title) + 4:end].strip() if end != -1 else content[start + len(section_title) + 4:].strip()
