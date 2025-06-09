import logging

from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_openai import ChatOpenAI

from filter.job import JobFilter

logger = logging.getLogger(__name__)


def get_llm_job_filters(query_text: str) -> dict:
    """
    Generate a smart job filter using an LLM based on the provided query text.
    EXAMPLE:

    ```
        query_text = "at least $80000 medium size company remote in Matthewshaven"

        {
            'salary__gte': 80000,
            'remote': True,
            'location__ilike': 'Matthewshaven',
            'company_employee_count__gte': 51, 'company_employee_count__lte': 250
        }
    ```

    ```
    query_text = "salary of at least $100000 in San Francisco"

    {
        'salary__gte': 100000,
        'location__ilike': 'San Francisco'
    }
    ```
    """
    llm = ChatOpenAI(
        model="gpt-4.1", temperature=0.0, max_tokens=1000, timeout=60, max_retries=2
    ).with_structured_output(method="json_mode")

    template = """
    You are a job filter generator.
    Given a query, generate a JSON object that can be used to filter jobs in a database.
    Each value should only be used on a single field based on what is most suitable
    where the values belong to one of the field examples, the field should take priority.
    {format_instructions}
    {query}
    """

    parser = JsonOutputParser(pydantic_object=JobFilter)
    prompt = PromptTemplate(
        template=template,
        input_variables=["query"],
        partial_variables={"format_instructions": parser.get_format_instructions()},
    )

    logger.info("LLM prompt: %s", prompt)

    chain = LLMChain(llm=llm, prompt=prompt)

    response = chain.run({"query": query_text})

    logger.info("LLM response: %s", response)

    smart_filter = {k: v for k, v in response.items() if v not in (None, 0, "", [], {})}

    return smart_filter
